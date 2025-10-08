# Testando os Exemplos gRPC

Este documento fornece instruções sobre como testar os exemplos de comunicação gRPC presentes na pasta `exemplos-gRPC`.

## Visão Geral do Projeto

Este projeto demonstra os quatro tipos de comunicação suportados pelo gRPC:

  * **Unary Call:** Um cliente envia uma única requisição e recebe uma única resposta do servidor.
  * **Server-streaming Call:** Um cliente envia uma única requisição e recebe um fluxo de respostas do servidor.
  * **Client-streaming Call:** Um cliente envia um fluxo de requisições e recebe uma única resposta do servidor.
  * **Bidirectional-streaming Call:** Um cliente e um servidor enviam um fluxo de mensagens um para o outro.

## Pré-requisitos

  * Python 3.x
  * pip (gerenciador de pacotes do Python)

## Instalação

1.  Navegue até a pasta `exemplos-gRPC`.
2.  Instale as dependências usando o seguinte comando:

<!-- end list -->

```bash
pip install -r requirements.txt
```

## Executando os Exemplos

Para cada exemplo, você precisará abrir dois terminais: um para o servidor e outro para o cliente.

### 1\. Unary Call (Chamada Unária)

Este exemplo demonstra uma chamada unária onde um cliente envia dois números para um servidor e o servidor retorna a soma.

  * **Arquivo Protobuf:** `01-unary-call/calculadora.proto`

**No primeiro terminal (servidor):**

```bash
python exemplos-gRPC/01-unary-call/servidor.py
```

**No segundo terminal (cliente):**

```bash
python exemplos-gRPC/01-unary-call/cliente.py
```

### 2\. Server-streaming Call (Streaming do Servidor)

Este exemplo demonstra uma chamada de streaming do servidor onde um cliente solicita um arquivo e o servidor o envia em partes (chunks).

  * **Arquivo Protobuf:** `02-server-streaming/downloader.proto`

**No primeiro terminal (servidor):**

```bash
python exemplos-gRPC/02-server-streaming/servidor.py
```

**No segundo terminal (cliente):**

```bash
python exemplos-gRPC/02-server-streaming/cliente.py
```

### 3\. Client-streaming Call (Streaming do Cliente)

Este exemplo demonstra uma chamada de streaming do cliente onde um cliente envia uma sequência de números para o servidor e o servidor retorna a média deles.

  * **Arquivo Protobuf:** `03-client-streaming/calcular_media.proto`

**No primeiro terminal (servidor):**

```bash
python exemplos-gRPC/03-client-streaming/servidor.py
```

**No segundo terminal (cliente):**

```bash
python exemplos-gRPC/03-client-streaming/cliente.py
```

### 4\. Bidirectional-streaming Call (Streaming Bidirecional)

Este exemplo demonstra uma chamada de streaming bidirecional onde um cliente e um servidor podem trocar mensagens de chat em tempo real.

  * **Arquivo Protobuf:** `04-bidirectional-streaming/chat.proto`

**No primeiro terminal (servidor):**

```bash
python exemplos-gRPC/04-bidirectional-streaming/servidor.py
```

**No segundo terminal (cliente):**

```bash
python exemplos-gRPC/04-bidirectional-streaming/cliente.py
```

## Conclusão

  * **Unary Call:** Ideal para requisições simples e diretas, como obter um recurso específico ou realizar uma operação atômica.
  * **Server-streaming Call:** Útil para situações onde o servidor precisa enviar uma grande quantidade de dados para o cliente de forma contínua, como streaming de vídeo ou downloads de arquivos grandes.
  * **Client-streaming Call:** Adequado para cenários onde o cliente precisa enviar uma grande quantidade de dados para o servidor, como upload de arquivos ou envio de dados de telemetria.
  * **Bidirectional-streaming Call:** Perfeito para comunicações em tempo real que exigem uma troca contínua de informações em ambas as direções, como em aplicações de chat, jogos online ou sessões interativas.