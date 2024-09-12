import json
import logging

import requests

logging.basicConfig(level=logging.DEBUG, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


def log_get(url, session=None):
    try:
        if session:
            resp = session.get(url=url)
        else:
            resp = requests.get(url=url)
        if resp.status_code in [200, 201, 202]:
            return json.loads(resp.text)
        else:
            logging.info(f"GET запрос на {url} закончен с кодом {resp.status_code}.")
            return False
    except ConnectionError as err:
        logging.error(f'Нет связи с сервером: {err}')
        return False


def log_post(url, json_=None, data=None, files=None):
    try:
        resp = requests.post(url=url, data=data, json=json_, files=files)
        if resp.status_code in [200, 201, 202]:
            return json.loads(resp.text)
        else:
            logging.info(f"POST запрос на {url} закончен с кодом {resp.status_code} и наполнением{json_}. "
                         f"Получен ответ: {resp.text}.")
            return False
    except ConnectionError as err:
        logging.error(f'Нет связи с сервером: {err}')
        return False


def log_put(url, json_=None, data=None, files=None):
    try:
        resp = requests.put(url=url, data=data, json=json_, files=files)
        if resp.status_code in [200, 201, 202]:
            return json.loads(resp.text)
        else:
            logging.info(f"POST запрос на {url} закончен с кодом {resp.status_code} и наполнением{json_}. "
                         f"Получен ответ: {resp.text}.")
            return 0
    except ConnectionError as err:
        logging.error(f'Нет связи с сервером: {err}')
        return 0


def log_patch(url, json_=None, data=None, files=None):
    try:
        resp = requests.patch(url=url, data=data, json=json_, files=files)
        if resp.status_code in [200, 201, 202, 203, 204, 205]:
            return json.loads(resp.text)
        else:
            logging.info(f"POST запрос на {url} закончен с кодом {resp.status_code} и наполнением{json_}. "
                         f"Получен ответ: {resp.text}.")
            return 0
    except ConnectionError as err:
        logging.error(f'Нет связи с сервером: {err}')
        return 0
