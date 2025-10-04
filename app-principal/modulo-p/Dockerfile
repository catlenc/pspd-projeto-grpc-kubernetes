# Usar uma imagem base do Python
FROM python:3.10-slim

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Copiar os arquivos de dependências e instalar
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copiar o resto da aplicação
COPY . .

# Expor a porta que a aplicação vai rodar
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
