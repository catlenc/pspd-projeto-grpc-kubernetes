# Projeto de Aplicação Distribuída com Microserviços gRPC e Kubernetes

Este projeto demonstra uma arquitetura de microserviços onde um frontend web se comunica com um backend gRPC através de um gateway de API. A aplicação é orquestrada utilizando Kubernetes.

## Arquitetura

A aplicação segue a arquitetura descrita na Figura 1, composta por três módulos principais no backend:

  * **Módulo P (Gateway API + Frontend):** Um serviço implementado em **Python** com Flask. Ele serve uma interface web para o usuário e atua como um cliente gRPC (Stub). Sua função é traduzir as requisições HTTP recebidas do navegador em chamadas gRPC para os microserviços A e B.
  * **Módulo A (Microserviço gRPC):** Um servidor gRPC implementado em **Go**. Responsável por uma parte da lógica de negócio (neste caso, o gerenciamento de nomes e preços de produtos).
  * **Módulo B (Microserviço gRPC):** Um servidor gRPC também implementado em **Go**. Responsável pela outra parte da lógica de negócio (gerenciamento de estoque de produtos).

Os três módulos trabalham de forma colaborativa para atender às solicitações do usuário.

 \#\# Pré-requisitos

Antes de começar, garanta que você tenha as seguintes ferramentas instaladas em sua máquina:

  * **Docker:** Para construir as imagens dos contêineres dos nossos serviços.
  * **Minikube:** Para executar um cluster Kubernetes local.
  * **kubectl:** A ferramenta de linha de comando para interagir com o cluster Kubernetes.

## Como Executar e Testar

Siga os passos abaixo para implantar e testar a aplicação em seu ambiente local.

### 1\. Iniciar o Cluster Kubernetes

Primeiro, inicie o Minikube para criar seu cluster local.

```bash
minikube start
```

### 2\. Configurar o Ambiente Docker

Para que o Minikube possa usar as imagens Docker que vamos construir localmente, aponte o seu terminal para o daemon Docker do Minikube.

```bash
eval $(minikube -p minikube docker-env)
```

**Atenção:** Este comando só vale para o terminal atual. Se você abrir um novo terminal, precisará executá-lo novamente.

### 3\. Construir as Imagens Docker

Navegue até a pasta de cada módulo e construa a respectiva imagem Docker.

  * **Módulo A (Go):**

    ```bash
    cd app-principal/modulo-a
    docker build -t modulo-a-img .
    cd ../..
    ```

  * **Módulo B (Go):**

    ```bash
    cd app-principal/modulo-b
    docker build -t modulo-b-img .
    cd ../..
    ```

  * **Módulo P (Python):**

    ```bash
    cd app-principal/modulo-p
    docker build -t modulo-p-img .
    cd ../..
    ```

### 4\. Implantar os Módulos no Kubernetes

Com as imagens prontas, use `kubectl` para aplicar os arquivos de configuração de implantação (Deployment) e serviço (Service) que estão na pasta `kubernete`.

  * **Aplicar os Deployments:**

    ```bash
    kubectl apply -f kubernete/deployment-a.yaml
    kubectl apply -f kubernete/deployment-b.yaml
    kubectl apply -f kubernete/deployment-p.yaml
    ```

  * **Aplicar os Services:**

    ```bash
    kubectl apply -f kubernete/service-a.yaml
    kubectl apply -f kubernete/service-b.yaml
    kubectl apply -f kubernete/service-p.yaml
    ```

Após aplicar os arquivos, você pode verificar se os pods estão rodando com o comando:

```bash
kubectl get pods
```

Aguarde até que o status de todos os pods seja "Running".

### 5\. Acessar e Testar a Aplicação

O **Módulo P** é o ponto de entrada da nossa aplicação e foi exposto através de um serviço do tipo `LoadBalancer`. Para obter o endereço de acesso, execute o seguinte comando no terminal:

```bash
minikube service modulo-p-service
```

Este comando abrirá automaticamente a interface web da aplicação no seu navegador.

**Para testar:**

1.  Na página web, você verá um campo para buscar um produto por ID.
2.  Digite um ID de produto (por exemplo, `1`ou `2`) e clique em "Buscar".
3.  O **Módulo P** receberá a requisição HTTP, fará uma chamada gRPC para o **Módulo A** para obter o nome e o preço do produto, e outra chamada gRPC para o **Módulo B** para obter o estoque.
4.  As informações coletadas dos dois microserviços serão combinadas e exibidas na tela.

Isso demonstra o funcionamento colaborativo de toda a arquitetura.

## Estrutura do Projeto

```
.
├── app-principal
│   ├── modulo-a/         # Microserviço A (Servidor gRPC em Go)
│   ├── modulo-b/         # Microserviço B (Servidor gRPC em Go)
│   ├── modulo-p/         # Módulo P (Cliente gRPC + Frontend Web em Python)
│   └── produtos.proto    # Arquivo de definição do Protobuf
│
├── kubernete/
│   ├── deployment-a.yaml # Arquivos de implantação e serviço
│   ├── deployment-b.yaml # para o Kubernetes
│   ├── deployment-p.yaml
│   ├── service-a.yaml
│   ├── service-b.yaml
│   └── service-p.yaml
│
└── README.md
```