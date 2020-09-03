from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.settings import api_settings

from rest_framework import status
from rest_framework.response import Response


from .models import WearerData, WearerEvent
from .serializers import WearerDataSerializer, WearerEventSerializer

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


class SensorGetView(ListAPIView):
    '''
    parent class of
    TempHumidSensorGetView,
    HeartRateSensorGetView,
    SoundSensorGetView,
    StepCountGetView.

    '''
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    recent7days = [datetime.now().date()-timedelta(days=i)
                   for i in range(6, -1, -1)]
    queryset = WearerData.objects.filter(
        nowDate__in=recent7days).order_by('nowDate')

    serializer_class = WearerDataSerializer

    def list(self, request, *args, **kwargs):
        # SECTION original method
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # SECTION overrided code

        # 오름차순으로 6일 전부터 오늘까지
        # print(self.recent7days)

        queryset = queryset.filter(user=self.request.user)
        serializer = self.get_serializer(queryset, many=True)

        # unlike the original code(which returns response), this method returns serializer
        return serializer

    def getDate(self, i, sensorDataList):
        # cur_diff: 현재 날짜와 며칠 차이 나는 지

        str_date = sensorDataList[i]['nowDate']
        dt_date = datetime.strptime(str_date, "%Y-%m-%d").date()
        cur_diff = int(str(datetime.now().date() - dt_date).split()[0][0])
        return cur_diff

    def getStatValueDict(self, sensorDataList, sensorName):
        '''
        EXPLANATION
        get statistics values of sensorData

        INPUT
        sensorDataList: list of OrderedDict

        TIME
        time complexity: O(n), where n = len(sensorDataList)

        OUTPUT
        returns avg, min, max values of each day in sensorDataList
        '''
        # statValues의 각 avg, min, max에 해당하는 val의 리스트 default값 어떻게 바꿀 지 고민하기
        # statValues 0자리=6일전, 1자리=5일전, ...
        statValues = {"avg": [-1]*7, "min": [-1]*7, "max": [-1]*7}
        # 변수 초기화(에러 방지)
        tot = cnt = 0
        minV, maxV = 100000, -100000
        pre_diff = 6        # 오름차순 때문
        # print(sensorDataList)

        for i in range(len(sensorDataList)):
            cur_diff = self.getDate(i, sensorDataList)
            # 오름차순: sensorDataList가 오름차순으로 정렬되었기 때문
            cur_sens = int(sensorDataList[i][sensorName])
            if pre_diff != cur_diff:
                # 요일이 달라지는 순간
                # 저장
                statValues["avg"][pre_diff] = tot/cnt
                statValues["min"][pre_diff] = minV
                statValues["max"][pre_diff] = maxV
                # 초기화
                tot = minV = maxV = cur_sens
                cnt = 1
            else:
                # 요일이 같을 때: tot, minV, maxV 업데이트
                tot += cur_sens
                if minV > cur_sens:
                    minV = cur_sens
                if maxV < cur_sens:
                    maxV = cur_sens
                cnt += 1
            pre_diff = cur_diff
        # 마지막 날짜 케어해주기
        statValues["avg"][pre_diff] = tot/cnt
        statValues["min"][pre_diff] = minV
        statValues["max"][pre_diff] = maxV

        return statValues

    def sensorList(self, sensorDataList, *sensorName):
        '''
        EXPLANATION
        get each sensors' statistic values(min, max, avg) by dict form.
        sensor stepCount is an exception.

        INPUT
        sensorDataList: list of OrderedDict
        sensorName: tuple of str, ex) 'temp', 'humid'

        TIME
        time complexity: O(n*m),
        where n = len(sensorName), m = len(sensorDataList)

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
        sensor_stats = dict()
        for sensor in sensorName:
            sensor_stats[sensor] = self.getStatValueDict(
                sensorDataList, sensor)
        update_data = dict()
        for i in range(7):
            day = str(self.recent7days[i])
            update_data[day] = dict()
            for sensor in sensorName:
                update_data[day][sensor] = {
                    # i=0일때 6일차이이므로 리스트에서는 6일차일때 값 뽑아오기
                    "avg": sensor_stats[sensor]['avg'][6-i],
                    "min": sensor_stats[sensor]['min'][6-i],
                    "max": sensor_stats[sensor]['max'][6-i],
                }

        return update_data


class TempHumidSensorGetView(SensorGetView):

    def tempHumidList(self, request, *args, **kwargs):
        serializer = super().list(request, *args, **kwargs)
        update_data = self.sensorList(serializer.data, 'temp', 'humid')
        # response.data.update(update_data)
        return Response(update_data)

    def get(self, request, *args, **kwargs):
        # overrided method: from ListAPIView
        return self.tempHumidList(request, *args, **kwargs)


class HeartSensorGetView(SensorGetView):

    def heartRateList(self, request, *args, **kwargs):
        serializer = super().list(request, *args, **kwargs)
        update_data = self.sensorList(serializer.data, 'heartRate')
        # response.data.update(update_data)
        return Response(update_data)

    def get(self, request, *args, **kwargs):
        # overrided method: from ListAPIView
        return self.heartRateList(request, *args, **kwargs)


class SoundSensorGetView(SensorGetView):

    def soundList(self, request, *args, **kwargs):
        serializer = super().list(request, *args, **kwargs)
        update_data = self.sensorList(serializer.data, 'sound')
        # response.data.update(update_data)
        return Response(update_data)

    def get(self, request, *args, **kwargs):
        # overrided method: from ListAPIView
        return self.soundList(request, *args, **kwargs)


class StepCountSensorGetView(SensorGetView):

    def stepCountList(self, request, *args, **kwargs):
        '''
        EXPLANATION
        Figures out when the day changes and updates the final sensor value to the list "steps".
        Gets step values by dictionary as following form
        {
            "stepCount": {
                "day": value
            }
        }


        TIME
        O(n), where n = len(serializer.data)

        OUTPUT
        returns Response which includes the dict data which was mentioned before
        '''
        serializer = super().list(request, *args, **kwargs)
        pre_diff = 6
        steps = [-1]*7
        daystep = 0
        for i in range(len(serializer.data)):

            cur_diff = self.getDate(i, serializer.data)
            cur_sens = int(serializer.data[i]["stepCount"])

            if pre_diff != cur_diff:
                # 요일이 달라지는 순간
                steps[pre_diff] = daystep

            # 초기화 or 업데이트
            daystep = cur_sens
            # 다음 i의 요일이 다른 요일인 지 체크
            pre_diff = cur_diff

        # 마지막 날짜 케어해주기
        steps[pre_diff] = daystep

        update_data = {
            "stepCount": {str(self.recent7days[i]): steps[6-i] for i in range(7)}
        }

        # response.data.update(update_data)
        return Response(update_data)

    def get(self, request, *args, **kwargs):
        # overrided method: from ListAPIView
        return self.stepCountList(request, *args, **kwargs)


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
        print("done is_valid")
        self.perform_create(serializer)
        print("done perform_create")
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
        print(self.request.user)
        serializer.save(user=self.request.user)
