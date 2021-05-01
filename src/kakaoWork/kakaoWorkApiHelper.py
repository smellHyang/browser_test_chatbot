import requests
import json
import os
from os.path import join, dirname, abspath
from dotenv import load_dotenv


dotenv_path = join(dirname('__file__'), '.env')
load_dotenv(dotenv_path,  verbose=True)

KAKAO_WORK_BOT_1_KEY = os.getenv("KAKAO_WORK_BOT_1_KEY")

class KakaoWorkApiHelper:
    def __init__(self):
        self.token = ""
        self.KAKAO_WORK_URL = "https://api.kakaowork.com/v1/"
        self.KAKAO_WORK_KEY = KAKAO_WORK_BOT_1_KEY
        #self.KAKAO_WORK_KEY = 'fcc51469.9a8a4a0ac62c4fd19cebc97c61511763'
        #self.KAKAO_WORK_KEY = 'b003ce81.566ec4094de04f419701127f6b75b471'
    
    def makeConversation(self, userIds):
        url = self.KAKAO_WORK_URL + "conversations.open"
        headers = {
            'Authorization': 'Bearer ' + self.KAKAO_WORK_KEY,
            'Content-type': 'application/json'
            }
        if(isinstance(userIds,list)):
            data = {'user_ids': userIds} #그룹대화
        else:
            data = {'user_id': userIds} #1:1대화
        response = requests.post(url, headers = headers, data = json.dumps(data))
        return response.json()

    def getDepartmentsList(self):
        url = self.KAKAO_WORK_URL + "departments.list"
        headers = {'Authorization': 'Bearer ' + self.KAKAO_WORK_KEY}
        response = requests.get(url, headers = headers)
        return response.json()

    def getDepartmentsUserList(self, data, departmentName):
        for entry in data['departments']:  
            if entry['name'] == departmentName:
                return entry['users_ids']

    #
    def getSpecificIds(self, data, specific):
        ids = []
        for entry in data[specific]:  
            ids.append(entry['id'])
        return ids

    def findUserByEmail(self, email):
        url = self.KAKAO_WORK_URL + "users.find_by_email"
        headers = {'Authorization': 'Bearer ' + self.KAKAO_WORK_KEY}
        params = {'email' : email}
        response = requests.get(url, headers = headers, params = params)
        return response.json()

    def sendMessages(self, conversationId, text, blocks = ''):
        url = self.KAKAO_WORK_URL + "messages.send"
        headers = {
            'Authorization': 'Bearer ' + self.KAKAO_WORK_KEY,
            'Content-type': 'application/json'
            }
        data = {'conversation_id': conversationId, 'text': text, 'blocks': blocks}
        #print(json.dumps(data))
        response = requests.post(url, headers = headers, data = json.dumps(data))
        return response.json()
    
    def userList(self):
        url = self.KAKAO_WORK_URL + "users.list"
        headers = {'Authorization': 'Bearer ' + self.KAKAO_WORK_KEY}
        response = requests.get(url, headers = headers)
        return response.json()
        

