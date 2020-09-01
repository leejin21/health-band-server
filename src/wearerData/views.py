from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.settings import api_settings

from rest_framework import status
from rest_framework.response import Response


from .models import WearerData
from .serializers import WearerDataSerializer

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
        serializer = WearerDataSerializer(data=request.data)
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

    time_filter_list = [datetime.now().date()-timedelta(days=i)
                        for i in range(6, -1, -1)]
    # queryset에 의하면
    queryset = WearerData.objects.filter(
        nowTime__in=time_filter_list).order_by('nowTime')

    serializer_class = WearerDataSerializer

    def list(self, request, *args, **kwargs):
        # SECTION original method
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # SECTION overrided code
        serializer = self.get_serializer(
            queryset.filter(user=self.request.user), many=True)

        return serializer
        # print(type(serializer.data[0]['nowTime']))
        # return Response(serializer.data)

    def getStatValueDict(self, sensorDataList, sensorName):
        '''
        get statistics values of sensorData,
        returns avg, min, max values of each day in sensorDataList

        sensorDataList: list of OrderedDict
        '''
        # statValues의 각 avg, min, max에 해당하는 val의 리스트 default값 어떻게 바꿀 지 고민하기
        statValues = {"avg": [-1]*7, "min": [-1]*7, "max": [-1]*7}
        # 변수 초기화(에러 방지)
        tot = 0
        cnt = 0
        minV = -100000
        maxV = 100000
        pre_diff = 6

        for i in range(len(sensorDataList)):
            # cur_diff: 날짜 표시
            str_date = sensorDataList[i]['nowTime'].split('T')[0]
            print(str_date)
            dt_date = datetime.strptime(str_date, "%Y-%m-%d").date()
            print(dt_date, str(datetime.now().date() - dt_date).split()[0][0])
            cur_diff = int(str(datetime.now().date() - dt_date).split()[0][0])
            cur_sens = int(sensorDataList[i][sensorName])
            if pre_diff != cur_diff:
                # 요일이 달라지는 순간 직전까지 구했던 통계값들 모두 저장
                # 저장
                statValues["avg"][pre_diff] = tot/cnt
                statValues["min"][pre_diff] = minV
                statValues["max"][pre_diff] = maxV
                # 초기화
                tot = cur_sens
                minV = cur_sens
                maxV = cur_sens
                cnt = 1
            else:
                tot += cur_sens
                if minV > cur_sens:
                    minV = cur_sens
                if maxV < cur_sens:
                    maxV = cur_sens
                cnt += 1
            pre_diff = cur_diff

        return statValues


class TempHumidSensorGetView(SensorGetView):

    def tempHumidList(self, request, *args, **kwargs):
        serializer = super().list(request, *args, **kwargs)

        response = Response(serializer.data)
        sensor_stats = dict()
        sensor_stats['temp'] = self.getStatValueDict(serializer.data, 'temp')
        sensor_stats['humid'] = self.getStatValueDict(serializer.data, 'humid')

        update_data = dict()
        for i in range(7):
            day = str(self.time_filter_list[i])
            update_data[day] = dict()
            for sensor in ['temp', 'humid']:
                update_data[day][sensor] = {
                    "avg": sensor_stats[sensor]['avg'][i],
                    "min": sensor_stats[sensor]['min'][i],
                    "max": sensor_stats[sensor]['max'][i],
                }

        print(update_data)
        # response.data.update(update_data)
        return Response(update_data)

    def get(self, request, *args, **kwargs):
        # overrided method: from ListAPIView
        return self.tempHumidList(request, *args, **kwargs)

        '''
        [OrderedDict([('nowTime', '2020-08-26T00:00:00'), ('temp', '20'), ('humid', '50'), ('heartRate', '30'), ('sound', '50'), ('stepCount', '2000')]),
        OrderedDict([('nowTime', '2020-08-26T00:00:00'), ('temp', '20'), ('humid',
                    '50'), ('heartRate', '20'), ('sound', '40'), ('stepCount', '1500')]),
        OrderedDict([('nowTime', '2020-08-27T00:00:00'), ('temp', '20'), ('humid',
                    '50'), ('heartRate', '30'), ('sound', '50'), ('stepCount', '2000')]),
        OrderedDict([('nowTime', '2020-08-28T00:00:00'), ('temp', '20'), ('humid',
                    '50'), ('heartRate', '30'), ('sound', '50'), ('stepCount', '2000')]),
        OrderedDict([('nowTime', '2020-08-29T00:00:00'), ('temp', '20'), ('humid',
                    '50'), ('heartRate', '30'), ('sound', '50'), ('stepCount', '2000')]),
        OrderedDict([('nowTime', '2020-08-30T00:00:00'), ('temp', '20'), ('humid',
                    '50'), ('heartRate', '30'), ('sound', '50'), ('stepCount', '2000')]),
        OrderedDict([('nowTime', '2020-08-31T00:00:00'), ('temp', '20'), ('humid',
                    '50'), ('heartRate', '30'), ('sound', '50'), ('stepCount', '2000')]),
        OrderedDict([('nowTime', '2020-09-01T00:00:00'), ('temp', '20'), ('humid',
                    '50'), ('heartRate', '30'), ('sound', '50'), ('stepCount', '2000')]),
        OrderedDict([('nowTime', '2020-09-01T00:00:00'), ('temp', '20'), ('humid', '50'), ('heartRate', '40'), ('sound', '60'), ('stepCount', '2500')])]

        '''
