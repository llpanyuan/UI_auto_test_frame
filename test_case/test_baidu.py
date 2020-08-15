#!/usr/bin/env python  
# -*- coding: utf-8 -*-
import logging
import os

import allure
import pytest
import yaml

from config.prj_conf import monitorweb, data_path
from page.baidu import BaiDu


class TestClass:
    data = yaml.safe_load(open(os.path.join(data_path, "baidu_data.yml")))
    def setup(self):
        logging.info("测试开始！")
        self.start = BaiDu()

    def teardown(self):
        self.start.close()
        logging.info("测试结束！")

    @monitorweb
    @allure.testcase(url="https://www.baidu.com" ,name="百度搜索功能测试")
    @pytest.mark.parametrize("text",["霍格沃兹测试学院"])
    def test_baidu(self,text):
        assert "百度一下" in self.start.search(text)
