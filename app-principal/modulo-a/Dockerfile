# Etapa 1: Build
FROM golang:1.23-alpine AS builder

WORKDIR /app

# Copiar os arquivos go.mod e go.sum
COPY go.mod go.sum ./

# Baixar as dependências
RUN go mod download

# Copiar o código fonte
COPY . .

# Construir o binário
# CGO_ENABLED=0 para criar um binário estático
RUN CGO_ENABLED=0 go build -o /main .

# Etapa 2: Imagem final
FROM alpine:latest

WORKDIR /app

# Copiar o binário construído da etapa anterior
COPY --from=builder /main .

# Expor a porta (ajuste se o seu serviço Go usar outra porta)
EXPOSE 50051

# Comando para rodar a aplicação
CMD ["./main"]
