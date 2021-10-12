
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time
from pymongo import MongoClient

driver = webdriver.Chrome()   # название нашего браузера
url = 'https://e.mail.ru'
driver.get(url)

wait = WebDriverWait(driver, 10)
username = wait.until(EC.presence_of_element_located((By.NAME, 'username')))

username.send_keys('study.ai_172')

username.send_keys(Keys.ENTER)


wait = WebDriverWait(driver, 10)
password = wait.until(EC.element_to_be_clickable((By.NAME, 'password')))
password.send_keys('NextPassword172???')
password.send_keys(Keys.ENTER)

time.sleep(3)

link_set = set()
new_round = True
while new_round:
    letters_list = driver.find_elements(By.XPATH,'//div[@class="dataset__items"]/a')
    for letter in letters_list:
        letter_link = letter.get_attribute('href')
        if letter_link is None:
            new_round = False
        else:
            link_set.add(letter_link)

    actions = ActionChains(driver)
    actions.move_to_element(letters_list[-1])
    actions.perform()



all_mails = []
for link in link_set:
    mail = {}
    driver.get(link)
    text = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'letter__body'))).text
    contact = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'letter-contact'))).text
    thread = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'thread__subject'))).text
    date = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'letter__date'))).text

    mail['text'] = text
    mail['contact'] = contact
    mail['thread'] = thread
    mail['date'] = date
    mail['link'] = link

    all_mails.append(mail)


client = MongoClient('127.0.0.1', 27017)
db = client['baze']
mails = db.mails

for mail in all_mails:
    if not list(mails.find({'link':mail.get('link')})):
        mails.insert_one({'contact': mail['contact'],
                          'date': mail['date'],
                          'thread': mail['thread'],
                          'text': mail['text'],
                          'link': mail['link']
                          })

