# Etapa 1: Build
FROM golang:1.23-alpine AS builder

# O WORKDIR agora é a raiz do projeto
WORKDIR /app

# Copiar tudo do contexto (app-principal) para o WORKDIR
COPY . .

# Mudar para o diretório do módulo que queremos construir
WORKDIR /app/modulo-b

# Baixar as dependências e construir o binário
# O 'go mod download' vai usar o go.mod e a diretiva 'replace'
RUN go mod download
# O binário será criado em /main
RUN CGO_ENABLED=0 go build -o /main .

# Etapa 2: Imagem final
FROM alpine:latest

WORKDIR /app

# Copiar o binário construído da etapa anterior, do caminho correto
COPY --from=builder /main .

# Expor a porta
EXPOSE 50052

# Comando para rodar a aplicação
CMD ["./main"]