'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2021-01-06 08:29:18
LastEditors: xiaoshuyui
LastEditTime: 2021-01-12 10:51:08
'''
__version__ = '0.0.0'
__appname__ = 'DevTool'

import logging
import os
import platform
from functools import wraps
import traceback
import pickle
import sys
import time
import argparse

from concurrent_log_handler import ConcurrentRotatingFileHandler

__current_platform__ = platform.system()

del platform

BASE_DIR = os.path.abspath(os.curdir)
# print(BASE_DIR)

logit_logger = logging.getLogger(__appname__)
logit_logger.setLevel(level=logging.INFO)

if not os.path.exists(BASE_DIR + os.sep + "DevLog"):
    os.mkdir(BASE_DIR + os.sep + "DevLog")

LOG_PATH = BASE_DIR + os.sep + "DevLog" + os.sep + 'devlog.log'
Cache_path = BASE_DIR + os.sep + "DevLog" + os.sep + 'devCache.dump'

rHandler = ConcurrentRotatingFileHandler(filename=LOG_PATH,
                                         maxBytes=5 * 1024 * 1024,
                                         backupCount=5)
rHandler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rHandler.setFormatter(formatter)

logit_logger.addHandler(rHandler)


class BaseParser(object):
    def __init__(self, args: list, appname: str):
        """
        args type:list
        arg type:tuple
        arg example : ('-f','--force','force to show message even do not contain the module')
        """
        self.args = args
        self.appname = __appname__
        self.parser = argparse.ArgumentParser(
            description='{} is a small tool for python development'.format(
                self.appname))

    def get_parser(self):
        # pass
        return self.parser

    def add_parser(self, arg):
        pass


class FuncAndName:
    def __init__(self, funcName: str, func, info: str = ''):
        self.funcName = funcName
        self.func = func
        self.info = info

    def __hash__(self) -> int:
        return hash(self.funcName)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return False
        return self.funcName == o.funcName

    def __str__(self):
        return self.funcName


class FuncnameParamRes:
    def __init__(self, funcName: str, params: list, res: any):
        self.funcName = funcName
        self.params = params
        self.res = res

    def __hash__(self) -> int:
        return hash(self.funcName) + hash(self.params[0]) + hash(
            self.params[1])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return False
        return self.funcName == o.funcName and self.params[0] == o.params[
            0] and self.params[1] == o.params[1]

    def __str__(self):
        return self.funcName


def do_nothing():
    pass


def testWrapper(func):
    @wraps(func)
    def inner(*args, **kwargs):
        print('This is a test wrapper.')
        print(func.__annotations__)
        print(func.__qualname__)
        return func(*args, **kwargs)

    return inner


def setWrap(func):
    @wraps(func)
    def inner(*args, **kwargs):
        # print(func.__name__ + ' is cached.')
        func.__annotations__['wrapped_cached'] = True
        return func(*args, **kwargs)

    return inner


def infoDecorate(message: str = '', **infomation):
    def decorator(func):
        @setWrap
        @wraps(func)
        def sub_dec(*args, **kwargs):
            func.__annotations__[
                'message'] = message if message != '' else do_nothing

            if len(infomation) > 0:
                for k, v in infomation.items():
                    func.__annotations__[k] = v
            return func(*args, **kwargs)

        return sub_dec

    return decorator


def logit(**params):
    def decorator(func):
        @setWrap
        def execute(*args, **kwargs):
            flag = False
            save = params.get('save', False)
            load = params.get('load', False)
            ignore = params.get('ignore', False)
            if load and os.path.exists(Cache_path) and not ignore:
                with open(Cache_path, 'rb') as fi:
                    d = pickle.load(fi)
                    if func.__module__ + '.' + func.__name__ in d.keys():
                        fan = d[func.__module__ + '.' + func.__name__]
                        thisFan = FuncnameParamRes(func.__name__,
                                                   [args, kwargs], None)
                        if thisFan == fan:
                            # print('this == that')
                            return fan.res
                    else:
                        flag = True
            if not flag:
                try:
                    res = func(*args, **kwargs)
                    logit_logger.info(func.__module__ + '.' + func.__name__ +
                                      ' finishes successfully.')
                    fan = FuncnameParamRes(func.__name__, [args, kwargs], res)
                    if save:
                        d = dict()
                        # d[func.__module__ + '.' + func.__name__] = res
                        d[func.__module__ + '.' + func.__name__] = fan
                        if not os.path.exists(Cache_path):
                            with open(Cache_path, 'wb') as fi:
                                if sys.getsizeof(fan) < 1024:
                                    pickle.dump(d, fi)
                        else:
                            if sys.getsizeof(fan) < 1024:
                                with open(Cache_path, 'rb') as fi:
                                    d = pickle.load(fi)
                                with open(Cache_path, 'wb') as fi:
                                    d[func.__module__ + '.' +
                                      func.__name__] = fan
                                    pickle.dump(d, fi)

                except Exception:
                    logit_logger.error(func.__module__ + '.' + func.__name__ +
                                       " " + traceback.format_exc())
                    res = None
                return res

        return execute

    return decorator


def Test(*pas, **params):
    def decorator(func):
        @logit()
        def execute(*args, **kwargs):
            for k in params.keys():
                if k in kwargs.keys():
                    params.clear()
                    break
            if len(pas) == len(func.__code__.co_varnames):
                args = pas
            # print('.....' + str(func.__code__.co_varnames))
            if len(params) > 0:
                for k, v in params.items():
                    if k in func.__code__.co_varnames:
                        kwargs[k] = v
            # print(kwargs)
            if len(kwargs) > 0:
                count = 0
                for k in kwargs.keys():
                    if k in func.__code__.co_varnames:
                        count += 1
                if not count == len(func.__code__.co_varnames):
                    print("param number {} count not match {}.".format(
                        count, len(func.__code__.co_varnames)))
                    return
            return func(*args, **kwargs)

        return execute

    return decorator


def recTime(times: int = 1):
    if type(times) is not int:
        times = 1
    elif int(times) < 1:
        times = 1
    else:
        pass

    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            record = 0
            res = None
            # print(times)
            for _ in range(0, times):
                t1 = time.time()
                res = func(*args, **kwargs)
                record += time.time() - t1
            if times > 1:
                print('average run time:' + str(record / times))
            else:
                print('run time:' + str(record))
            return res

        return inner

    return decorator


def afterExec(beep=False, string=''):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            res = func(*args, **kwargs)
            if beep:
                if __current_platform__ == 'Windows':
                    import winsound
                    try:
                        winsound.Beep(523 * 2, 250)
                        winsound.Beep(988, 300)
                        winsound.Beep(523 * 2, 600)
                        winsound.Beep(880, 600)
                    except:
                        pass
                else:
                    print('Not support on {}.'.format(__current_platform__))

            if string != '':
                print(string)

            return res

        return inner

    return decorator


def beforeExec(beep=False, string=''):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):

            if beep:
                if __current_platform__ == 'Windows':
                    import winsound
                    try:
                        winsound.Beep(880, 250)
                        winsound.Beep(523 * 2, 600)
                        winsound.Beep(988, 300)
                        winsound.Beep(523 * 2, 600)
                    except:
                        pass
                else:
                    print('Not support on {}.'.format(__current_platform__))

            if string != '':
                print(string)

            return func(*args, **kwargs)

        return inner

    return decorator
