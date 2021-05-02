import os
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone

import src.kakaoWork.kakaoWorkBlockBuilder as kakaoBlockBuilder
from src.kakaoWork.kakaoWorkApiHelper import KakaoWorkApiHelper

class TestScenario():
    def __init__(self, title, steps = []) :
        self.title = title
        self.steps = steps
        self.imageUrl = None
        self.videoUrl = None

    def addStep(self, description):
        self.steps.append(description)

    def setImageLink(self, url):
        self.imageUrl = url
    
    def setVideoLink(self, url):
        self.videoUrl = url

    def __makeKakaoWorkBlockBuilder(self):
        builder = kakaoBlockBuilder.KaKaoWorkBlockBuiler()
        builder.setHeaderBlock("브라우저 테스트 실패 알림")
        builder.addTextBlock('*{}*'.format(self.title))
        builder.addDividerBlock()
        
        for index, step in enumerate(self.steps):
            builder.addTextBlock('{0} > {1}'.format(index + 1, step))
        if self.steps:
            builder.addDividerBlock()    

        if self.imageUrl != None:
            builder.addImageLinkBlock(self.imageUrl)

        if self.videoUrl != None:
            builder.addContextBlock("[error.avi]({})".format(self.videoUrl))

        now = datetime.now(timezone('Asia/Seoul'))
        builder.addDescriptionBlock("일시", now.strftime('%Y-%m-%d %H:%M:%S'))
        
        return builder    

    def sendFailAlertToKakaoWork(self):
        load_dotenv()
        helper = KakaoWorkApiHelper()
        email = os.getenv("KAKAO_WORK_USER_EMAIL")
        block = self.__makeKakaoWorkBlockBuilder().toBlock()

        response = helper.findUserByEmail(email)
        userId = response['user']['id'] if response.get('user') else None
        if userId == None:
            raise Exception("유저 검색 실패!")

        conversationId = None
        if os.path.isfile("conversation.txt"):
            f = open("conversation.txt", "r")
            conversationId = f.readline()
            f.close()
        else: 
            userIds = [userId]
            response = helper.makeConversation(userIds = userIds)
            conversationId = response['conversation']['id'] if response.get('conversation') else None
            f = open("conversation.txt", "a")
            f.write(conversationId)
            f.close()
        
        if conversationId == None:
            raise Exception("채팅방 생성 실패!")
        
        helper.sendMessages(conversationId = conversationId, text = "{} 실패!!".format(self.title), blocks=block)
        
        
