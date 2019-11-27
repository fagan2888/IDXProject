import time
import os
import shutil
from selenium import webdriver
import pyautogui
import os
from datetime import datetime
datestring = datetime.strftime(datetime.now(), '(%Y-%m-%d)-(%H.%M.ss)')
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib.request
import requests

cwd = os.getcwd()
DRIVER = 'chromedriver'


chrome_options = webdriver.ChromeOptions()
if os.name == "nt":
    # If current OS is Windows
    chrome_options.add_argument("--start-maximized")
else:
    # Other OS (Mac / Linux)
    chrome_options.add_argument("--kiosk")


#------------------------------------------------------------------
driver = webdriver.Chrome(DRIVER, chrome_options = chrome_options)
driver.get('https://www.idx.co.id/berita/pengumuman/')

all_html = driver.page_source
soup = BeautifulSoup(all_html,"html.parser")
all_folder_name = soup.findAll("p", attrs={"class":"text-bigger text-bold block-clear ng-binding"})


for x in range(15000):
	for x in all_folder_name:
		eachName = x.text.replace("/"," ")
		print(eachName)
		targetPath = os.path.join(os.getcwd(), eachName);
		while not os.path.exists(targetPath):
			os.mkdir(targetPath)
		for link in soup.findAll('a', href= True):			
				if(link['href'].split('.')[-1] == 'pdf'):
					nama_href = link['href']
					# print(nama_href)
					url = "https://www.idx.co.id"+nama_href
					print(url)
					myfile = requests.get(url)
					targetPath_PDF = os.path.join(targetPath,"pdf") ####------------->ini penting
					while not os.path.exists(targetPath_PDF):		  ####------------->ini penting
						os.mkdir(targetPath_PDF)					  ####------------->ini penting
					targetFile_PDF = os.path.join (targetPath_PDF, nama_href.split('/')[-1])
					code = open(targetFile_PDF,'wb').write(myfile.content)
			
		
		


	driver.find_element_by_css_selector("a[ng-click='setCurrent(pagination.current + 1)']").click()
	time.sleep(5)
	all_html = driver.page_source
	soup = BeautifulSoup(all_html,"html.parser")
	all_folder_name = soup.findAll("p", attrs={"class":"text-bigger text-bold block-clear ng-binding"})
