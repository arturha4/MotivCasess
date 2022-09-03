import xml.etree.ElementTree as ET
from datetime import datetime as dt
import requests

from cfg import USD_UNICODE


def usd_course_from_cbr_xml_string(xml_string):
    tree = ET.ElementTree(ET.fromstring(xml_string))
    root = tree.getroot()
    for item in root.findall('Valute'):
        if item.attrib['ID'] == USD_UNICODE:
            return item.find('Value').text


def get_usd_by_date():
    res = []
    for i in get_uniq_dates():
        usd_course = try_to_get_usd_course(i)
        res.append(usd_course)
    return res


def get_uniq_dates() -> set:
    tree = ET.parse('dump.xml')
    root = tree.getroot()
    uniq_dates = []
    for date in root.findall('content'):
        date_string = date.attrib['includeTime']
        uniq_dates.append((dt.strptime(date_string, '%Y-%m-%dT%H:%M:%S').toordinal(), 89.89))
    return set(uniq_dates)


def try_to_get_usd_course(item):
    try:
        pair_daily = get_usd_from_usd_daily(item)
        return pair_daily
    except BaseException as e:
        pair_cbr = get_usd_from_cbr(item)
        return pair_cbr


def get_usd_from_usd_daily(date: tuple) -> tuple:
    try:
        parsed_date = str(dt.fromordinal(date[0])).split(' ')[0].split('-')
        usd_course = requests.get('https://www.cbr-xml-daily.ru/archive/{0}/{1}/{2}/daily_json.js'
                                  .format(parsed_date[0], parsed_date[1], parsed_date[2])).json()['Valute']['USD'][
            'Value']
        return (date[0], usd_course)
    except:
        return get_usd_from_cbr(date)


def get_usd_from_cbr(date: tuple) -> tuple:
    try:
        parsed_date = str(dt.fromordinal(date[0])).split(' ')[0].split('-')
        usd_course = requests.get('http://www.cbr.ru/scripts/XML_daily.asp?date_req={0}.{1}.{2}'
                                  .format(parsed_date[2], parsed_date[1], parsed_date[0]))
        if usd_course.status_code == 200:
            return (date[0], usd_course_from_cbr_xml_string(usd_course.text).replace(',','.'))
    except BaseException as e:
        return (date[0], 0.0)
