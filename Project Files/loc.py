#import geoip2.webservice
from ip2geotools.databases.noncommercial import DbIpCity

with open("loc.txt") as fp:
    while 1:
        IP=fp.readline()
        response = DbIpCity.get(IP.strip(), api_key='free')
        print(IP,response.city,response.latitude,response.longitude)
