import selenium
from selenium import webdriver

driver = webdriver.Chrome("C:/chromedriver.exe")
driver.maximize_window()

driver.get("http://127.0.0.1:5000/assistants/")
driver.find_element_by_css_selector("#navbarTogglerDemo02 > ul > li > a").click()
driver.find_element_by_css_selector("#username").send_keys("Max")
driver.find_element_by_css_selector("#firstName").send_keys("Maksymilian")
driver.find_element_by_css_selector("#lastName").send_keys("Kalek")
driver.find_element_by_xpath("//input[@value='generatedPhoto']").click()
driver.find_element_by_xpath("//input[@value='3D Technologist']").click()
driver.find_element_by_css_selector("body > div > form > button").click()

driver.get("http://127.0.0.1:5000/assistants/")
driver.find_element_by_css_selector("body > div > ul > li > div > div.col-md-3.align-self-end.text-right.mb-4 > a:nth-child(1) > button").click()
driver.find_element_by_xpath("//input[@value='generatedPhoto']").click()
driver.find_element_by_css_selector("body > div > form > button").click()

driver.get("http://127.0.0.1:5000/assistants/")
driver.find_element_by_css_selector("body > div > ul > li > div > div.col-md-3.align-self-end.text-right.mb-4 > a:nth-child(2) > button").click()
driver.find_element_by_css_selector("body > div > ul > li > div > div.col-md-4.align-self-end.text-right.mb-4 > form > a > button").click()
driver.quit()
print("ALL TESTS PASSED")