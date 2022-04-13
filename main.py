#Load the libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import os

# Get the top 40 songs
response = requests.get("https://top40weekly.com/")
response.raise_for_status()
page_contents = response.text
doc = BeautifulSoup(page_contents, 'html.parser')
top40songsdets = doc.find_all('div', {'class':'x-text'})
p_tags = top40songsdets[2].find_all('p')

def get_ten(p_tags):
    a_list = p_tags.text.split(sep='\n')
    for i in range(0, len(a_list)):
        a_list[i] = a_list[i][3:].strip()
    return a_list

def get_top_40(p_tags):
    global top40list
    top40list =  []
    for i in range(0, len(p_tags)):
        top40list.extend(get_ten(p_tags[i]))
    return top40list

get_top_40(p_tags)

# start bot automation
try:
    driver = webdriver.Firefox(executable_path=r"geckodriver.exe")
    driver.implicitly_wait(8)
except:
    driver = webdriver.Chrome(executable_path=r"chromedriver.exe")

# Make folder where all songs would be stored
path = r"lyrics"
try:
    os.makedirs(path, exist_ok = True)
    print("Directory '%s' created successfully" % path)
except OSError as error:
    print("Directory '%s' can not be created" % path)

# Get the lyrics of every song on the top 40 list
# and store it to the lyrics folder
for song in top40list:
    song_name = song.split(sep="by")
    driver.get('https://www.azlyrics.com/')
    driver.implicitly_wait(8)
    element = driver.find_element_by_id('q')
    element.send_keys(song_name[0].strip())
    element.send_keys(Keys.RETURN)
    element2 = driver.find_element_by_class_name("visitedlyr")
    element2.click()
    response3 = requests.get(driver.current_url)
    page_contents3 = response3.content
    page_contents3 =page_contents3.decode('utf-8')
    doc3 = BeautifulSoup(page_contents3, 'html.parser')
    lyrics = doc3.select('div.main-page')
    another_list =lyrics[0].text.split(sep='\n')
    another_list = another_list[:-120]
    while '' in another_list:
        for word in another_list:
            if word =='':
                another_list.remove(word)
    with open(path + "\\" + song_name[0].strip() + ".txt", 'w', encoding='utf-*') as f:
        for line in another_list:
            f.write(line)
            f.write('\n')

driver.close()


