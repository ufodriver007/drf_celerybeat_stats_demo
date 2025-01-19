from typing import Union

from loguru import logger

from AvitoStats.celery_app import app
from parser import AvitoParser
from main.models import ParserCall


@app.task()
def periodic_parsing() -> int:
    """
    Задача, которая запускает парсинг всех уникальных запросов в БД(локация + запрос)
    :return: Количество уникальных запросов
    """
    queryset = ParserCall.objects.all().distinct('phrase_region_id')
    unique_queries: int = len(queryset)
    logger.info(f'Уникальных запросов {unique_queries}')

    for elem in queryset:
        start_parser.delay(uid=elem.phrase_region_id, region=elem.region, phrase=elem.phrase)

    return unique_queries


@app.task()
def start_parser(uid: str, region: str, phrase: str) -> Union[str, None]:
    """
    Парсинг информации по одному запросу
    :param uid: Уникальный идентификатор запроса
    :param region: Локация в которой будет производится поиск. Полный список в AvitoParser.locations_dict
    :param phrase: Сам запрос
    :return: Количество объявлений найденных по запросу или None
    """
    parser = AvitoParser()
    try:
        number_of_ads = parser.parse(region, phrase)
        ParserCall(phrase_region_id=uid, phrase=phrase, region=region, number_of_ads=number_of_ads).save()
    except Exception as e:
        logger.error(f'Ошибка при выполнении задачи: {e}')
        number_of_ads = None

    return number_of_ads
