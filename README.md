# browser-test-bot

### Usage

```bash
# install Container
docker run -i -t dlgiddk10/kakaowork:1.0

# git clone
git clone https://github.com/smellHyang/browser_test_chatbot.git

# 패키지 설치
cd browser_test_chatbot
conda env update -f ./environment.yml

# .env setting
KAKAO_WORK_BOT_1_KEY=
KAKAO_WORK_USER_EMAIL=
AWS_S3_ACCRESS_KEY=
AWS_S3_SECRET_KEY=
AWS_S3_KAKAO_WORK_BUCKET_NAME=

# run broswer-test
python -m unittest test-run
```



![image](https://user-images.githubusercontent.com/73684562/116816085-7ff56000-ab9b-11eb-93d0-d92680dd2593.png)


### 시나리오 contents
1. Block Kit Builder 접속 (https://www.kakaowork.com/block-kit-builder)
2. 메뉴의 [Header Block] 클릭 시 미리보기 화면의 이미지 및 텍스트 박스에 정확한 정보 입력되었는지 체크(성공)
3. 메뉴의 [Text Block] 클릭 시 미리보기 화면의 이미지 및 텍스트 박스에 정확한 정보 입력되었는지 체크(실패)
4. 테스트 실패 시 설정한 이메일 기준 그룹대화 창 오픈 및 알람 발생


### Issue 및 해결 방안

- python 패키지 관리 문제
    - dockerFile 로 패키지 설치하여 관리할 수도 있었지만 miniConda 로 관리하기로 함
- conda 설정으로 export 한 파일(environment.yml)로 패키지 설치 시 15분 넘게 걸리는 걸리는 이슈 발견
    - 당시 conda 종속성 관리 관리 로직을 이해 못하여 퍼포먼스 이슈가 생김, 패키지 파일의 버전을 명시하여  Indexing 범위를 축소 [[참조](https://www.anaconda.com/blog/understanding-and-improving-condas-performance)]
- GUI 환경이 셋팅이 되지 않은 Linux 도커 컨테이너에서 web driver 사용
    - 웹드라이버 설정 중 Headless 설정으로 웹 드라이버 사용하고 디버그 시 스크린 샷을 이용하여 확인
- Web driver 사용 시 웹브라우저에서 한글이 깨져서 노출되는 이슈
    - 한글 시스템 폰트를 별도로 설치
- python opencv 사용하여 Record 파일 생성 시 Image 관련 클래스(Pillow, Python Imaging Library)를 사용할 수 없었던 이슈
    - Xvfb (화면 출력을 표시하지 않고 가상 메모리에서 모든 그래픽 작업을 수행하는 X11 디스플레이 서버)  설치 및 pyvirtualdisplay 패키지를 통해 Xvfb 가상 환경 셋팅
    - [https://github.com/ponty/pyvirtualdisplay/tree/2.1](https://github.com/ponty/pyvirtualdisplay/tree/2.1)

### 아쉬운 점

- 카카오 블록 킷 웹페이지 처음 접속 시 가이드 UI 뜨는 문제 해결 방안 (LocalStorage SetItem)
- 동영상 생성 시 스크린 샷으로 생성하는데 프레임 수(20)에 맞게 sleep 추가 또는 동영상 생성 방법 변경
- 테스트 케이스 실패 처리 시 Unittest TestResult 객체의 addFailure / addError 메소드를 활용하여 개선하면 더 좋을 것 같음
- 괜찮은 테스트 시나리오(실무 관련)가 있어 좀 더 디테일하게


###화면결과
https://user-images.githubusercontent.com/73684562/118298135-0b66dd80-b51a-11eb-976f-5feca00f2d6a.jpeg
