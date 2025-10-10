Claro, segue o arquivo `README.md` com o trecho solicitado substituído:

# Microserviços com gRPC e Kubernetes: Consulta de Produtos

## 📖 Sobre o Projeto

Este projeto é uma demonstração prática de uma arquitetura de microserviços distribuídos, desenvolvida no âmbito da disciplina de Programação para Sistemas Paralelos e Distribuídos (PSPD). A aplicação simula um sistema de consulta de produtos, onde as informações estão segmentadas em diferentes serviços, comunicando-se através do gRPC para alta performance e orquestrados com Kubernetes para escalabilidade e resiliência.

O objetivo principal é demonstrar uma arquitetura poliglota, onde os microserviços de backend são desenvolvidos em **Go** e o serviço de gateway/API é desenvolvido em **Python**.

## 🏛️ Arquitetura

A aplicação é composta por três módulos principais, seguindo o padrão de API Gateway:

  * **Módulo A (Serviço de Catálogo):** Um servidor gRPC desenvolvido em **Go**. É responsável por fornecer informações básicas de um produto, como nome e descrição.
  * **Módulo B (Serviço de Inventário):** Um servidor gRPC também em **Go**. É responsável por fornecer informações de stock e preço do produto.
  * **Módulo P (API Gateway):** Um servidor web desenvolvido em **Python** com **Flask**. Ele atua como a porta de entrada para o cliente final. Recebe requisições HTTP/REST, comunica-se com os microserviços A e B através de um cliente gRPC (stub), combina as respostas e devolve um JSON completo para o cliente.

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

1.  **Configuração do Ambiente**
    Primeiro, inicie o cluster Minikube e configure o ambiente Docker para que o Minikube possa utilizá-lo.

    ```bash
    # Inicie o cluster Kubernetes local
    minikube start
    # Configure o seu terminal para usar o daemon Docker do Minikube
    eval $(minikube docker-env)
    ```

    *Importante: O comando `eval $(minikube docker-env)` deve ser executado em cada novo terminal que você abrir para interagir com este projeto.*

2.  **Construindo as Imagens Docker**
    As imagens Docker para cada módulo devem ser construídas a partir do diretório `app-principal`, que é a pasta "pai" de todos os módulos.

    Navegue para o diretório `app-principal`:

    ```bash
    cd "caminho/para/o/projeto/pspd-projeto-grpc-kubernetes/app-principal"
    ```

    Agora, construa a imagem para cada um dos módulos:

    ```bash
    # Construir a imagem do Módulo P (API Gateway em Python)
    docker build -t modulo-p:latest -f modulo-p/Dockerfile .
    # Construir a imagem do Módulo A (Microserviço em Go)
    docker build -t modulo-a:latest -f modulo-a/Dockerfile .
    # Construir a imagem do Módulo B (Microserviço em Go)
    docker build -t modulo-b:latest -f modulo-b/Dockerfile .
    ```

    *Nota: O `.` no final de cada comando é crucial. Ele define o contexto do build para o diretório `app-principal`, permitindo que os Dockerfiles acessem os arquivos de outros módulos quando necessário.*

3.  **Deploy no Kubernetes**
    Com as imagens prontas, vamos fazer o deploy da aplicação no cluster Minikube usando os arquivos de configuração.

    Navegue para o diretório `kubernete`:

    ```bash
    cd "../kubernete" # A partir da pasta app-principal
    ```

    Aplique os deployments e serviços:
    Execute os comandos abaixo para criar os pods (onde os contêineres rodam) e os services (que permitem a comunicação entre eles e com o exterior).

    ```bash
    # Aplicar os deployments
    kubectl apply -f deployment-a.yaml
    kubectl apply -f deployment-b.yaml
    kubectl apply -f deployment-p.yaml
    # Aplicar os serviços
    kubectl apply -f service-a.yaml
    kubectl apply -f service-b.yaml
    kubectl apply -f service-p.yaml
    ```

4.  **Verificando e Acessando a Aplicação**
    Após aplicar os arquivos, verifique se tudo está rodando corretamente.

    ```bash
    # Verifique se os pods estão com o status "Running"
    kubectl get pods
    # Verifique se os serviços foram criados
    kubectl get services
    ```

    Finalmente, para acessar a aplicação, obtenha o URL do serviço do Módulo P (`modulo-p-service`):

    ```bash
    minikube service modulo-p-service --url
    ```

    O comando acima irá retornar um URL, algo como `http://192.168.49.2:30001`. Copie este URL e cole no seu navegador para ver a aplicação funcionando.

### Troubleshooting

  * **Erro:** `ERROR: failed to build: ... no such file or directory`
      * **Causa:** Você está executando o comando `docker build` a partir do diretório errado (por exemplo, de dentro de `modulo-b`).
      * **Solução:** Certifique-se de executar todos os comandos `docker build` a partir do diretório `app-principal`.
  * **Erro:** `Exiting due to SVC_NOT_FOUND: Service 'service-p' was not found...`
      * **Causa:** O nome do serviço no comando `minikube service` está incorreto.
      * **Solução:** Verifique o nome correto do serviço com `kubectl get services`. O nome correto é `modulo-p-service`. Use o comando: `minikube service modulo-p-service --url`.

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