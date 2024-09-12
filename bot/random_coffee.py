from data.config import REGION_FLAG
from db_responce import log_get


# TODO random coffee
async def rand_cof(tg_id: str):
    res = log_get(url=f'http://194.67.86.225/ru/api/students/detail-update/{tg_id}/')
    list_res = log_get(url='http://194.67.86.225/ru/api/students/list/')
    if res and list_res:
        ind_dict = \
            {
                'before_university': res[f'before_university_{REGION_FLAG}'],
                'university': res[f'university_{REGION_FLAG}'],
                'course': res[f'course_{REGION_FLAG}'],
                'interest_first': res[f'interest_first_{REGION_FLAG}'],
                'interest_second': res[f'interest_second_{REGION_FLAG}'],
                'interest_third': res[f'interest_third_{REGION_FLAG}']
            }
        result = []
        urls = [
            '',
        ]
        while result:
            pass
    else:
        return False
