#!/usr/bin/env python  
# -*- coding: utf-8 -*-
import os

from config.prj_conf import results_path, report_path, test_case_path


def run_test_case(browser):
    # 运行参数配置
    run_args = ' -sv --alluredir=' + results_path + ' '
    test_case_run = test_case_path + "/test_baidu.py"
    # 运行命令
    run_test_cases = "set browser=" + browser + '&&pytest' + run_args + test_case_run
    os.system(run_test_cases)
    # 生成测试报告
    make_test_report = 'allure generate ' + results_path + " -o " + report_path + ' --clean'
    os.system(make_test_report)
    os.system("echo 测试报告生成完毕，请前往test_report查看!")


if __name__ == '__main__':
    run_test_case('headless')
