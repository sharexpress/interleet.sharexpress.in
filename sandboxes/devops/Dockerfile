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
    bind-tools

RUN addgroup -S judge && adduser -S -G judge -H -s /bin/bash judge

WORKDIR /workspace

USER judge
