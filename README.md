# Microserviços com gRPC e Kubernetes: Consulta de Produtos

## 📖 Sobre o Projeto

Este projeto é uma demonstração prática de uma arquitetura de microserviços distribuídos, desenvolvida no âmbito da disciplina de Programação para Sistemas Paralelos e Distribuídos (PSPD). A aplicação simula um sistema de consulta de produtos, onde as informações estão segmentadas em diferentes serviços, comunicando-se através do gRPC para alta performance e orquestrados com Kubernetes para escalabilidade e resiliência.

O objetivo principal é demonstrar uma arquitetura poliglota, onde os microserviços de backend são desenvolvidos em **Go** e o serviço de gateway/API é desenvolvido em **Python**.

## 🏛️ Arquitetura

[cite\_start]A aplicação é composta por três módulos principais, seguindo o padrão de API Gateway[cite: 2, 65]:

  * **Módulo A (Serviço de Catálogo):** Um servidor gRPC desenvolvido em **Go**. É responsável por fornecer informações básicas de um produto, como nome e descrição.
  * **Módulo B (Serviço de Inventário):** Um servidor gRPC também em **Go**. É responsável por fornecer informações de stock e preço do produto.
  * **Módulo P (API Gateway):** Um servidor web desenvolvido em **Python** com **Flask**. Ele atua como a porta de entrada para o cliente final. [cite\_start]Recebe requisições HTTP/REST, comunica-se com os microserviços A e B através de um cliente gRPC (stub), combina as respostas e devolve um JSON completo para o cliente[cite: 15, 244].

## ✨ Tecnologias Utilizadas

  * **Linguagens:** Go, Python
  * **Comunicação entre Microserviços:** gRPC, Protocol Buffers
  * **API Gateway & Web:** Flask (Python)
  * **Containerização:** Docker
  * **Orquestração:** Kubernetes (Minikube)

## ▶️ Como Executar o Projeto

Existem duas formas de executar a aplicação: localmente na sua máquina ou num cluster Kubernetes (usando Minikube).

### 1\. Execução Local (Fora de Contêineres)

Esta abordagem é ideal para desenvolvimento e testes rápidos de cada serviço individualmente.

**Pré-requisitos:**

  * Go (versão 1.23+)
  * Python (versão 3.10+)
  * `pip` e `venv`

**Passos:**

1.  **Pare o Minikube** (caso esteja a ser executado) para libertar as portas:

    ```bash
    minikube stop
    ```

2.  **Abra 3 terminais diferentes**, um para cada módulo.

3.  **Terminal 1: Rodar o Módulo A (Catálogo)**

    ```bash
    cd app-principal/modulo-a
    go run main.go
    # O servidor estará a escutar na porta 50051
    ```

4.  **Terminal 2: Rodar o Módulo B (Inventário)**

    ```bash
    cd app-principal/modulo-b
    go run main.go
    # O servidor estará a escutar na porta 50052
    ```

5.  **Terminal 3: Rodar o Módulo P (Gateway)**

    ```bash
    cd app-principal/modulo-p

    # Crie e ative um ambiente virtual (venv)
    python -m venv venv
    source venv/bin/activate

    # Instale as dependências
    pip install -r requirements.txt

    # Gere os ficheiros do Protobuf (caso encontre erros de importação)
    python -m grpc_tools.protoc -I../ --python_out=. --grpc_python_out=. ../produtos.proto

    # Execute o servidor Flask
    python app.py
    # O servidor estará a escutar na porta 5000
    ```

6.  **Aceda à Aplicação:** Abra o seu navegador e vá para `http://localhost:5000`.

### 2\. Execução com Docker e Kubernetes

Esta abordagem simula um ambiente de produção, orquestrando os serviços como contêineres.

**Pré-requisitos:**

  * Docker
  * Minikube
  * kubectl

**Passos:**

1.  **Inicie o Minikube:**

    ```bash
    minikube start
    ```

2.  **Configure o ambiente Docker:** Aponte o seu terminal para o daemon Docker do Minikube.

    ```bash
    eval $(minikube -p minikube docker-env)
    ```

    *Nota: Este comando deve ser executado em cada novo terminal que interage com o Minikube.*

3.  **Construa as Imagens Docker:** A partir da **raiz do projeto**, execute os seguintes comandos:

    ```bash
    # Construir imagem para o Módulo A
    docker build -t modulo-a:latest -f app-principal/modulo-a/Dockerfile app-principal/modulo-a

    # Construir imagem para o Módulo B
    docker build -t modulo-b:latest -f app-principal/modulo-b/Dockerfile app-principal/

    # Construir imagem para o Módulo P
    docker build -t modulo-p:latest -f app-principal/modulo-p/Dockerfile app-principal/modulo-p
    ```

4.  **Implante no Kubernetes:** Navegue para a pasta `kubernete` e aplique todos os manifestos de configuração.

    ```bash
    cd kubernete
    kubectl apply -f .
    ```

5.  **Verifique se os Pods estão a funcionar:**

    ```bash
    kubectl get pods
    # Espere até que o STATUS de todos os pods seja "Running"
    ```

6.  **Aceda à Aplicação:** Obtenha o URL do serviço e abra-o no seu navegador.

    ```bash
    minikube service modulo-p-service --url
    ```

## 📂 Estrutura do Projeto

```
/
|-- app-principal/
|   |-- produtos.proto         # Definição da API gRPC
|   |-- modulo-a/              # Microserviço de Catálogo (Go)
|   |-- modulo-b/              # Microserviço de Inventário (Go)
|   `-- modulo-p/              # API Gateway (Python/Flask)
|
|-- exemplos-grpc/             # Códigos de exemplo dos 4 tipos de comunicação gRPC
|
`-- kubernete/
    |-- deployment-a.yaml      # Manifestos de Deployment e Service
    |-- service-a.yaml         # para os módulos A, B e P
    |-- ...
|
`-- README.md                  # Este ficheiro
```


