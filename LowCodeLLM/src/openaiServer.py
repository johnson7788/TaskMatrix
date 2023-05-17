#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2023/5/17 14:47
# @File  : openaiServer.py
# @Author: 
# @Desc  : 调用openai的api
import requests
import json
def get_openai_response(prompt, context=None):
    """
    :return:
    :rtype:
    """
    one_data = {"prompt": prompt}
    if context:
        one_data["text"] = context
    data = [one_data]
    params = {'data': data}
    headers = {'content-type': 'application/json'}
    url = "http://mysig:4636/api/openai"
    r = requests.post(url, headers=headers, data=json.dumps(params), timeout=1200)
    result = r.json()
    if r.status_code == 200:
        print(f"返回结果: {result}")
        status = True
        assert len(result) == len(data), f"返回结果个数不正确, 期望个数: {len(data)}, 实际个数: {len(result)}"
    else:
        print(r.status_code)
        status = False
    return result,status