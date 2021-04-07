from urllib import request
import urllib
import http.cookiejar
import json
# 生成全局的cookie
c = http.cookiejar.LWPCookieJar()
cookie = urllib.request.HTTPCookieProcessor(c)
opener = urllib.request.build_opener(cookie)
urllib.request.install_opener(opener)

header = {
    'Host': 'kyfw.12306.cn',
    'Origin': 'https://kyfw.12306.cn',
    'Referer': 'https://kyfw.12306.cn/otn/resources/login.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': '_uab_collina=159421192629070267972786; JSESSIONID=C0C93D41C28A3AC97655010034393203; RAIL_EXPIRATION=1617504858119; RAIL_DEVICEID=Vf0tGLvXMOOCaMXvnqTVqST_KmnHKn7olVsHN2zEmnaEkDV8UQevgdxf5sjbnyoqERcREU08uQZkixZzJ7ky8IBg0pe5Jl1kiyT8MM53vJ1fad8z-w5_EDzPmkR6X0tEEkjckDqJJAsqxkvp3kBxCbMt6m_cJQWH; BIGipServerotn=3973513482.50210.0000; BIGipServerpassport=954728714.50215.0000; route=6f50b51faa11b987e576cdb301e545c4'
}


def urlopen(url, headers=None, data=None, method='GET'):
    if headers is None:
        headers = header
    req = request.Request(url=url, data=data, headers=header, method=method)
    response = opener.open(req)
    return response


class Ticket:
    time = '2021-04-02'
    leftStation = 'SNQ'  # 韶关
    toStation = 'IZQ'  # 广州南
    tickKind = [
        '0X00',
        'ADULT'
    ]
    baseUrl = 'https://kyfw.12306.cn/otn/leftTicket/query'

    def getTicketUrl(self):
        finalUrl = self.baseUrl + '?leftTicketDTO.train_date=' + self.time + '&leftTicketDTO.from_station=' + self.leftStation + '&leftTicketDTO.to_station=' + self.toStation + '&purpose_codes=' + self.tickKind[1]
        return finalUrl



ticketInfo = Ticket()

response = urlopen(url=ticketInfo.getTicketUrl())
html = json.loads(response.read())
trainInfo =   html['data']['result']

''''
4:车次
5：车辆起始站
6：车辆终点站
7：本车票起始站点
8：本车票到站站点
9：出发时间
10:到站时间
11：历时
12：有票与否
13:
14:日期
31:二等座
32:一等座
33：商务
候补是哪个？



'''''
index = int(0)

for each in trainInfo:
    tempList = each.split('|')
    if(tempList[11] == 'Y'):
            print('车次为:' + tempList[3] +
                  '\t起始：:' + tempList[6] +
                  '\t到：' + tempList[7] +
                  '\t日期：' + tempList[13] +
                  '\t二等座数量：' + tempList[30] +
                  '\t一等座数量：' + tempList[31] )
            index+=1
    else:
        continue

print(index)