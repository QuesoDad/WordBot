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
RUN curl -s https://raw.githubusercontent.com/torch/ezinstall/master/install-deps | bash
# Torch and luarocks
RUN git clone https://github.com/torch/distro.git /root/torch --recursive && cd /root/torch && \
    bash ./clean.sh && \
	install-deps && \
    ./install.sh -b

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
# RUN mkdir tmp
# RUN wget -P /tmp https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.1/nvidia-docker_1.0.1-1_amd64.deb
# RUN sudo dpkg -i /tmp/nvidia-docker*.deb
# RUN rm /tmp/nvidia-docker*.deb

WORKDIR /root
RUN luarocks install torch
RUN luarocks install cutorch
RUN luarocks install cunn
RUN luarocks install cltorch
RUN luarocks install clnn

WORKDIR /root
RUN git clone https://github.com/larspars/word-rnn.git
RUN git clone https://github.com/kboruff/wordbot.git

WORKDIR word-rnn
RUN wget http://nlp.stanford.edu/data/glove.840B.300d.zip
RUN mkdir util/glove
RUN fastjar xvf http://nlp.stanford.edu/data/glove.840B.300d.zip
RUN mv glove.840B.300d.txt util/glove/vectors.840B.300d.txt
RUN rm glove*
