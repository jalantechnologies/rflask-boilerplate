FROM ubuntu:20.04

WORKDIR /root
RUN mkdir app

WORKDIR /root/app
COPY . .

RUN apt-get update -y && \
    apt-get install build-essential -y && \
    apt-get install git -y && \
    apt-get install curl -y
    
RUN apt-get install -y libgtk2.0-0 libgtk-3-0 libgbm-dev libnotify-dev libgconf-2-4 libnss3 libxss1 libasound2 libxtst6 xauth xvfb

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
RUN apt-get install software-properties-common -y

RUN add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get install python3.11 python3-pip -y && \
    pip install pipenv

RUN curl -sL https://deb.nodesource.com/setup_14.x -o nodesource_setup.sh && \
    bash nodesource_setup.sh && \
    cat /etc/apt/sources.list.d/nodesource.list

RUN apt-get install nodejs -y
RUN node --version && npm --version
RUN npm install && npm run build

CMD [ "npm", "run", "start" ]
