import src.kakaoWork.kakaoWorkApiHelper as kakaoWorkHelper
import src.kakaoWork.kakaoWorkBlockBuilder as kakaoBlockBuilder
import browser_test as bt
import time





helper = kakaoWorkHelper.KakaoWorkApiHelper()
builder = kakaoBlockBuilder.KaKaoWorkBlockBuiler()



#에러가 없으면 성공 
if len(bt.err_msg) == 0:
    print("로그인 성공")
else: #에러가 뜨면 알람발생
    print("알람발생")

    #특정그룹 리스트 받아오기
    data = helper.getDepartmentsList() 
    #특정그룹의 users_ids 가져오기
    users = helper.getDepartmentsUserList(data,'smell system')

    #각 유저마다 1:1채팅방 오픈
    ids = []
    for i in users:
        con = helper.makeConversation(i)
        
        #각각 메시지 보내기
        helper.sendMessages(con['conversation']['id'],'test')


