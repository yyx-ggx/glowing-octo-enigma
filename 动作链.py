from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from lxml import etree
from selenium.webdriver import ActionChains

url = 'https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
bro = webdriver.Chrome()
bro.get(url)
sleep(1)
#通过find定位，标签在iframe下，会定位失败，使用switch to
bro.switch_to.frame('iframeResult')
div_tag = bro.find_element(By.XPATH,'//*[@id="draggable"]')
#对div_tag滑动
action = ActionChains(bro)
action.click_and_hold(div_tag)#点击且长按

for i in range(6):
    action.move_by_offset(20,30).perform()
    sleep(1)