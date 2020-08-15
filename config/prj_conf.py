#!/usr/bin/env python  
# -*- coding: utf-8 -*-
import datetime
import logging
import os

import allure
from functools import wraps

# 项目绝对路径

prj_path = os.path.abspath(
    os.path.dirname(os.path.abspath(os.path.split(os.path.abspath(os.path.realpath(__file__)))[0])))

# 测试报告
results_path = os.path.join(prj_path, "test_report", "results")
report_path = os.path.join(prj_path, "test_report", "report")

# data
data_path = os.path.join(prj_path, "data")

# 测试用例
test_case_path = os.path.join(prj_path, "test_case")

# driver
chromedriver_path = os.path.join(prj_path, "chromedriver.exe")
geckodriver_path = os.path.join(prj_path, "geckodriver.exe")
phantom_js_path = os.path.join(prj_path, "phantomjs.exe")

# 验证码存放地址
screenImg_path = os.path.join(prj_path, "config")


def monitorweb(function):
    @wraps(function)
    def get_ErrImage(self, *args, **kwargs):
        try:
            allure.dynamic.description('用例开始时间:{}'.format(datetime.datetime.now()))
            function(self, *args, **kwargs)
            s = self.start._driver.get_screenshot_as_png()
            allure.attach(s, '用例执行成功截图', allure.attachment_type.PNG)
            weblog = self.start._driver.get_log('browser')
            c = '\n'.join([i['message'] for i in weblog])
            allure.attach(c, '浏览器控制台日志', allure.attachment_type.TEXT)
        except Exception as e:
            f = self.start._driver.get_screenshot_as_png()
            allure.attach(f, '用例执行失败截图', allure.attachment_type.PNG)
            weblog = self.start._driver.get_log('browser')
            c = '\n'.join([i['message'] for i in weblog])
            allure.attach(c, '浏览器控制台日志', allure.attachment_type.TEXT)
            raise e
        else:
            logging.info(" %s 脚本运行正常" %
                         (function.__name__)
                         )

    return get_ErrImage

