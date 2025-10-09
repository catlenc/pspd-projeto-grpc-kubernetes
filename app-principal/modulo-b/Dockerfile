# Etapa 1: Build
FROM golang:1.23-alpine AS builder

WORKDIR /app

# Copiar os arquivos de ambos os módulos para que o 'replace' funcione
COPY . .

# Mudar para o diretório do modulo-b
WORKDIR /app/modulo-b

# Baixar as dependências
RUN go mod download

# Construir o binário
# CGO_ENABLED=0 para criar um binário estático
RUN CGO_ENABLED=0 go build -o /main .

# Etapa 2: Imagem final
FROM alpine:latest

WORKDIR /app

# Copiar o binário construído da etapa anterior
COPY --from=builder /main .

# Expor a porta
EXPOSE 50052

# Comando para rodar a aplicação
CMD ["./main"]