FROM ubuntu:22.04

# Avoid tzdata prompts
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    wget \
    jq \
    vim \
    nano \
    sudo \
    iproute2 \
    net-tools \
    dnsutils \
    && rm -rf /var/lib/apt/lists/*

# Add judge user for sandbox execution
RUN useradd -m -s /bin/bash judge

WORKDIR /workspace

# Set default user to judge
USER judge
