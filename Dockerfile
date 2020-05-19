#FROM python:3.7
#
#ENV PYTHONUNBUFFERED 1
#
##RUN echo \
##deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free\
##deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free\
##deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free\
##deb https://mirrors.tuna.tsinghua.edu.cn/debian-security buster/updates main contrib non-free\
##    > /etc/apt/sources.list
#
#RUN apt-get update
#RUN apt-get install python3-dev default-libmysqlclient-dev -y
#
#RUN mkdir /code
#WORKDIR /code
#RUN pip install pip -U -i https://pypi.tuna.tsinghua.edu.cn/simple
#ADD requirements.txt /code/
#RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
#ADD . /code/

#FROM python:3.7
#ENV PYTHONUNBUFFERED 1
## 添加这两行
#RUN sed -i 's#http://archive.ubuntu.com/#http://mirrors.tuna.tsinghua.edu.cn/#' /etc/apt/sources.list;
#RUN apt-get update --fix-missing
#RUN apt-get install python3-dev default-libmysqlclient-dev -y --fix-missing

#RUN mkdir /code
#WORKDIR /code
#COPY pip.conf /root/.pip/pip.conf
#RUN pip install pip -U
#ADD requirements.txt /code/
#RUN pip install -r requirements.txt
#ADD . /code/

FROM python:3.7
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY pip.conf /root/.pip/pip.conf
COPY requirements.txt /usr/src/app/
RUN pip install --upgrade pip
RUN pip install -r /usr/src/app/requirements.txt
RUN rm -rf /usr/src/app
COPY . /usr/src/app
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8080"]

