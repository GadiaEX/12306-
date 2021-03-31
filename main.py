from urllib import request
import re
import urllib
import http.cookiejar
import time
from urllib import parse

# 生成全局的cookie
c = http.cookiejar.LWPCookieJar()
cookie = urllib.request.HTTPCookieProcessor(c)
opener = urllib.request.build_opener(cookie)
urllib.request.install_opener(opener)


# 初始化，包括拿到验证用的cookie
def init():
    init_header = {
        'Host': 'kyfw.12306.cn',
        'Origin': 'https://kyfw.12306.cn',
        'Referer': 'https://kyfw.12306.cn/otn/resources/login.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    url = "https://www.12306.cn/index/otn/login/conf"
    init_request = request.Request(url, headers=init_header)
    response = opener.open(init_request)

    cookie_url = "https://kyfw.12306.cn/otn/resources/login.html"
    cookie_request = request.Request(cookie_url, headers=init_header)
    opener.open(cookie_request)

    # 模仿浏览器发的，我也不知道这东西是啥子
    cookie_request = request.Request("https://kyfw.12306.cn/otn/login/conf", headers=init_header)
    opener.open(cookie_request)

    # 添加验证header
    checkHeaer = {
        'Host': 'kyfw.12306.cn',
        'Origin': 'https://kyfw.12306.cn',
        'Referer': 'https://kyfw.12306.cn/otn/resources/login.html',
        'keep-alive': 'keep-alive'
    }

    # 检查登陆状态
    login_check_url = "https://kyfw.12306.cn/passport/web/auth/uamtk-static"
    login_data = {'appid': 'otn'}
    login_data = urllib.parse.urlencode(login_data).encode('ascii')

    login_check_request = request.Request(login_check_url, method='POST', data=login_data, headers=init_header)
    # login_check_request.add_header({'Host': 'kyfw.12306.cn'})
    response = opener.open(login_check_request)
    print(response.read())


# 验证码来的，懒得搞滑块，就是试验下而已
def getImg():
    # 首先获得时间戳
    current_time = str(time.time())
    current_time = current_time.replace('.', '')
    current_time = current_time[0:13]
    baseCheckUrl = "https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand&"
    baseCheckUrl += current_time
    return opener.open(baseCheckUrl)


def get_QR_Img():
    qr_url = "https://kyfw.12306.cn/passport/web/create-qr64"
    header = {
        'Host': 'kyfw.12306.cn',
        'Origin': 'https://kyfw.12306.cn',
        'Referer': 'https://kyfw.12306.cn/otn/resources/login.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    qr_data = {'appid': 'otn'}
    qr_data = urllib.parse.urlencode(qr_data).encode('ascii')

    qr_request = request.Request(url=qr_url, data=qr_data, method='POST', headers=header)
    response = opener.open(qr_request)
    return response


# 现在改为QR生成专用的了，如果还是要去生成验证码图的话，请修改re正则表达式
def decodeImg(code):
    # 拿到了code之后，首先解析出加密内容
    print(code)
    img_patt = re.compile(r'"image":"(.*?)","result_message')
    state_patt = re.compile(r'"result_code":"(.?)","uuid"')
    code = str(code)
    img_code = (img_patt.findall((code)))
    state_code = state_patt.findall(code)
    print("返回状态码为：" + state_code[0])
    img_url = img_code[0]
    # 解析完成后，解析并写入
    import base64
    img = base64.urlsafe_b64decode(img_url)
    fh = open("img.jpg", "wb")
    fh.write(img)
    fh.close()

    # 新增加内容，我们顺路把uuid一起提出来并且返回
    uuid_patt = re.compile(r'"uuid":"(.*?)"}')
    uuid = uuid_patt.findall(code)
    return uuid[0]

def check_login():
    pass



# 查询QR是否还有用
def QRquery(uuid):
    header = {
        'Host': 'kyfw.12306.cn',
        'Origin': 'https://kyfw.12306.cn',
        'Referer': 'https://kyfw.12306.cn/otn/resources/login.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'RAIL_DEVICEID': 'Vf0tGLvXMOOCaMXvnqTVqST_KmnHKn7olVsHN2zEmnaEkDV8UQevgdxf5sjbnyoqERcREU08uQZkixZzJ7ky8IBg0pe5Jl1kiyT8MM53vJ1fad8z-w5_EDzPmkR6X0tEEkjckDqJJAsqxkvp3kBxCbMt6m_cJQWH',
        'RAIL_EXPIRATION': '1617504858119'

    }
    check_url = "https://kyfw.12306.cn/passport/web/checkqr"
    data = {
        'RAIL_DEVICEID': 'Vf0tGLvXMOOCaMXvnqTVqST_KmnHKn7olVsHN2zEmnaEkDV8UQevgdxf5sjbnyoqERcREU08uQZkixZzJ7ky8IBg0pe5Jl1kiyT8MM53vJ1fad8z-w5_EDzPmkR6X0tEEkjckDqJJAsqxkvp3kBxCbMt6m_cJQWH',
        'RAIL_EXPIRATION': '1617504858119',
        'uuid': uuid,
        'appid': 'otn'
    }
    data = urllib.parse.urlencode(data).encode('ascii')
    check_request = request.Request(url=check_url, data=data, method='POST', headers=header)
    html = opener.open(check_request)
    print(html.read())


init()
response = get_QR_Img()
uuid = decodeImg(response.read())

import platform
import os

userPlatform = platform.system()

file = 'img.jpg'
os.startfile(file)

i = int(0)
while 1:
    QRquery(uuid)
    time.sleep(1)
    i += 1
    if i == 50:
        break
