from selenium import webdriver
import time
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import requests
import datetime

app = Flask(__name__)  
client=MongoClient('127.0.0.1')
db=client.login
#collection = db.users
@app.route('/singup',methods=['POST'])
def singUp():
    content=request.get_json()
    username=content['username']
    password=content['password']
    save=db.users.insert_one({"username":username, "password":password})
    return "success"

@app.route('/login', methods=['POST'])
def login():
    content=request.get_json()
    username=content['username']
    password=content['password']
    url=content['url']
    count=content['count']
    htime=content['htime']
    date_time_str=content['date_time_str']
    timeout = round((int(htime) * 60) / int(count))
    print(timeout)
    date_time_obj = datetime.datetime.strptime(date_time_str, '%m-%d-%Y %H:%M:%S')
    now=datetime.datetime.now()
    c=date_time_obj-now
    datetime.timedelta(0, 8, 562000)
    b=divmod(c.days * 86400 + c.seconds, 60)[0]
    print(b)
    times=b*60
    
 
    time.sleep(int(times))
    resultUsername= db.users.find_one({"username": username})
    resultPassword= db.users.find_one({"password": password})
    print(resultUsername['username'][0])
    if resultUsername == None and resultPassword==None:
        print("NOT FOUND")

    try:
        if password==resultUsername['password'][0]:

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
           
            k=0
            posts=db.ipSave
            j=0
            while k < int(count):
                post_data={
                    'username':username,
                    'count':count,
                    'ip':ip[k],
                    'port':port[k],
                    'last_modified': datetime.datetime.utcnow()
                    
                   

                }
                
                result=posts.insert_one(post_data)
                k+=1
                print('One Post: {0}' .format(result.inserted_id))
            
            

           
            while j<int(count):   
                PROXY=ip[j]+":"+port[j]
                print(PROXY)
                
                webdriver.DesiredCapabilities.FIREFOX['proxy']= {
                    "httpProxy":PROXY,
                    "ftpProxy":PROXY,
                    "sslProxy":PROXY,
                    "proxyType":"MANUAL"
                }
                driver = webdriver.Firefox()
                
                driver.get(content['url']) 
               
               
                try:
                    element_present = EC.presence_of_element_located((By.ID, 'element_id'))
                    WebDriverWait(driver, timeout).until(element_present)
                except TimeoutException:
                    print ("Timed out waiting for page to load")
                j+=1
            driver.close()
            return "tamam"
        else:
            print("username or password is wrong")
            return "username or password is wrong"
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                # Whoops it wasn't a 200
                return "Error: " + str(e)

            # Must have been a 200 status code
            json_obj = response.json()
            return json_obj
           
        
    except:
        return "Sonlandi"

        # Whoops it wasn't a 200
        #return "Error: " + str(e)
    
   
        


if __name__ == '__main__':
    app.run(port=3003,debug=True)
