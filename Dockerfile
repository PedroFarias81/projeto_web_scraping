# Usando a imagem base do Python
FROM python:3.12-slim

#Definindo o diretório de trabalho
WORKDIR /app

#Copiando o arquivo de dependência para o diretorio de trabalho
COPY requirements.txt .

#Instalando as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

#Copiando o código da aplicação para o container
COPY . .

#Instrução para rodar a aplicação
CMD ["python", "app.py"]