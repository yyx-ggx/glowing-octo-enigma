from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from lxml import etree

url = 'https://movie.douban.com/top250'
bro = webdriver.Chrome()
bro.get(url)
page_text_list = []
sleep(2)
#捕获页面数据
page_text = bro.page_source #返回全部编码数据
#第一页数据放到列表里面
page_text_list.append(page_text)
sleep(2)
#点击下一页
for i in range(2):
    next_page = bro.find_element(By.XPATH,'//*[@id="content"]/div/div[1]/div[2]/span[3]/a')
    next_page.click()
    sleep(2)
    page_text_list.append(bro.page_source)

for page_text in page_text_list:
    tree = etree.HTML(page_text)
    li_list = tree.xpath('//*[@id="content"]/div/div[1]/ol/li')
    for li in li_list:
        name = li.xpath('.//span[@class="title"]/text()')[0]
        print(name)
sleep(2)
bro.quit()

    