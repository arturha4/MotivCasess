# -*- coding:utf-8 -*-
import time
import functools
from datetime import datetime as dt
import xml.etree.ElementTree as ET
from tldextract import extract
from server.db import delete_table, create_table, create_web_sites
from server.services import get_usd_by_date

def timefunc(func):
    @functools.wraps(func)
    def time_closure(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        time_elapsed = time.perf_counter() - start
        print(f"Function: {func.__name__}, Time: {time_elapsed}")
        return result

    return time_closure


@timefunc
def parse_xml_to_json_with_generator():
    tree = ET.parse('dump.xml')
    root = tree.getroot()
    print(test_uniq_domain_counter(root))
    usd_courses = dict(get_usd_by_date())
    return ((int(child.attrib['hash'], 16),
             dt.strptime(child.attrib['includeTime'], '%Y-%m-%dT%H:%M:%S'),
             float(usd_courses[dt.strptime(child.attrib['includeTime'], '%Y-%m-%dT%H:%M:%S').date().toordinal()]),
             'http://' + sub.text) for child in root.findall('content') for sub in child.findall('./domain'))

@timefunc
def test_uniq_domain_counter(root):
    res = []
    for child in root.findall('content'):
        for subchild in child.findall('./domain'):
            res.append(extract(subchild.text).domain)
    return len(set(res))

@timefunc
def test_generator():
    delete_table()
    create_table()
    create_web_sites(parse_xml_to_json_with_generator)
