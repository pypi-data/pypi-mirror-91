#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Author         ：Kim
@Desc           ：活动基类
@PythonVersion  ：Python3.8.5
'''
import abc

class BaseActivity(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, inParams:dict):
        '''
        初始化传入参数
        :param inParams: 传入参数字典
        '''
        self.inParams = inParams
        self.__outParams = {}

    @abc.abstractmethod
    def doAction(self):
        '''
        活动运行逻辑
        :return:
        '''
        pass

    def setOutParams(self, name, value):
        '''
        设置输出参数
        :param name: 参数名
        :param value: 参数值
        :return:
        '''
        self.__outParams[name] = value

