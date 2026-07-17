FROM alpine:latest

RUN apk add --no-cache \
    bash \
    curl \
    wget \
    jq \
    vim \
    nano \
    sudo \
    iproute2 \
    net-tools \
    bind-tools \
    nginx \
    git

RUN addgroup -S judge && adduser -S -G judge -H -s /bin/bash judge
RUN echo "judge ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

WORKDIR /workspace

USER judge
