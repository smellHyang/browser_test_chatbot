# Linux amb64 https://hub.docker.com/r/continuumio/miniconda3
FROM continuumio/miniconda3

# 크롬 설치
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# exit 0; 성공했다고 가정
RUN dpkg -i ./google-chrome-stable_current_amd64.deb; exit 0 
RUN apt-get update
# fix dependecies
RUN apt-get -f --yes install
RUN dpkg -i ./google-chrome-stable_current_amd64.deb
RUN rm ./google-chrome-stable_current_amd64.deb

# X virtual Framebuffer / X 윈도우 GUI
RUN apt-get install --yes xvfb x11-xkb-utils
RUN apt-get install --yes xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic

# 한글 폰트 설치
RUN apt-get install -y fonts-nanum
RUN fc-cache -f -v

# git clone
RUN git clone https://github.com/smellHyang/browser_test_chatbot.git

# conda 설정
RUN conda update -n base -c defaults conda
RUN conda init
RUN conda config --add channels conda-forge
RUN conda config --set channel_priority strict
RUN conda install -c bjrn webdriver_manager


CMD ["/bin/bash"]
