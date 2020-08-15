#!/usr/bin/env python  
# -*- coding: utf-8 -*-
import logging
import os
from functools import wraps
from time import sleep

import allure
import yaml
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config.prj_conf import chromedriver_path, geckodriver_path,phantom_js_path


# 异常处理装饰器
def exception_handle(fun):
    def magic(*args, **kwargs):
        instance: BasePage = args[0]
        try:
            result = fun(*args, **kwargs)
            instance._retry = 0
            return result
        except Exception as e:
            instance._retry += 1
            if instance._retry > instance._retry_max:
                raise e
            instance._driver.implicitly_wait(0)
            for e in instance._black_list:
                elements = instance._driver.find_elements(*e)
                if len(elements) > 0:
                    elements[0].click()
                    instance._driver.implicitly_wait(10)
                    return fun(*args, **kwargs)

    return magic


class BasePage:
    _driver: WebDriver
    _params = {}
    _error_max = 10
    _error_count = 0
    _black_list = []
    _retry_max = 3
    _retry = 0

    def __init__(self, driver: WebDriver = None):
        browser = os.getenv("browser").lower()
        if driver is None:
            logging.info("开始初始化web driver")
            if browser == "headless":
                self._driver = webdriver.PhantomJS(executable_path=phantom_js_path)
            elif browser == "firefox":
                self._driver = webdriver.Firefox(executable_path=geckodriver_path)
            else:
                options = webdriver.ChromeOptions()
                options.debugger_address = "127.0.0.1:9222"
                self._driver = webdriver.Chrome(executable_path=chromedriver_path)
                self._driver.implicitly_wait(2)
            logging.info("web driver初始化完成，测试使用浏览器为：{}".format(browser))
        else:
            self._driver = driver
        self.action = ActionChains(self._driver)

    # 测试步骤驱动
    def steps(self, path):
        with open(path) as f:
            steps: list[dict] = yaml.safe_load(f)
            element: WebElement = None
            for step in steps:
                logging.info(step)
                if "by" in step.keys():
                    element = self.find(step["by"], step["value"])
                if "action" in step.keys():
                    action = step["action"]
                    if action == "find":
                        pass
                    elif action == "click":
                        element.click()
                    elif action == "text":
                        element.text()
                    elif action == "attribute":
                        element.get_attribute(step["value"])
                    elif action in ["send", "input"]:
                        content: str = step["value"]
                        for key in self._params.keys():
                            content = content.replace("{%s}" % key, self._params[key])
                        element.send_keys(content)

    def find(self, by, value: str = None):
        """
        定位单个元素
        :param by:
        :param value:
        :return:
        """
        logging.info("定位元素({},{})".format(by,value))
        try:
            element = self._driver.find_element(*by) \
                if isinstance(by, tuple) else self._driver.find_element(by, value)
            self._error_count = 0
            return element
        except Exception as e:
            if self._error_count > self._error_max:
                raise e
            self._error_count += 1
            for element in self._black_list:
                logging.info(element)
                elements = self._driver.find_elements(*element)
                if len(elements) > 0:
                    elements[0].click()
                    return self.find(by, value)
                logging.error("black list no one found")
                raise e

    def finds(self, value, by=By.CSS_SELECTOR):
        """
        定位多个元素
        :param by:
        :param value:
        :return:
        """
        return self._driver.find_elements(by, value)

    def wait(self, value, by=By.CSS_SELECTOR, timeout=5):
        element = self.find(by, value)
        WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located(element))

    def send_keys(self, value, text, by=By.CSS_SELECTOR):
        """
        输入文本
        :param value:
        :param text:
        :param by:
        :return:
        """
        element = self.find(by, value)
        element.clear()
        element.send_keys(text)
        logging.info("输入文本：{}".format(text))

    def click(self, value, by=By.CSS_SELECTOR):
        """
        点击元素
        :param value:
        :param by:
        :return:
        """
        self.find(by, value).click()
        logging.info("点击元素：({},{})".format(by,value))

    def clear(self, value, by=By.CSS_SELECTOR):
        """
        清除内容
        :param value:
        :param by:
        :return:
        """
        self.find(by, value).clear()

    def close(self):
        """
        关闭标签页
        :return:
        """
        sleep(3)
        self._driver.close()
        logging.info("关闭标签页")

    def quit(self):
        """
        关闭浏览器
        :return:
        """
        sleep(3)
        self._driver.quit()
        logging.info("关闭浏览器")

    def open(self, url):
        """
        打开浏览器
        :param url:
        :return:
        """
        self._driver.get(url)
        logging.info("打开测试目标网页：{}".format(url))

    def get_attribute(self, name, value, by=By.CSS_SELECTOR):
        """
        获取元素属性
        :param method:
        :param value:
        :param by:
        :return:
        """
        self.find(by, value).get_attribute(name)
        logging.info('获取元素"{}"属性'.format(name))


    def get_location_and_size(self, value, by=By.CSS_SELECTOR):
        """
        获取元素坐标
        :param value:
        :param by:
        :return:
        """
        location = self.find(by, value).location
        size = self.find(by, value).size
        print("location:{}\nsize:{}".format(location, size))
        return location, size

    def get_page_source(self):
        """
        获取网页源代码
        :return:
        """
        logging.info("获取网页源代码")
        return self._driver.page_source

    def refresh(self):
        """
        刷新页面
        :return:
        """
        self._driver.refresh()
        logging.info("刷新网页")

    def set_window_size(self, width, height):
        """
        设置窗口大小
        :param width:
        :param height:
        :return:
        """
        self._driver.set_window_size(width, height)

    def minimize_window(self):
        """
        最小化窗口
        :return:
        """
        self._driver.minimize_window()
        logging.info("最小化窗口")

    def maximize_window(self):
        """
        最大化窗口
        :return:
        """
        self._driver.maximize_window()
        logging.info("最大化窗口")

    def click_and_hold(self, value, by=By.CSS_SELECTOR):
        on_element = (by, value)
        self.action.click_and_hold(on_element).perform()

    def context_click(self, value, by=By.CSS_SELECTOR):
        on_element = (by, value)
        self.action.context_click(on_element).perform()

    def double_click(self, value, by=By.CSS_SELECTOR):
        pass

    def drag_and_drop(self, source, target):
        pass

    def drag_and_drop_by_offset(self, source, xoffset, yoffset):
        pass

    def key_down(self, key_name, value, by=By.CSS_SELECTOR):
        pass

    def move_by_offset(self, xoffset, yoffset):
        pass

    def move_to_element(self, value, by=By.CSS_SELECTOR):
        pass

    def move_to_element_with_offset(self, value, xoffset, yoffset, by=By.CSS_SELECTOR):
        pass

    def release(self, value, by=By.CSS_SELECTOR):
        pass

    def switch_to_frame(self, value):
        self._driver.switch_to.frame(value)

    def switch_to_default_content(self):
        self._driver.switch_to.default_content()

    def switch_to_parent_frame(self):
        self._driver.switch_to.parent_frame()

    def get_window_handles(self):
        handles = self._driver.window_handles
        return handles

    def switch_to_window(self, window_name):
        self._driver.switch_to.window(window_name)

    def execute_script(self, script, *args):
        self._driver.execute_script(script, *args)

    def switch_to_alert(self):
        return self._driver.switch_to.alert

    def switch_to(self):
        return self._driver.switch_to



