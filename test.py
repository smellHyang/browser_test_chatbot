from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from bs4 import BeautifulSoup
from os.path import join, dirname, abspath
from dotenv import load_dotenv
import os
import requests
import json


dotenv_path = join(dirname('__file__'), '.env')
load_dotenv(dotenv_path,  verbose=True)

BROWSER_TEST_EMAIL = os.getenv("BROWSER_TEST_EMAIL")
BROWSER_TEST_PW = os.getenv("BROWSER_TEST_PW")
 
#driver = webdriver.Chrome(r'C:\chromedriver.exe') ## webdriver 경로 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')       # 창 숨기는 옵션 추가
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

 
driver.implicitly_wait(10)  ## 10초까지 기다려준다. 10초 안에 웹 화면이 표시되면 바로 다음 작업이 진행됨

#sleep(8) # 무조건 지정된 time만큼 대기 
#url = 'https://nid.naver.com/nidlogin.login' #네이버
#url = 'https://logins.daum.net/accounts/signinform.do' #다음아이디
url = 'https://accounts.kakao.com/login?continue=https%3A%2F%2Faccounts.kakao.com%2Fweblogin%2Faccount%2Finfo' #카카오로그인

driver.get(url)  ##접속
#driver.find_element_by_xpath('//*[@id="query"]').send_keys('selenium') # 입력창에 텍스트 입력
#driver.find_element_by_xpath('//*[@id="search_btn"]').click() # 특정 버튼 클릭
driver.implicitly_wait(10)
#driver.save_screenshot("Website_login_fail1.png")

#로그인 실패
#driver.get('https://logins.daum.net/accounts/signinform.do')
#driver.find_element_by_name('id').send_keys('dlgiddk30')
#driver.find_element_by_name('pw').send_keys('giddk19951')
#driver.find_element_by_xpath('//*[@id="log.login"]').click() # 네이버
#driver.find_element_by_xpath('//*[@id="loginBtn"]').click() # 다음

#로그인 성공
driver.find_element_by_name('email').send_keys(BROWSER_TEST_EMAIL)
driver.find_element_by_name('password').send_keys(BROWSER_TEST_PW)
driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click() 

driver.save_screenshot("Website_login_fail1.png")


#//*[@id="err_common"]/div/p
#에러창 뜨는지 가져오기
response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    err_msg = soup.select('.error')
else : 
    print(response.status_code)

#에러가 없으면 성공 
if len(err_msg) == 0:
    print("로그인 성공")
else: #에러가 뜨면 알람발생
    print("알람발생")

#REST API함수(GET/POST)
API_HOST = 'https://api.kakaowork.com'
headers = {'Authorization': 'Bearer fcc51469.9a8a4a0ac62c4fd19cebc97c61511763', 'Content-Type': 'application/json'}  

def req(path, query, method, data={}):
    url = API_HOST + path 

    print('HTTP Method: %s' % method)
    print('Request URL: %s' % url)
    print('Headers: %s' % headers)
    print('QueryString: %s' % query)

    if method == 'GET':
        return requests.get(url, headers=headers)
    elif method == 'POST':
        return requests.post(url, headers=headers, data=data)  



#1. 사용자 리스트 받아오기
resp = req('/v1/users.list', '', 'GET')
#print(resp)
#print("response status:%d\n" % resp.status_code)
#print("response headers:%s\n" % resp.headers)
print("response body:%s\n" % resp.text)

json_data = json.loads(resp.text)
user_id = []
for entry in json_data['users']: 
  user_id.append(entry['id'])

#2. 그룹채팅방 오픈
#params = {"user_ids" :  user_id   }
params = {"user_id" : user_id[0]}
print("len>>>>>>>>", len(user_id[0]))
resp = req('/v1/conversations.open', '', 'POST', data=json.dumps(params))
#print("response body:%s\n" % resp.text)
print("conversations.open >>> " , resp.text)

#채팅방 정보가져오기
resp = req('/v1/conversations.list', '', 'GET')
#print("conversation.list  >>>>> " % resp.text)

json_data = json.loads(resp.text)
conversation_id = []
for entry in json_data['conversations']: 
  conversation_id.append(entry['id'])

print("conversation.id >>>>> ",  conversation_id[1])
print("len_conversation >>>>>", len(conversation_id[1]))
#3. 메세지보내기(알림)
params = {"conversation_id" :  conversation_id[1]
            ,"text": "Push alarm message",
            "blocks": [
                        {
                        "type": "header",
                        "text": "[조간점검] 이벤트 오류 알람 발생",
                        "style": "blue"
                        },                        
                        {
                        "type": "text",
                        "text": "- 자산명 : TMS자금관리 WEB#1                                    - IP정보 : 123.456.789.001                                - 발생시간 : 2021/04/25 08:48:27                                - 알람정의 : 로그인 접속 오류 발생",
                        "markdown": True
                        },
                        {
                        "type": "divider"
                        },
                        {
                            "type": "context",
                            "content": {
                                "type": "text",
                                "text": "[포탈 접속하기](https://www.naver.com)",
                                "markdown": True
                            },
                            "image": {
                                "type": "image_link",
                                "url": "https://www.google.com/url?sa=i&url=https%3A%2F%2Ficon-icons.com%2Fko%2F%25EC%2595%2584%25EC%259D%25B4%25EC%25BD%2598%2Fsign-error%2F34362&psig=AOvVaw3OKDkWAf1eNIFRa7ub6T8X&ust=1619378462219000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCKjBz4PNl_ACFQAAAAAdAAAAABAD"
                            }
                         }
    
                    ]  
            }
resp = req('/v1/messages.send', '', 'POST', data=json.dumps(params))
print(resp)



driver.quit()
