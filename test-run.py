import unittest
import json
import io
import time
import cv2
import numpy as np
import os
from datetime import datetime
from PIL import Image
from threading import Thread
from pyvirtualdisplay import Display

import src.webDriver as webDriverHelper
from src.fileUpload.S3FileHelper import S3FileHelper
from src.test.TestScenario import TestScenario

class BrowserTest(unittest.TestCase):
    def setUp(self):
        # 가상 x11 실행
        self.disp=Display(backend="xvfb").start()
        self.driver = webDriverHelper.driver
        self.driver.implicitly_wait(10)
        self.testScenario = None
        self.passTest = False
        self.thread = None
        
    def tearDown(self):
        self.videoRecording = False 
        if self.thread and self.thread.is_alive():
            time.sleep(3)

        # 실패 시 notifiaction
        # TODO migrate to TestResult Object method (addFailure / addError)
        if not self.passTest and self.testScenario != None:
            self.driver.save_screenshot("output.png")

            now = datetime.now()
            imageKey = "images/broswer_test_fail_{}.png".format(now.strftime('%Y-%m-%d %H:%M:%S'))
            videoKey = "videos/broswer_test_fail_{}.avi".format(now.strftime('%Y-%m-%d %H:%M:%S'))
            
            fileHelper = S3FileHelper()
            fileHelper.uploadFile('output.png', imageKey)
            fileHelper.uploadFile('output.avi', videoKey)

            # signed Url
            imgSignedUrl = fileHelper.getSignedUrl(imageKey)
            videoSignedUrl = fileHelper.getSignedUrl(videoKey)

            self.testScenario.setImageLink(imgSignedUrl)
            self.testScenario.setVideoLink(videoSignedUrl)
            
            self.testScenario.sendFailAlertToKakaoWork()

        if os.path.isfile("output.png"):
            os.remove("output.png")
        if os.path.isfile("output.avi"):
            os.remove("output.avi")

        self.thread = None    
        self.driver.close()
        self.disp.stop()
    
    def __videoWriting(self):
        # open cv video writer
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi', fourcc , 20.0, (1920, 1080))

        while True:
            data = self.driver.get_screenshot_as_png()
            img = Image.open(io.BytesIO(data))
            numpy_array = np.asarray(img)
            frame = cv2.cvtColor(numpy_array, cv2.COLOR_BGR2RGB)
            out.write(frame)
            cv2.imshow('frame', frame)
            if not self.videoRecording:
                out.release()
                break

    def __recordVideoOnBackGround(self):
        self.videoRecording = True
        self.thread = Thread(target=self.__videoWriting)
        self.thread.daemon = True
        self.thread.start()

    def __clearBlock(self, webDriver):
        webDriver.implicitly_wait(10)
        deleteBtn = webDriver.find_element_by_xpath('//*[@id="root"]/div[1]/main/section[2]/article/div[2]/div[2]/button[2]');
        deleteBtn.click()
        webDriver.implicitly_wait(5)
        modalDeleteBtn = webDriver.find_element_by_xpath('//*[@id="root"]/div[1]/main/section[2]/article/div[4]/div/div/button[2]')
        modalDeleteBtn.click()
        webDriver.implicitly_wait(20)

    def test_scenario_header_block(self):
        # Write TestScenario
        self.testScenario = TestScenario(
            title = "헤더 블록 / 텍스트 블록 테스트",
            steps = []
        )

        # run Record Screen Video
        self.__recordVideoOnBackGround()

        webDriver = self.driver

        # step 1 - Open KakaoWorkBlockKit Url
        self.testScenario.addStep("Open KakaoWorkBlockKit Url")
        kakaoWorkBlockKitUrl = 'https://www.kakaowork.com/block-kit-builder';
        webDriver.get(kakaoWorkBlockKitUrl)
        webDriver.implicitly_wait(200)

        # TODO localStorage setItem OR Browser always init
        uiGuideConfirmBtn = webDriver.find_element_by_xpath('//*[@id="root"]/div[1]/main/section[2]/article/div[4]/div/button');
        if uiGuideConfirmBtn != None:
            uiGuideConfirmBtn.click()
            webDriver.implicitly_wait(5)

        # common elements
        blockKitJsonEl = webDriver.find_element_by_xpath('//*[@id="root"]/div[1]/main/section[2]/article/div[3]/div[2]/div/div[1]/div[2]/div[1]/div[4]')

        # step 2 - Header Block (in Nav) Click
        time.sleep(6)
        self.testScenario.addStep("Header Block (in Nav) Click")
        print("RUN - Header Block (in Nav) Click")
        navBuilderBtn = webDriver.find_element_by_xpath('/html/body/div[1]/div[1]/main/section[1]/div[1]/button[1]')
        navBuilderBtn.click()        
        webDriver.implicitly_wait(10)
        layoutHeader = webDriver.find_element_by_xpath('//*[@id="root"]/div[1]/main/section[2]/article/div[3]/div[1]/div/div/div/div[2]/div[2]/div/h2')    
        blockKitJson = json.loads(blockKitJsonEl.text)
        
        self.assertEqual(layoutHeader.text, 'Header Sample')
        self.assertEqual(blockKitJson, json.loads('{"text": "Push alarm message","blocks": [{"type": "header","text": "Header Sample","style": "blue"}]}'))
        self.__clearBlock(webDriver)

        # step 3 - Text Block (in Nav) Click
        time.sleep(6)
        self.testScenario.addStep("Text Block (in Nav) Click")
        print("RUN - Text Block (in Nav) Click")
        navBuilderBtn = webDriver.find_element_by_xpath('/html/body/div[1]/div[1]/main/section[1]/div[1]/button[2]')
        navBuilderBtn.click()
        webDriver.implicitly_wait(10)
        blockKitJson = json.loads(blockKitJsonEl.text)      
        layoutHeader = webDriver.find_element_by_xpath('/html/body/div[1]/div[1]/main/section[2]/article/div[3]/div[1]/div/div/div/div[2]/div[2]/div/div')

        # raise Fail
        self.assertEqual(layoutHeader.text, 'wrong - sample')
        self.assertEqual(blockKitJson, json.loads('{"text": "Push alarm message","blocks": [{"type": "text","text": "text sample","markdown": true}]}'))
        self.passTest = True


if __name__ == '__main__':
    unittest.main()
