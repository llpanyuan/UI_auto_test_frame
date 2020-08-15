#!/usr/bin/env python  
# -*- coding: utf-8 -*-
import pytest
from faker import Faker

@pytest.fixture(scope='session')
def faker():
    faker = Faker(locale='zh_CN')
    return faker