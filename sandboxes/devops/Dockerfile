FROM alpine:latest

# Install standard Alpine packages
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
    git \
    openssl \
    bc \
    procps \
    sysstat \
    logrotate \
    supervisor \
    mariadb-client \
    redis \
    haproxy \
    openrc \
    yamllint \
    nmap \
    netcat-openbsd \
    tar \
    gzip \
    zip \
    unzip \
    ansible \
    kubectl

# Install statically compiled Terraform binary
RUN curl -LO https://releases.hashicorp.com/terraform/1.8.5/terraform_1.8.5_linux_amd64.zip && \
    unzip terraform_1.8.5_linux_amd64.zip && \
    mv terraform /usr/bin/ && \
    rm terraform_1.8.5_linux_amd64.zip

RUN addgroup -S judge && adduser -S -G judge -H -s /bin/bash judge
RUN echo "judge ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

WORKDIR /workspace

USER judge
