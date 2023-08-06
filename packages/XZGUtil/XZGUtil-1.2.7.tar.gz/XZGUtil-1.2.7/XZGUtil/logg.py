#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @XZGUtil    : 2021-01-09 19:36
# @Site    : 
# @File    : logg.py
# @Software: PyCharm
"""
装饰器
说明：
前景色            背景色           颜色
---------------------------------------
30                40              黑色
31                41              红色
32                42              绿色
33                43              黃色
34                44              蓝色
35                45              紫红色
36                46              青蓝色
37                47              白色
显示方式           意义
-------------------------
0                终端默认设置
1                高亮显示
4                使用下划线
5                闪烁
7                反白显示
8                不可见
"""
import asyncio
import datetime
import random
from functools import wraps
import time
from loguru import logger

def logit(func):
    """
    日志输出
    :param func:
    :return:
    """
    @wraps(func)
    def with_logging(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        logger.info(f'\033[1;30m 耗时:{"%.4f" %(t2 - t1)}秒\033[0m - \033[1;32m{result}\033[0m')
        return result
    return with_logging

def async_logit(func):
    @wraps(func)
    async def with_logging(*args, **kwargs):
        t1 = time.time()
        result =await func(*args, **kwargs)
        t2 = time.time()
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f'\033[1;30m 耗时:{"%.4f" %(t2 - t1)}秒\033[0m - \033[1;32m{result}\033[0m')
        return result
    return with_logging

#demo:
# @async_logit
# async def test():
#     return 6666
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(test())
