# Etapa 1: Build da aplicação
FROM golang:1.23-alpine AS builder

# Define o diretório de trabalho raiz do nosso projeto dentro da imagem
WORKDIR /app

# Copia os arquivos de definição de módulos de ambos os projetos.
# Isso é feito primeiro para aproveitar o cache do Docker. A camada
# só será reconstruída se os arquivos go.mod ou go.sum mudarem.
COPY modulo-a/go.mod modulo-a/go.sum ./modulo-a/
COPY modulo-b/go.mod modulo-b/go.sum ./modulo-b/

# Define o diretório de trabalho para o modulo-b para que o Go
# possa resolver a dependência local do modulo-a.
WORKDIR /app/modulo-b

# Baixa as dependências. Como o contexto agora está correto,
# o "replace" no go.mod vai funcionar.
RUN go mod download

# Volta para a raiz do projeto na imagem
WORKDIR /app

# Agora copia todo o código-fonte de ambos os módulos
COPY modulo-a/ ./modulo-a/
COPY modulo-b/ ./modulo-b/

# Entra novamente no diretório do modulo-b para compilar
WORKDIR /app/modulo-b

# Compila o binário da aplicação de forma estática
RUN CGO_ENABLED=0 go build -o /main .

# Etapa 2: Imagem final, leve e otimizada
FROM alpine:latest

WORKDIR /app

# Copia apenas o binário compilado da etapa de build
COPY --from=builder /main .

# Expõe a porta que o serviço gRPC do modulo-b vai escutar
EXPOSE 50052

# Comando para iniciar a aplicação quando o contêiner rodar
CMD ["./main"]