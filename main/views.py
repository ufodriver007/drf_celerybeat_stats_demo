from datetime import timedelta
from hashlib import sha256

from loguru import logger

from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from main.models import ParserCall
from parser import AvitoParser


logger.add('main.log', rotation='10mb', level='DEBUG')


class AddView(APIView):
    def post(self, request):
        """
        Получение связки регион + запрос, генерация UID и регистрация в БД
        :param request:
        :return:
        """
        phrase = request.data.get('phrase')
        region = request.data.get('region')

        if region not in AvitoParser.locations_dict:
            return Response({'region': 'Wrong region data'}, status=status.HTTP_400_BAD_REQUEST)

        uid = sha256(f'{phrase}{region}'.encode('utf-8')).hexdigest()

        try:
            if ParserCall.objects.filter(phrase_region_id=uid).exists():
                logger.error(f'UID: {uid} уже существует')
                return Response({'uid': 'uid already exists'}, status=status.HTTP_400_BAD_REQUEST)

            ParserCall(phrase_region_id=uid, phrase=phrase, region=region).save()
        except Exception as e:
            logger.error(f'Ошибка добавления в БД: {e}')
            return Response({'Error': 'Internal error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.info(f'Запись {uid} создана в БД')
        return Response({'uid': uid, 'phrase': phrase, 'region': region}, status=status.HTTP_201_CREATED)


class StatsView(APIView):
    def post(self, request):
        """
        Получение UID и интервала в часах и выдача записей БД(вызовов парсера с результатом)
        :param request:
        :return:
        """
        uid = request.data.get('uid')
        hours = request.data.get('hours')

        try:
            hours = int(hours)
            if hours < 1:
                raise ValueError
        except Exception as e:
            return Response({'interval': 'Wrong data! Needed hours in integer'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = ParserCall.objects.filter(phrase_region_id=uid,
                                             created_at__gte=timezone.now() - timedelta(hours=hours)).exclude(number_of_ads=None)

        result = {}
        for elem in queryset:
            result[str(elem.created_at)] = {
                'query': elem.phrase,
                'region': elem.region,
                'number_of_ads': elem.number_of_ads,
            }

        return Response(result, status=status.HTTP_200_OK)
