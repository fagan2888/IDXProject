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


for x in range(13000):

	for link in soup.findAll('div', attrs={"class":"container-space container-space--big ng-scope"}):
		# print(link.get_text())
		for link_a in link.findAll(attrs={"class":"text-bigger text-bold block-clear ng-binding"}):
			print(link_a.get_text())
			judul = link_a.get_text()
			targetFolder = os.path.join(os.getcwd(), judul.replace("/",""))
			while not os.path.exists(targetFolder):
				os.mkdir(targetFolder)
			link_judul = link_a.parent['href']
			print(link_judul)
			url = "https://www.idx.co.id"+link_judul
			myfile = requests.get(url)
			targetPDF_Judul = os.path.join(targetFolder, judul.replace("/","")+".pdf")
			code = open(targetPDF_Judul,'wb').write(myfile.content)

		for link_b in link.findAll('a', href = True, attrs={"class":"red ng-binding"}):
			print(link_b.get_text())
			nama_attachment = link_b.get_text() 
			link_attachment = link_b['href']
			print(link_attachment)
			url = "https://www.idx.co.id"+link_attachment
			myfile = requests.get(url)
			targetPDF_Attachment = os.path.join(targetFolder, nama_attachment.replace("/",""))
			code = open(targetPDF_Attachment, 'wb').write(myfile.content)
		print('-----------------------')


	driver.find_element_by_css_selector("a[ng-click='setCurrent(pagination.current + 1)']").click()
	time.sleep(5)
	all_html = driver.page_source
	soup = BeautifulSoup(all_html,"html.parser")
	all_folder_name = soup.findAll("p", attrs={"class":"text-bigger text-bold block-clear ng-binding"})
