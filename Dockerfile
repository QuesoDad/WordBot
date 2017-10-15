FROM ubuntu:14.04
MAINTAINER Kristian Boruff <kboruff@gmail.com>

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get update && apt-get install -y \
	curl \
	git \
	libpcre3 \
	libpcre3-dev \
	fastjar \
	software-properties-common \
	wget \
	python3-pip \
	build-essential \
	libssl-dev \
	libffi-dev \
	python3-dev

WORKDIR /dockerdata
RUN pip3 install --upgrade pip
RUN pip3 install twython
RUN pip3 install --upgrade google-api-python-client

# Torch and luarocks
WORKDIR /root
RUN git clone --recursive https://github.com/torch/distro.git ~/torch 
RUN cd ~
RUN cd torch
RUN bash ~/torch/install-deps && cd ~/torch && ./install.sh

ENV LUA_PATH='/root/.luarocks/share/lua/5.1/?.lua;/root/.luarocks/share/lua/5.1/?/init.lua;/root/torch/install/share/lua/5.1/?.lua;/root/torch/install/share/lua/5.1/?/init.lua;./?.lua;/root/torch/install/share/luajit-2.1.0-beta1/?.lua;/usr/local/share/lua/5.1/?.lua;/usr/local/share/lua/5.1/?/init.lua'
ENV LUA_CPATH='/root/.luarocks/lib/lua/5.1/?.so;/root/torch/install/lib/lua/5.1/?.so;./?.so;/usr/local/lib/lua/5.1/?.so;/usr/local/lib/lua/5.1/loadall.so'
ENV PATH=/root/torch/install/bin:$PATH
ENV LD_LIBRARY_PATH=/root/torch/install/lib:$LD_LIBRARY_PATH
ENV DYLD_LIBRARY_PATH=/root/torch/install/lib:$DYLD_LIBRARY_PATH
ENV LUA_CPATH='/root/torch/install/lib/?.so;'$LUA_CPATH

WORKDIR /root
RUN luarocks install nngraph
RUN luarocks install nninit
RUN luarocks install optim
RUN luarocks install nn
RUN luarocks install underscore.lua --from=http://marcusirven.s3.amazonaws.com/rocks/
RUN luarocks install lrexlib-pcre PCRE_LIBDIR=/lib/x86_64-linux-gnu

WORKDIR /root
RUN git clone https://github.com/kboruff/wordbot.git
WORKDIR /root/wordbot

# Nvidia-Docker WIP section
# WORKDIR /root
# RUN sudo apt-get -f install
# RUN wget -P /tmp https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.1/nvidia-docker_1.0.1_amd64.tar.xz
# RUN sudo tar --strip-components=1 -C /usr/bin -xvf /tmp/nvidia-docker*.tar.xz && rm /tmp/nvidia-docker*.tar.xz
# RUN rm /tmp/nvidia-docker_1.0.1-1_amd64.deb

# WORKDIR /root
# RUN luarocks install cutorch
# RUN luarocks install cunn
# RUN luarocks install cltorch
# RUN luarocks install clnn

