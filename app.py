from craigslist import CraigslistHousing as ch
import config
import smtplib
from datetime import datetime, timedelta

def minutes_between_now(d1):
    # ValueError: time data '2021-01-08 15:12' does not match format '%d/%m/%Y %H:%M:%S'
    cl_time_string = "%Y-%m-%d %H:%M"
    d1 = datetime.strptime(d1, cl_time_string)
    d2 = datetime.strptime(datetime.strftime(datetime.now(), cl_time_string), cl_time_string)
    return abs((d2 - d1))


def send_text(phone_number, msg):
    fromaddr = "Craigslist Checker"
    toaddrs = phone_number
    msg = ("From: {0}\r\nTo: {1}\r\n\r\n{2}").format(fromaddr, toaddrs, msg)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(config.settings['username'], config.settings['password'])
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


def check_listings(filters):
    cl_h = ch(site='sfbay', area='sfc', category='apa', filters=filters)

    for result in cl_h.get_results(sort_by='newest', geotagged=True):
        post_time = result['datetime']
        if (minutes_between_now(post_time)) < timedelta(seconds=660):
            msg = result['name'] + '\n' + result['price'] + '\n' + result['url']
            print(msg)
            send_text(config.settings['phone_1'], msg)
            send_text(config.settings['phone_2'], msg)


zip_code = 94123
filters = {
    'posted_today': True
    ,'min_price': 4000
    ,'max_price': 6000
    ,'min_bedrooms': 2
    ,'min_bathrooms': 1
    ,'laundry': {'w/d in unit', 'w/d hookups'}
    ,'parking': {'attached garage', 'detached garage', 'carport', 'off-street parking'}
    , 'zip_code': zip_code
    , 'search_distance': 1
}

check_listings(filters)

zip_code = 94117
filters = {
    'posted_today': True
    ,'min_price': 4000
    ,'max_price': 6000
    ,'min_bedrooms': 2
    ,'min_bathrooms': 1
    ,'laundry': {'w/d in unit', 'w/d hookups'}
    ,'parking': {'attached garage', 'detached garage', 'carport', 'off-street parking'}
    , 'zip_code': zip_code
    , 'search_distance': 1
}

check_listings(filters)
