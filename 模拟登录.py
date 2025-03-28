#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5

class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def PostPic_base64(self, base64_str, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
            'file_base64':base64_str
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()

def tranImgCode(imgPath,imgType):
    chaojiying = Chaojiying_Client('yyxggx', 'A123456a.', '968634')
    im = open(imgPath, 'rb').read()
    return chaojiying.PostPic(im, imgType)['pic_str']


import requests
from lxml import etree

session = requests.Session()
url = 'https://www.gushiwen.cn/user/login.aspx?from=http://www.gushiwen.cn/user/collect.aspx'
headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36 Edg/134.0.0.0'
}
page_text = session.get(url=url, headers=headers).text
tree = etree.HTML(page_text)  # 解析验证码图片地址
img_src = 'https://www.gushiwen.cn/' + tree.xpath('//*[@id="imgCode"]/@src')[0]
# 保存验证码到本地
img_data = session.get(img_src, headers=headers).content
with open('./pic.jpg', 'wb') as fp:
    fp.write(img_data)
pic_text = tranImgCode('./pic.jpg', 1902)

logic_url = 'https://www.gushiwen.cn/user/login.aspx?from=http%3a%2f%2fwww.gushiwen.cn%2fuser%2fcollect.aspx'
data = {
    '__VIEWSTATE': ' VvEG+y2KwVG3p+VBA2zE2rOWY0DV7J2+P3jo1J7sp6hPnonRf1YLR7fNcDuM4vqfrH6wlpiTugVkMukmbCYItov1qLbSrs4g5kZDwpo3+hWcOzwgUVHYPqNd/2DQqhOJpOGLHmosfgpBAHKpRPomBzIE9n8=',
    '__VIEWSTATEGENERATOR': ' C93BE1AE',
    'from': 'http://www.gushiwen.cn/user/collect.aspx',
    'email': '15738357871',
    'pwd': 'A123456a.',
    'code': pic_text,  # 动态变化
    'denglu': '登录',
}
page_text_logic = session.post(url=logic_url, headers=headers, data=data).text  # 对点击按钮发送请求
with open('./gushiwen.html', 'w', encoding='utf-8') as f:
    f.write(page_text_logic)