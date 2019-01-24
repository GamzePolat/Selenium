from selenium import webdriver
import time
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)  
driver = webdriver.Firefox()
driver.get("https://www.hide-my-ip.com/tr/proxylist.shtml")
time.sleep(3)
ip=[]
port=[]
i=1
j=0
k=0



while i<=20:
 
    ip_element=driver.find_elements_by_xpath("//*[@id='sort-list']/tbody/tr["+str(i)+"]/td[1]")
    port_element=driver.find_elements_by_xpath("//*[@id='sort-list']/tbody/tr["+str(i)+"]/td[2]")
    
   
    
    for ip_elements in ip_element:
        ip.append(ip_elements.text)
    for port_elements in port_element:
        port.append(port_elements.text)
    i+=1
print(ip[1])
print(port[1])
    
time.sleep(3)

@app.route('/', methods=['POST'])
def sendUrl():
     content=request.get_json()
     url=content['url']
     count=content['count']
     return "tamam"


def send(url,count):
    j=0
    while j<=count:   
        PROXY=ip[j]+":"+port[j]
        print(PROXY)
        
        webdriver.DesiredCapabilities.FIREFOX['proxy']= {
            "httpProxy":PROXY,
            "ftpProxy":PROXY,
            "sslProxy":PROXY,
            "proxyType":"MANUAL"
        }
        driver = webdriver.Firefox()
        driver.get("url") 
        timeout = 5
        try:
            element_present = EC.presence_of_element_located((By.ID, 'element_id'))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            print ("Timed out waiting for page to load")
        j+=1
    driver.close()
if __name__ == '__main__':
    app.run(port=3002,debug=True)

