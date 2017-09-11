# Automated-Course-Registration 
#Copyright (C) 2017 Sanchit Anand 
 
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

import ssl
import urllib.request
from bs4 import BeautifulSoup
import time
import smtplib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException       
 
def check_exists_by_xpath(driver,xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

## Function to register. You need selenium for python, and chrome web driver should be in the same directory as this file.
def register_course():
	driver = webdriver.Chrome()
	##UIUC Enterprise Website
	driver.get("https://webprod.admin.uillinois.edu/ssa/servlet/SelfServiceLogin?appName=edu.uillinois.aits.SelfServiceLogin&dad=BANPROD1")
	elem = driver.find_element_by_id("netid")
	elem.clear()
	##Enter your netID below
	elem.send_keys("NETID")
	elem = driver.find_element_by_id("easpass")
	elem.clear()
	##Enter PW below 
	elem.send_keys("PASS")
	elem = driver.find_element_by_name("BTN_LOGIN")
	##Do a login
	elem.send_keys(Keys.RETURN)
	##Go to Course Registration Page
	elem = driver.find_element_by_xpath("//a[text()='Registration & Records']")
	elem.send_keys(Keys.RETURN)
	elem = driver.find_element_by_xpath("//a[text()='Classic Registration']")
	elem.send_keys(Keys.RETURN)
	elem = driver.find_element_by_xpath("//a[text()='Add/Drop Classes']")
	elem.send_keys(Keys.RETURN)
	elem = driver.find_element_by_xpath("//a[text()='I Agree to the Above Statement ']")
	elem.send_keys(Keys.RETURN)
	elem = driver.find_element_by_xpath("//input[@value='Submit']")
	elem.send_keys(Keys.RETURN)
	elem = driver.find_element_by_id("crn_id1")
	##Enter Course CRN
	elem.send_keys("CRN")
	elem = driver.find_element_by_xpath("//input[@value='Submit Changes']")
	##Submit
	elem.send_keys(Keys.RETURN)
	##Check if any errors popped up
	ret = not(check_exists_by_xpath(driver,"//table[@class= 'datadisplaytable']"))
	driver.close()
	return ret
 
##Function to send emails (via gmail right now)
def sendemail(fromaddr,toaddr,subject,user,pw,msg):
	header  = 'From: '+fromaddr+'\n'
	header += 'To: '+toaddr+'\n'
	header += 'Subject: '+subject+'\n\n'
	message = header + msg
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(user, pw)
	server.sendmail(fromaddr, toaddr, message)
	server.quit()
	
##main code	
##Enter year,semester(Fall,Spring or Summer),department, number and crn into link below 
if __name__ == "__main__":
	uri = 'https://courses.illinois.edu/cisapp/explorer/schedule/YEAR/SEM/DEP/NUM/CRN.xml'
	cont = ssl.SSLContext()

	#main loop. you need to install python package bs4 
	while True:
		#use college API to get course status
		with urllib.request.urlopen(uri,context=cont) as req:
			xml=req.read()
	 
		soup = BeautifulSoup(xml,"html.parser")
	 
		status = soup.enrollmentstatus.string
	 
		if status != 'Closed':
			#display something to console
			print("Registering")
			#try to register
			register_course()
			#send yourself an email(function is only good for logging into gmail right now). You might have to change your gmail account settings.
			sendemail("FROMEmailID","TO","SUBJECT","FROMEmailID", "PASSWORD","BODY")
			
		else:
			#do something
			print('Running')
		##Run in a loop 
		time.sleep(30)