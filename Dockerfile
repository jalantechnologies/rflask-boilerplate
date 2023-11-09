# Use the Ubuntu 20.04 base image
FROM ubuntu:20.04

# Set the NVM environment variable and create the working directory
ENV NVM_DIR=/root/.nvm
WORKDIR /app

# Update and install necessary dependencies
RUN apt-get update && \
    apt-get install -y curl wget && \
    apt-get clean

# Install NVM, configure it, and install Node.js 14.17.3
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash && \
    /bin/bash -c "source /root/.nvm/nvm.sh && nvm install 14.17.3 && nvm alias default 14.17.3"

RUN /bin/bash -c "source /root/.nvm/nvm.sh && npm install -g npm"

# Install Pipenv, build your Node.js app, and set the default command
RUN apt-get install -y python3-pip && \
    pip install pipenv && \
    npm install && \
    npm run build

# Set the default command to start your Node.js app
CMD [ "npm", "run", "app:serve" ]
