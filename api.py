from datetime import datetime as dt

import requests

from xml_parser import get_usd_course_from_xml_string, get_uniq_dates


def get_usd_by_date(dates):
    res = []
    for i in dates:
        try:
            pair = get_usd_from_cbr(i)
            res.append(pair)
        except BaseException as e:
            print(e)
    return res


def get_usd_from_usd_daily(date):
    try:
        parsed_date = str(dt.fromordinal(date[0])).split(' ')[0].split('-')
        usd_course = requests.get('https://www.cbr-xml-daily.ru/archive/{0}/{1}/{2}/daily_json.js'
                                  .format(parsed_date[0], parsed_date[1], parsed_date[2])).json()['Valute']['USD'][
            'Value']
        return (date, usd_course)
    except:
        print(date)


def get_usd_from_cbr(date):
    try:
        parsed_date = str(dt.fromordinal(date[0])).split(' ')[0].split('-')
        usd_course = requests.get('http://www.cbr.ru/scripts/XML_daily.asp?date_req={0}.{1}.{2}'
                                  .format(parsed_date[2], parsed_date[1], parsed_date[0]))
        if usd_course.status_code == 200:
            return (date[0],get_usd_course_from_xml_string(usd_course.text))
    except BaseException as e:
        print(date, e)


# usd_course = requests.get('http://www.cbr.ru/scripts/XML_daily.asp?date_req=12.08.2012')
# print(usd_course.status_code, usd_course.text)
