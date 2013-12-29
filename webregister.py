from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select, WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from time import sleep
import requests
import sys
from datetime import datetime

nexmo_key = '07a0e4e7'
nexmo_secret = 'e561a9c4'
nexmo_number = '17142940200'

f = open('log.txt', 'a')
f.write(datetime.now().isoformat() + ' ')

if len(sys.argv) >= 2 and sys.argv[1] == "testalert":
	txt = {
		'api_key': nexmo_key,
		'api_secret': nexmo_secret,
		'from': nexmo_number,
		'to': "16505808282",
		'text': "Testing"
	}

	f.write('testalert\r\n')
	requests.get("https://rest.nexmo.com/sms/json", params=txt)
	sys.exit(0)

# Create a new instance of the driver
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
	"(KHTML, like Gecko) Chrome/15.0.87"
)

driver = webdriver.PhantomJS("./phantomjs", desired_capabilities=dcap)

# Go to UIUC Enterprise homepage
driver.get("https://eas.admin.uillinois.edu/eas/servlet/EasLogin?redirect=https://webprod.admin.uillinois.edu/ssa/servlet/SelfServiceLogin?appName=edu.uillinois.aits.SelfServiceLogin&dad=BANPROD1")

# Authenticate
driver.find_element_by_id("ENT_ID").send_keys("alee13")
driver.find_element_by_id("PASSWORD").send_keys("Mozart314")
sleep(5)
driver.find_element_by_name("BTN_LOGIN").click()

WebDriverWait(driver, 5).until(EC.title_contains("Main Menu"))
sleep(1)
driver.find_element_by_partial_link_text("Registration").click()

WebDriverWait(driver, 5).until(EC.title_contains("Registration"))
sleep(1)
driver.find_element_by_link_text("Registration").click()

WebDriverWait(driver, 5).until(EC.title_contains("Registration;"))
sleep(1)
driver.find_element_by_partial_link_text("Look-up").click()

WebDriverWait(driver, 5).until(EC.title_contains("Registration Agreement"))
sleep(1)
driver.find_element_by_partial_link_text("I Agree to the Above Statement").click()

WebDriverWait(driver, 5).until(EC.title_contains("Select A Term"))
sleep(1)
select = Select(driver.find_element_by_name("p_term"))
select.select_by_value("120141")
sleep(0.5)
driver.find_element_by_name("p_term").submit()

WebDriverWait(driver, 5).until(EC.title_contains("Look-up"))
sleep(1)
select = Select(driver.find_element_by_id("subj_id"))
select.select_by_value("ECE")
sleep(0.5)
driver.find_element_by_xpath("//input[@name='SUB_BTN'][@value='Course Search']").click()

WebDriverWait(driver, 5).until(EC.title_contains("Results;"))
sleep(1)
driver.find_element_by_xpath("//input[@name='SEL_CRSE'][@value='411']/../input[@name='SUB_BTN']").click()

WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "32816")))
x = len(driver.find_elements_by_xpath("//abbr[@title='Closed']"))

if len(sys.argv) >= 2 and sys.argv[1] == "repl":
	f.write('repl ')
	print(x)

f.write('x=' + str(x) + ' ')

if int(x) != 2:
	# Alert via text
	txt = {
		'api_key': nexmo_key,
		'api_secret': nexmo_secret,
		'from': nexmo_number,
		'to': "16505808282",
		'text': "WebRegister alert. (ECE411)"
	}

	requests.get("https://rest.nexmo.com/sms/json", params=txt)

driver.quit()
f.write('\r\n')
f.close()
