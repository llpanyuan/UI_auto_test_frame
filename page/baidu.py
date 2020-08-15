#!/usr/bin/env python  
# -*- coding: utf-8 -*-
import logging

from page.base_page import BasePage


class BaiDu(BasePage):

    def search(self,text):
        self.open("https://www.baidu.com")
        self.send_keys("#kw",text)
        print(text)
        self.click('#su')
        title = self._driver.title
        logging.info("网页标题为：{}".format(title))
        return title