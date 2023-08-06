'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2021-01-08 09:27:04
LastEditors: xiaoshuyui
LastEditTime: 2021-01-08 10:08:52
'''
import re
import datetime

def match_datetime(text):
    '''正则表达式提取文本所有日期+时间

    :param text: 待检索文本

    >>> match_datetime('日期是2020-05-20 13:14:15.477062.')
    ['2020-05-20 13:14:15']
    '''
    pattern = r'(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})'
    pattern = re.compile(pattern)
    result = pattern.findall(text)
    return result


def validate_datetime(text):
    '''验证日期+时间格式

    :param text: 待检索文本

    >>> validate_datetime('2020-05-20 13:14:15')
    True
    >>> validate_datetime('2020-05-32 13:14:15')
    False
    '''
    try:
        if text != datetime.datetime.strptime(text, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'):
            raise ValueError
        return True
    except ValueError:
        return False


def validate_date(text):
    '''验证日期+时间格式

    :param text: 待检索文本

    >>> validate_date('2020-05-20')
    True
    >>> validate_date('2020-05-32')
    False
    '''
    try:
        if text != datetime.datetime.strptime(text, '%Y-%m-%d').strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False