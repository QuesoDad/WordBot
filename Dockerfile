FROM ubuntu:14.04
MAINTAINER Ryan Lee <ryantlee9@gmail.com>

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
	wget
# Torch and luarocks
WORKDIR /root
#RUN git clone git://github.com/luarocks/luarocks.git
RUN git clone --recursive https://github.com/torch/distro.git ~/torch 
RUN cd ~
RUN cd torch
RUN ~/torch/clean.sh
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

WORKDIR /root
# RUN git clone https://github.com/larspars/word-rnn.git
RUN git clone https://github.com/kboruff/wordbot.git
WORKDIR /wordbot

# WORKDIR word-rnn
# RUN wget http://nlp.stanford.edu/data/glove.840B.300d.zip
# RUN mkdir util/glove
# RUN fastjar xvf glove.840B.300d.zip
# RUN mv glove.840B.300d.txt glove/vectors.840B.300d.txt
# RUN rm glove*
