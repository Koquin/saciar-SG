FROM ubuntu:22.04

# Instala dependências básicas
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk maven

# Define o diretório de trabalho
WORKDIR /app

# Copia o projeto para o container
COPY . /app

# Compila o projeto (gera o JAR)
RUN mvn clean package

# Não executa nada por padrão
CMD ["/bin/bash"]
