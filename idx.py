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
import datetime

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


for x in range(25000):

	for link in soup.findAll('div', attrs={"class":"container-space container-space--big ng-scope"}):
		# print(link.get_text())
		# for link_time in link.findAll("time"):
		# 	waktu = link_time.get_text()
		# 	#print(waktu)
		# 	date_time_obj = datetime.datetime.strptime(waktu, "%d %B %Y %H:%M:%S")
		# 	converted_date = date_time_obj.date()
		# 	print(converted_date)

		for link_a in link.findAll(attrs={"class":"text-bigger text-bold block-clear ng-binding"}):

			for link_time in link.findAll("time"):
				waktu = link_time.get_text()
				#print(waktu)
				date_time_obj = datetime.datetime.strptime(waktu, "%d %B %Y %H:%M:%S")
				converted_date = str(date_time_obj.date()).replace("-","")
				#print(converted_date)


			print(converted_date+"_"+link_a.get_text())
			
			judul = link_a.get_text()
			namaFolder = converted_date+"_"+judul
			judul_windows = namaFolder.replace("/","").replace(chr(92),"").replace(chr(58),"").replace("*","").replace("?","").replace('"',"").replace("<","").replace(">","").replace("|","")

			targetFolder = os.path.join(os.getcwd(), judul_windows)
			while not os.path.exists(targetFolder):
				os.mkdir(targetFolder)
			link_judul = link_a.parent['href']
			print(link_judul)
			url = "https://www.idx.co.id"+link_judul
			myfile = requests.get(url)
			
			if(len(cwd+judul+judul) > 250):
				targetPDF_Judul = os.path.join(targetFolder, "Header"+".pdf")
				code = open(targetPDF_Judul,'wb').write(myfile.content)
			else:
				targetPDF_Judul = os.path.join(targetFolder, judul.replace("/","")+".pdf")
				code = open(targetPDF_Judul,'wb').write(myfile.content)
			time.sleep(2)
			target_txt = os.path.join(targetFolder, "link.txt")
			f = open(target_txt,"a")
			f.write(url + "\n")
			f.close()


		for link_b in link.findAll('a', href = True, attrs={"class":"red ng-binding"}):
			print(link_b.get_text())
			nama_attachment = link_b.get_text() 
			nama_attachment_windows = nama_attachment.replace("/","").replace(chr(92),"").replace(chr(58),"").replace("*","").replace("?","").replace('"',"").replace("<","").replace(">","").replace("|","")
			link_attachment = link_b['href']
			print(link_attachment)
			url = "https://www.idx.co.id"+link_attachment
			myfile = requests.get(url)
			if(len(cwd+judul+nama_attachment_windows) > 250):
				targetPDF_Attachment = os.path.join(targetFolder, nama_attachment_windows[0:200])
				code = open(targetPDF_Attachment, 'wb').write(myfile.content)
			else:
				targetPDF_Attachment = os.path.join(targetFolder, nama_attachment_windows)
				code = open(targetPDF_Attachment, 'wb').write(myfile.content)
			time.sleep(2)
			target_txt = os.path.join(targetFolder, "link.txt")
			f = open(target_txt,"a")
			f.write(url + "\n")
			f.close()

		print('-----------------------')

		time.sleep(1)


	driver.find_element_by_css_selector("a[ng-click='setCurrent(pagination.current + 1)']").click()
	time.sleep(5)
	all_html = driver.page_source
	soup = BeautifulSoup(all_html,"html.parser")
	all_folder_name = soup.findAll("p", attrs={"class":"text-bigger text-bold block-clear ng-binding"})
