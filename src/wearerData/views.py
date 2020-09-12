from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.settings import api_settings

from rest_framework import status
from rest_framework.response import Response

from .models import WearerData, WearerEvent, WearerStats, HeatPreEvent
from .serializers import WearerDataSerializer, WearerEventSerializer
from users.models import CustomUser

from datetime import datetime, timedelta


class WearerDataPostView(CreateAPIView):
    # url: /linkedUser/post/
    # TODO 로그인한 유저가 스스로와 연관된 유저만 추가할 수 있다는 security error 설정 넣기

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # FIXED: 위 코드 떄문에 계속 Anonymous User 관련 오류 떴었는데, 이는 self.request.user을 쓰기 위해서는 `authentication_classes = [어쩌고]`로 header에 숨겨져 있는 token을 찾아내는 코드(재료)가 필요하기 때문인 것으로 추정된다.

    queryset = WearerData.objects.all()
    serializer_class = WearerDataSerializer
    # overrided method

    def create(self, request, *args, **kwargs):
        '''
        Overrided method. added update_data which includes status: sucess.
        '''
        # SECTION original method
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        response = Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        # SECTION overrided code
        # customizing the original_response.data
        update_data = {
            "data": serializer.data,
            "status": "success"
        }
        response.data.clear()
        response.data.update(update_data)
        removeStatsNData(self.request.user)
        self.check_event(serializer.data)
        return response

    def perform_create(self, serializer):
        '''
        Overrided method. saves user as self.request.user to the serializer.
        '''
        serializer.save(user=self.request.user)

    def check_event(self, sensorData):
        '''
        EXPLANATION
        메모이제이션: pre_event에다가 미리 저장해두고 a_start, b_start, c_start 등으로 무슨 이벤트가 얼마나 지속되었는 지 확인해서 이벤트 발생 확인하면 이벤트 데이터 save

        '''
        # 열지수 계산
        heatIndex = self.calHeatIndex(
            int(sensorData['temp']), int(sensorData['humid']))

        # 열지수 유형 분류
        eventType = self.getHeatPhase(heatIndex)

        # preEvent 저장
        if eventType == "N" or len(HeatPreEvent.objects.filter(user=self.request.user)) == 0:
            HeatPreEvent.objects.create(
                user=self.request.user, eventType=eventType)

        else:
            before = HeatPreEvent.objects.filter(
                user=self.request.user).latest('id')

            if before.eventType == 'N':
                HeatPreEvent.objects.create(
                    user=self.request.user, eventType=eventType)

            elif before.eventType == eventType:
                current = HeatPreEvent.objects.create(
                    user=self.request.user, a_start=before.a_start, b_start=before.b_start, c_start=before.c_start, eventType=eventType)
                # 이벤트 detect
                self.detectHeatEvent(current)

            else:
                if before.eventType < eventType:

                    if before.eventType == "A" and eventType == "B":
                        HeatPreEvent.objects.create(
                            user=self.request.user, a_start=before.a_start, c_start=before.c_start, eventType=eventType)

                    elif before.eventType == "B" and eventType == "C":
                        HeatPreEvent.objects.create(
                            user=self.request.user, a_start=before.a_start, b_start=before.b_start, eventType=eventType)

                    elif before.eventType == "A" and eventType == "C":
                        # A에서 바로 C로 넘어가도 C는 B 유형에 속하기 떄문에 (A>B>C, 여기서 >는 집합에 속한다는 의미)
                        HeatPreEvent.objects.create(
                            user=self.request.user, a_start=before.a_start, eventType=eventType)

                else:
                    HeatPreEvent.objects.create(
                        user=self.request.user, a_start=before.a_start, b_start=before.b_start, c_start=before.c_start, eventType=eventType)

    def calHeatIndex(self, temp, humid):
        temp = 32 + (9/5 + temp)
        heatIndex = (-42.379 + (2.04901523 * temp) + (10.14333127 * humid) - (0.22475541 * temp * humid) - (0.00683770 * humid * humid) - (0.05481717 *
                                                                                                                                           humid * humid) + (0.00122874 * temp * temp * humid) + (0.00085282 * temp * humid * humid) - (0.00000199 * temp * temp * humid * humid))
        return (heatIndex - 32) / 1.8

    def getHeatPhase(self, heatIndex):
        if heatIndex >= 32:
            # 주의
            return "A"
        if heatIndex >= 41:
            # 위험
            return "B"
        if heatIndex >= 54:
            # 매우위험
            return "C"
        return "N"

    def detectHeatEvent(self, current):
        '''
        EXPLANATION
        이벤트가 있는 지 확인하고 없으면 지나가기, 있으면 WearerEvent.save()
        '''

        danger_time = {'A': timedelta(hours=2), 'B': timedelta(
            hours=1), 'c': timedelta(minutes=30)}
        a_start, b_start, c_start = current.a_start, current.b_start, current.c_start

        # 모든 경우에
        if datetime.now().time() - a_start > danger_time['A']:
            event = WearerEvent(user=self.request.user, heatIllEvent='A')

        if current.eventType == "B" or current.eventType == "C":
            if datetime.now().time() - b_start > danger_time['B']:
                event = WearerEvent(user=self.request.user, heatIllEvent='B')

        if current.eventType == "C":
            if datetime.now().time() - c_start > danger_time['C']:
                event = WearerEvent(user=self.request.user, heatIllEvent='C')

        # 가장 위험한 경우만 event save해서 push alarm
        try:
            event.save()
            return
        except:
            return


class SensorGetView(ListAPIView):
    '''
    END POINT
    wearerData/get/

    CALLING SEQUENCE
    list - sensorList - eachSensorList - statsDict, getTodayStats
                      - stepCountList  - getTodayStats

    EXPLANATIONS
    get statistic version of wearerdata(sensor datas) to the wearer
    and also to the protector, whose protector-wearer relationships are saved in linkedUsers model.

    INPUT
    as get param, needs
    1. wearerID: wearer_username
    2. sensorName: which_sensor(choices: 'tempHumid', 'sound', 'heartRate', 'stepCount')

    OUTPUT
    type=json, if no wearerData posted on that day, -1
    examples of json form is written in eachSensorList, and stepCountList.
    '''
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    recent7days = [datetime.now().date()-timedelta(days=i)
                   for i in range(6, -1, -1)]
    # 오름차순으로 6일 전부터 오늘까지

    queryset = WearerData.objects.order_by('nowDate').filter(
        nowDate=recent7days[-1])

    serializer_class = WearerDataSerializer

    def list(self, request, *args, **kwargs):
        # SECTION original method
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # SECTION overrided code
        print(self.request.user, self.request.query_params.get('wearerID'))

        if self.request.user.user_type == "P":
            # protector가 요청하는 경우, wearer 확인하기
            wearID = self.request.query_params.get('wearerID')
            self.wearer = CustomUser.objects.get(username=wearID)
            linkedUsers = self.request.user.protectee.filter(
                wearer=self.wearer)
            if len(linkedUsers) != 0:
                queryset = queryset.filter(user=linkedUsers[0].wearer)
            else:
                raise ValueError(
                    "The relationship is not registered in linkedUsers model!")
        else:
            # wearer가 요청하는 경우
            self.wearer = self.request.user
            queryset = queryset.filter(user=self.request.user)
        serializer = self.get_serializer(queryset, many=True)

        if self.request.query_params.get('sensorName') not in ['tempHumid', 'sound', 'heartRate', 'stepCount']:
            raise ValueError(
                "the params should be one of these: 'tempHumid', 'sound', 'heartRate', 'stepCount'")

        return Response(self.sensorList(serializer.data, self.request.query_params.get('sensorName')))

    def sensorList(self, sensorDataList, sensorName):
        '''
        EXPLANATION
        get each sensors' statistic values(min, max, avg) by dict form.
        sensor stepCount is an exception.

        INPUT
        sensorDataList: list of OrderedDict
        sensorName: str, choices) 'tempHumid', 'sound', 'heartRate', 'stepCount'

        TIME
        time complexity: O(n*m),
        where n = len(sensorName), m = len(sensorDataList)

        '''
        if sensorName == 'tempHumid':
            return self.eachSensorList(sensorDataList, 'temp', 'humid')
        elif sensorName == "stepCount":
            return self.stepCountList(sensorDataList)
        else:
            return self.eachSensorList(sensorDataList, sensorName)

    def eachSensorList(self, sensorDataList, *sensorName):
        '''
        EXPLANATION
        get each sensors' statistic values(min, max, avg) by dict form.
        sensor stepCount is an exception.

        OUTPUT
        returns dictionary which has form like the following
        update_data = {
            "day": {
                "sensor": {
                    "avg": avg,
                    "min": min,
                    "max": max
                },
                ...
            },
            ...
        }

        '''
        today_stats = dict()
        for sensor in sensorName:
            today_stats[sensor] = self.getTodayStats(
                sensorDataList, sensor)

        update_data = dict()

        for i in range(6):
            # 6일 전~ 1일 전: Stats에서 가져오기
            day = self.recent7days[i]
            update_data[str(day)] = dict()
            for sensor in sensorName:
                update_data[str(day)][sensor] = self.statsDict(day, sensor)
        update_data[str(self.recent7days[-1])] = today_stats

        return update_data

    def statsDict(self, date, sensor):
        '''
        EXPLANATION
        get statistics values of 6 days ago ~ yesterday from WearerStats

        INPUT
        date: datetime.date object
        sensor: string, choice = temp, humid, sound, heartRate

        TIME COMPLEXITY
        Vary by the filtering process in db

        OUTPUT
        return d = {
            "avg": avgval,
            "max": maxval,
            "min": minval,
        }

        if no certain data which contains date and sensor value,
        then return d = {"avg": -1, "min": -1, "max": -1}
        '''
        qs = WearerStats.objects.filter(user=self.wearer, nowDate=date)
        d = dict()
        if len(qs) == 0:
            d = {"avg": -1, "min": -1, "max": -1}
        elif len(qs) == 1:
            stat = qs[0].__dict__
            d = {
                "avg": stat[sensor+'_avg'],
                "max": stat[sensor+'_max'],
                "min": stat[sensor+'_min'],
            }
        else:
            raise ValueError(
                "This data instance's (date, user) in WearerStats is not unique.")
        return d

    def getTodayStats(self, sensorDataList, sensorName):
        '''
        EXPLANATION
        get statistics values of today sensorData

        INPUT
        sensorDataList: list of OrderedDict
        sensorName can be temp, humid, sound, heartRate, stepCount

        TIME
        time complexity: O(n), where n = len(sensorDataList)

        OUTPUT
        if sensorName == "stepCount" : returns tot value of stepCount at that day
        else: returns avg, min, max values of each day in sensorDataList

        '''
        # 변수 초기화(에러 방지)
        minV = 10000
        maxV = -10000
        if sensorName != "stepCount":
            if len(sensorDataList) == 0:
                return {'avg': -1, 'max': -1, 'min': -1}
            statValues = dict()
            tot = cnt = 0

            for i in range(len(sensorDataList)):
                cur_sens = int(sensorDataList[i][sensorName])
                tot += cur_sens
                if minV > cur_sens:
                    minV = cur_sens
                if maxV < cur_sens:
                    maxV = cur_sens
                cnt += 1

        # 마지막 날짜 케어해주기
            statValues['avg'] = tot/cnt
            statValues['max'] = maxV
            statValues['min'] = minV
        else:
            if len(sensorDataList) == 0:
                return -1
            statValues = int(sensorDataList[len(sensorDataList)-1][sensorName])

        return statValues

    def stepCountList(self, sensorDataList):
        '''
        EXPLANATION
        get stepCount's value by dict form.

        OUTPUT
        returns dictionary which has form like the following
        update_data = {
            "sensor": {
                "day": val,
                ...
            },
            ...
        }

        '''
        sensor = 'stepCount'
        update_data = dict()
        update_data[sensor] = dict()

        for i in range(6):
            # 6일 전~ 1일 전: Stats에서 가져오기
            day = self.recent7days[i]
            qs = WearerStats.objects.filter(nowDate=day, user=self.wearer)
            if len(qs) == 1:
                update_data[sensor][str(day)] = qs[0].stepCount
            elif len(qs) == 0:
                update_data[sensor][str(day)] = -1
            else:
                raise ValueError(
                    "This data instance's (date, user) in WearerStats is not unique.")

        today_stats = self.getTodayStats(sensorDataList, sensor)
        update_data[sensor][str(self.recent7days[-1])] = today_stats
        return update_data


class WearerEventPostView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = WearerEvent.objects.all()
    serializer_class = WearerEventSerializer

    def create(self, request, *args, **kwargs):
        '''
        Overrided method. added update_data which includes status: sucess.
        '''
        # SECTION original method
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        response = Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        # SECTION overriding code
        # customizing the original_response.data
        update_data = {
            "data": serializer.data,
            "status": "success"
        }
        response.data.clear()
        response.data.update(update_data)

        return response

    def perform_create(self, serializer):
        '''
        Overrided method. saves user as self.request.user to the serializer.
        '''

        serializer.save(user=self.request.user)


def removeStatsNData(wearer):
    '''
    1.  lastStatsDate < lastDataDate일 때,
            그 사이 date에 대해 wearerData => stats로 추가
    2.  7일 이전 wearerData는 삭제하기
    3.  1년 이전 wearerStats 삭제
    '''
    today = datetime.now().date()
    if wearer.dataRemovedDate == today or len(WearerData.objects.filter(nowDate__lt=today)) == 0:
        # 1. 이미 오늘 removeStatsNData()를 call했거나(실행시간 줄이기 위해 session 사용)
        # 2. 막 회원가입해서 예전 데이터가 없을 경우
        return
    else:
        # 업데이트하고 다음 코드들 실행
        wearer.dataRemovedDate = today
        wearer.save()

    yearAgo = datetime.now().date()-timedelta(days=365)
    weekAgo = datetime.now().date()-timedelta(days=7)

    # SECTION 1. lastStatsDate < lastDataDate일 때, 그 사이 date에 대해 wearerData => stats로 추가

    stats_qs = WearerStats.objects.order_by('nowDate').filter(
        user=wearer, nowDate__gt=yearAgo)
    data_qs = WearerData.objects.order_by('nowDate').filter(
        user=wearer, nowDate__gt=yearAgo, nowDate__lt=today)

    lastStatsDate = stats_qs.last().nowDate if len(
        stats_qs) != 0 else data_qs.first().nowDate - timedelta(days=1)
    # stats에 마지막으로 등록되어 있는 데이터 날짜

    lastDataDate = data_qs.last().nowDate
    # data에 당일 제외 마지막으로 등록되어 있는 데이터 날짜

    fillStats(wearer, lastStatsDate, lastDataDate)

    # SECTION 2-1: 7일 이전 wearerData는 삭제하기
    WearerData.objects.filter(user=wearer, nowDate__lte=weekAgo).delete()

    # SECTION 2-2: 1일 이전 heartPreEvent는 삭제하기
    HeatPreEvent.objects.filter(user=wearer, nowDate__lt=today).delete()

    # # SECTION 3: 1년 이전 stats 삭제
    WearerStats.objects.filter(user=wearer, nowDate__lte=yearAgo).delete()


def fillStats(wearer, stats_last, data_last):
    data_queryset = WearerData.objects.order_by(
        'nowDate').filter(user=wearer, nowDate__gt=stats_last, nowDate__lte=data_last)
    if len(data_queryset) == 0:
        return False
    else:
        saveStatDayValues(wearer, data_queryset)


def saveStatDayValues(wearer, data_queryset):
    '''
    EXPLANATION
    WearerData에서 각 날짜별로, 각 센서별 통계값 얻어서 WearerStats에 넣어주기

    INPUT
    data_queryset

    TIME
    O(len(data_queryset))

    OUTPUT
    returns True if successfully saved the instances in to the model WearerStats,
    else False
    '''
    pre_date = data_queryset.first().nowDate

    steps = 0
    he_dict = {'tot': 0, 'min': 10000, 'max': -10000}
    s_dict = {'tot': 0, 'min': 10000, 'max': -10000}
    t_dict = {'tot': 0, 'min': 10000, 'max': -10000}
    hu_dict = {'tot': 0, 'min': 10000, 'max': -10000}
    cnt = 0

    for data in data_queryset:
        cur_date = data.nowDate
        sc_list = [(he_dict, int(data.heartRate)), (s_dict, int(data.sound)),
                   (t_dict, int(data.temp)), (hu_dict, float(data.humid))]
        if cur_date != pre_date:
            # date가 달라지는 순간:
            # 저장

            if len(WearerStats.objects.filter(user=wearer, nowDate=pre_date)) == 0:
                # print(wearer.username, "nowDate=", pre_date, "step=", steps, "\nheartRate=",
                #       he_dict, "sound=", s_dict, "temp=", t_dict, "humid=", hu_dict)
                WearerStats.objects.create(user=wearer, nowDate=pre_date, stepCount=steps,
                                           heartRate_max=he_dict['max'], heartRate_avg=he_dict['tot']/cnt, heartRate_min=he_dict['min'],
                                           sound_max=s_dict['max'], sound_avg=s_dict['tot']/cnt, sound_min=s_dict['min'],
                                           temp_max=t_dict['max'], temp_avg=t_dict['tot']/cnt, temp_min=t_dict['min'],
                                           humid_max=hu_dict['max'], humid_avg=hu_dict['tot']/cnt, humid_min=hu_dict['min'])
            # 초기화
            steps = data.stepCount
            for dic, dat in sc_list:
                dic['max'] = dic['tot'] = dic['min'] = dat
            cnt = 1

        else:
            # date가 같을 때:
            # 업데이트
            steps = data.stepCount
            for dic, dat in sc_list:
                # 둘다 if로 한 이유: 가장 처음 날짜의 데이터가 딱 하나일 경우를 고려해서.
                if dic['max'] < dat:
                    dic['max'] = dat
                if dic['min'] > dat:
                    dic['min'] = dat
                dic['tot'] += dat
            cnt += 1
        pre_date = cur_date

    # 마지막 data 케어
    steps = data.stepCount
    # print(wearer.username, "nowDate=", pre_date, "step=", steps, "\nheartRate=",
    #   he_dict, "sound=", s_dict, "temp=", t_dict, "humid=", hu_dict)
    WearerStats.objects.create(user=wearer, nowDate=pre_date, stepCount=steps,
                               heartRate_max=he_dict['max'], heartRate_avg=he_dict['tot']/cnt, heartRate_min=he_dict['min'],
                               sound_max=s_dict['max'], sound_avg=s_dict['tot']/cnt, sound_min=s_dict['min'],
                               temp_max=t_dict['max'], temp_avg=t_dict['tot']/cnt, temp_min=t_dict['min'],
                               humid_max=hu_dict['max'], humid_avg=hu_dict['tot']/cnt, humid_min=hu_dict['min'])
    return True
