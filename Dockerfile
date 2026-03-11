FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Instala JDK, Maven e dependências necessárias para o jpackage gerar instaladores Linux.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-17-jdk \
        maven \
        fakeroot \
        dpkg-dev \
        rpm \
        binutils \
        xz-utils \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

# Script para gerar o JAR do projeto.
RUN printf '%s\n' \
    '#!/bin/bash' \
    'set -e' \
    'cd /app' \
    'mvn clean package' \
    > /usr/local/bin/build-jar && \
    chmod +x /usr/local/bin/build-jar

# Script para gerar o instalador Linux via jpackage.
RUN printf '%s\n' \
    '#!/bin/bash' \
    'set -e' \
    'cd /app' \
    'mvn clean package' \
    'mkdir -p dist' \
    'jpackage --type deb \' \
    '  --input target \' \
    '  --name "Sistema de gerenciamento Saciar" \' \
    '  --main-jar saciar-sistema-1.0.0.jar \' \
    '  --main-class com.saciar.SaciarApplication \' \
    '  --icon src/assets/logoSaciar.png \' \
    '  --linux-shortcut \' \
    '  --app-version 1.0.0 \' \
    '  --vendor "Saciar" \' \
    '  --dest dist' \
    > /usr/local/bin/build-installer && \
    chmod +x /usr/local/bin/build-installer

CMD ["/bin/bash"]
