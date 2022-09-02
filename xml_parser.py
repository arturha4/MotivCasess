# -*- coding:utf-8 -*-
import time
import functools
from datetime import datetime as dt
import xml.etree.ElementTree as ET

import requests as requests
from tld import get_tld
import hashlib

from db import delete_table, create_table, create_web_sites_fast


def timefunc(func):
    @functools.wraps(func)
    def time_closure(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        time_elapsed = time.perf_counter() - start
        print(f"Function: {func.__name__}, Time: {time_elapsed}")
        return result

    return time_closure


def usd_course_from_cbr_xml_string(xml_string):
    tree = ET.ElementTree(ET.fromstring(xml_string))
    root = tree.getroot()
    for item in root.findall('Valute'):
        if item.attrib['ID'] == 'R01235':
            return item.find('Value').text


@timefunc
def get_uniq_dates() -> set:
    tree = ET.parse('dump.xml')
    root = tree.getroot()
    uniq_dates = []
    for date in root.findall('content'):
        date_string = date.attrib['includeTime']
        uniq_dates.append((dt.strptime(date_string, '%Y-%m-%dT%H:%M:%S').toordinal(), 89.89))
    return set(uniq_dates)


@timefunc
def parse_xml_to_json_with_generator():
    tree = ET.parse('dump.xml')
    root = tree.getroot()
    usd_courses = get_uniq_dates()
    return ((int(child.attrib['hash'], 16),
             dt.strptime(child.attrib['includeTime'], '%Y-%m-%dT%H:%M:%S'),
             89.89,
             'http://' + sub.text) for child in root.findall('content') for sub in child.findall('./domain')
            if (dt.strptime(child.attrib['includeTime'], '%Y-%m-%dT%H:%M:%S').toordinal(), 89.89) in usd_courses)


@timefunc
def test_generator():
    delete_table()
    create_table()
    create_web_sites_fast(parse_xml_to_json_with_generator)

test_generator()