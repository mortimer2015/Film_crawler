# -*- coding: utf-8 -*-
# author: hunter
import requests
from apps import settings


def send_text(text, to=settings.DINGTALK_TOKEN):
    url = 'https://oapi.dingtalk.com/robot/send?access_token={}'.format(to)

    message_content = {
        "msgtype": "text",
        "text": {
            "content": text,
        }
    }
    requests.post(url, json=message_content)
