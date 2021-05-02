import requests
import json
import os
from dotenv import load_dotenv

class KakaoWorkApiHelper:
    def __init__(self):
        load_dotenv()
        self.token = ""
        self.KAKAO_WORK_URL = "https://api.kakaowork.com/v1/"
        self.KAKAO_WORK_KEY = os.getenv("KAKAO_WORK_BOT_1_KEY")
    
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
        

