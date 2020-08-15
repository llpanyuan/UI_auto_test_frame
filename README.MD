## ui_auto_frame

### 简介

**UI自动化测试框架使用pytest + selenium + allure搭建**

---

**整个框架主要分为三层，base_page层、page层、test_case层，采用传统的互联网的垂直架构模式。**

**元素公共操作方法封装存放在base_page层**

**页面元素操作存放在第二层page层，后面如果页面元素变化，直接在第二层相应的page对象修改即可**

**测试case存放在test_case层，主要做断言等操作**

---
### 模块设计
**data模块是存放测试数据的文件**

**page模块提取页面对象封装公共操作方法**

**test_case模块是存放测试用例的文件**

**test_report模块，存放测试报告，以及测试报告的生成模板allure**

**config模块是存放全局配置文件**

---
###环境说明：

**开发工具：pycharm**

**python版本：python3.8**

**测试case总入口：run.py**

**浏览器：Chrome**

**webdriver请选择对应Chrome版本的driver，并且放入项目所在的目录中**

---

### 环境搭建

- python安装:`version:3.8`  https://www.python.org
- java环境配置，`version 1.8`，win10系统中配置配置java环境，参考[win10java环境配置](https://www.runoob.com/w3cnote/windows10-java-setup.html)
- allure安装：
  - 不同平台安装allure的方法不同，这里仅介绍windows平台下allure的安装步骤。其它平台请阅读[allure官方文档](https://docs.qameta.io/allure/)进行操作
  - 官方提供的安装方法可能会受网络环境影响而安装失败，可选择在[GitHub仓库](https://github.com/allure-framework/allure2 )下载文件并安装allure2
  - Windows环境下可以用以下步骤进行安装
    - 安装scoop，使用**管理员权限**打开powershell窗口，输入命令`Invoke-Expression (New-Object System.Net.WebClient).DownloadString('https://get.scoop.sh')`
    - 如果安装不成功则运行`Set-ExecutionPolicy RemoteSigned -scope CurrentUser`，运行成功后重新执行第一步
    - scoop安装成功后控制台会输出`Scoop was installed successfully!`
    - 执行`scoop install allure`进行allure的安装
    - allure安装成功后控制台会输出`'allure' (2.13.1) was installed successfully!`
---
### 依赖包安装

**安装所需要的依赖包，使用pycharm导入项目，打开pycharm的terminal，只要到 requirements.txt 所在的目录下，使用如下命令 ，就能在当前的 python 环境中导入所有需要的依赖包：**

```
pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```



---
### allure装饰器使用

- @allure.severity("critical")
  - 优先级，包含blocker, critical, normal, minor, trivial几个不同的等级
    - 测试用例优先级1：blocker，中断缺陷（客户端程序无响应，无法执行下一步操作）
    - 测试用例优先级2：critical，临界缺陷（ 功能点缺失）
    - 测试用例优先级3：normal，普通缺陷（数值计算错误）
    - 测试用例优先级4：minor，次要缺陷（界面错误与UI需求不符）
    - 测试用例优先级5：trivial级别，轻微缺陷（必输项无提示，或者提示不规范）'
- @allure.feature("测试模块_demo1")
  - 功能块，feature功能分块时比story大,即同时存在feature和story时,feature为父节点
- @allure.story("测试模块_demo2")
  - 功能块，具有相同feature或story的用例将规整到相同模块下,执行时可用于筛选
- @allure.issue("BUG号：123")
  - 问题标识，关联标识已有的问题，可为一个url链接地址
- @allure.testcase("用例名：测试字符串相等")
  - 用例标识，关联标识用例，可为一个url链接地址

---


### 如何编写测试用例

下面详细说明如何添加一条用例，以登录界面演示

1、在page模块创建一个login.py

2、封装login页面操作元素对象

~~~ python
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

~~~



3、在test_case下面新建一个文件，例如test_baidu.py，测试登录页面

conftest.py为全局测试方法，供编写测试用例调用，如生成测试数据

~~~ python
import pytest
from faker import Faker


@pytest.fixture(scope='session')
def faker():
    faker = Faker(locale='zh_CN')
    return faker

~~~

test_baidu.py编写具体的测试用例内容，断言方法使用基本的assert即可
~~~ python
import logging
import os

import allure
import pytest
import yaml

from config.prj_conf import monitorweb, data_path
from page.baidu import BaiDu


class TestClass:
    def setup(self):
        logging.info("测试开始！")
        self.start = BaiDu()

    def teardown(self):
        self.start.close()
        logging.info("测试结束！")

    @monitorweb
    @allure.testcase(url="https://www.baidu.com" ,name="百度搜索功能测试")
    @pytest.mark.parametrize("text",yaml.safe_load(open(os.path.join(data_path,"baidu_data.yml"))))
    def test_baidu(self,text):
        assert "百度一下" in self.start.search(text)
~~~

4、执行用例

执行用例可以通过两种常用的方法进行

1. pycharm中配置`test runner`为`pytest`，配置路径为`settings->Tools->Python Integrated Tools->Testing`；配置完成后就能够在打开测试用例文件后看到可执行的按钮了
2. 在根目录下的`runner.py`文件中运行，需要配置要运行的`test_case_run`后就可以运行了。例如当你在调试`baidu`时只需要保证`test_case`中含有`baidu`就行了，`pytest`会自动寻找`testcase`下为`login`参数的用例

~~~ python
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
    run_test_case('chrome')
~~~

---

**有任何使用问题请联系我：pan.yuan**
