FROM repo:tag

# git clone

# TODO 크롬 설치 대체
# 아래 링크는 git clone 시 루트 파일로 대체 가능!
# wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# dpkg -i ./google-chrome-stable_current_amd64.deb
# apt-get update
# apt --fix-broken install 
# dpkg -i google-chrome-stable_current_amd64.deb
# dpkg -l | grep chrome

# conda 설정
RUN conda create --name browser-test-bot python=3.8
RUN conda env list
RUN conda init
# RUN conda activate browser-test-bot ㄷ
RUN conda config --add channels conda-forge
RUN conda config --set channel_priority strict

# TODO 
RUN conda install -c bjrn webdriver_manager
RUN conda install selenium
RUN conda install time
RUN conda install beautifulsoup4
RUN conda install python-dotenv

# TODO
CMD ["/bin/bash"]