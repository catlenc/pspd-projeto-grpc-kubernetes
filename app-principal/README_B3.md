# Infraestrutura Cloud Native com Kubernetes para Aplicação Distribuída

Este documento descreve como preparar e configurar a infraestrutura para a aplicação distribuída de microserviços gRPC utilizando Kubernetes em um ambiente local com Minikube. A configuração segue o modelo apresentado na Figura 2, onde um host único (`HServ`) executa o cluster Kubernetes que hospeda os contêineres da aplicação.

## Visão Geral da Arquitetura de Infraestrutura

A infraestrutura é composta por um cluster Kubernetes de nó único, gerenciado pelo Minikube, rodando em um host Linux (`HServ`). Dentro deste cluster, a aplicação é distribuída em três contêineres principais:

  * **Contêiner P (API-Gateway):** Atua como a porta de entrada da aplicação. Ele contém um servidor web que recebe requisições HTTP de clientes externos (como um navegador no `HClient`) e um cliente gRPC (stub) que traduz essas requisições em chamadas gRPC para os microserviços internos. Este contêiner está exposto tanto à rede externa (para tráfego HTTP) quanto à rede interna do cluster (para tráfego gRPC/HTTP/2).
  * **Contêiner A (Microserviço gRPC):** Executa o servidor gRPC do Módulo A. Ele responde apenas às requisições vindas da rede interna do cluster, especificamente do Contêiner P.
  * **Contêiner B (Microserviço gRPC):** Executa o servidor gRPC do Módulo B. Assim como o contêiner A, ele atende apenas às requisições internas do Contêiner P.

 \#\# Pré-requisitos no Host do Servidor (HServ)

Para configurar o ambiente, o host Linux (`HServ`) precisa ter as seguintes ferramentas instaladas:

1.  **Docker:** Um motor de contêiner para construir e executar as imagens da nossa aplicação.
2.  **Minikube:** Ferramenta para executar um cluster Kubernetes local de forma simples. (Site oficial: [minikube.sigs.k8s.io/docs/](https://minikube.sigs.k8s.io/docs/))
3.  **kubectl:** A interface de linha de comando do Kubernetes para gerenciar o cluster.

## Guia de Instalação e Deploy

Siga os passos abaixo para implantar a aplicação no cluster Minikube.

### Passo 1: Iniciar o Cluster Kubernetes

Com o Minikube instalado, inicie o cluster no `HServ` com o seguinte comando:

```bash
minikube start --driver=docker
```

### Passo 2: Construir as Imagens dos Contêineres

Para que o Minikube encontre as imagens Docker que vamos construir, precisamos apontar o ambiente do nosso terminal para o Docker daemon dentro do Minikube:

```bash
eval $(minikube -p minikube docker-env)
```

**Importante:** Este comando é válido apenas para a sessão atual do terminal. Se abrir um novo terminal, execute-o novamente.

Agora, construa a imagem Docker para cada um dos módulos (P, A e B):

```bash
# Navegue até a pasta do módulo A e construa a imagem
cd app-principal/modulo-a
docker build -t modulo-a-img .
cd ../..

# Navegue até a pasta do módulo B e construa a imagem
cd app-principal
docker build -t modulo-b-img .
cd ../..

# Navegue até a pasta do módulo P e construa a imagem
cd app-principal/modulo-p
docker build -t modulo-p-img .
cd ../..
```

### Passo 3: Implantar os Contêineres no Kubernetes

Com as imagens prontas, vamos usar `kubectl` para criar os recursos no cluster. Os arquivos de configuração (`.yaml`) na pasta `kubernete/` definem como os contêineres devem ser implantados (Deployments) e como eles se comunicam (Services).

1.  **Crie os Deployments:** Um Deployment garante que um número especificado de réplicas de um contêiner (Pod) esteja sempre em execução.

    ```bash
    kubectl apply -f kubernete/deployment-a.yaml
    kubectl apply -f kubernete/deployment-b.yaml
    kubectl apply -f kubernete/deployment-p.yaml
    ```

2.  **Crie os Services:** Um Service expõe os Pods a outras partes do cluster ou a redes externas.

      * `service-a` e `service-b` são do tipo `ClusterIP`, o que significa que só são acessíveis de dentro do cluster (pelo contêiner P).
      * `service-p` é do tipo `LoadBalancer`, expondo o contêiner P para fora do cluster, permitindo que o `HClient` o acesse.

    <!-- end list -->

    ```bash
    kubectl apply -f kubernete/service-a.yaml
    kubectl apply -f kubernete/service-b.yaml
    kubectl apply -f kubernete/service-p.yaml
    ```

### Passo 4: Verificar a Infraestrutura

Para confirmar que todos os contêineres estão em execução, use o comando:

```bash
kubectl get pods
```

Você deverá ver três pods, um para cada módulo, com o status `Running`.

Para verificar os serviços de rede:

```bash
kubectl get services
```

Você verá os três serviços, incluindo o IP externo para o `modulo-p-service`.

### Passo 5: Acessar a Aplicação a partir de um Cliente (HClient)

Para acessar a interface web da aplicação a partir de uma máquina cliente (`HClient`), como um desktop com um navegador:

1.  No `HServ`, execute o seguinte comando para obter o URL de acesso ao serviço P:
    ```bash
    minikube service modulo-p-service
    ```
2.  Este comando abrirá o navegador no `HServ` ou fornecerá um URL (ex: `http://192.168.49.2:30000`).
3.  Use este URL no navegador do `HClient` para acessar a aplicação.

O fluxo de comunicação será:

  * O **Navegador (HClient)** envia uma requisição **HTTP** para o URL do serviço P.
  * O **Contêiner P (API-Gateway)** recebe a requisição e a traduz em chamadas **gRPC (sobre HTTP/2)** para os serviços A e B na rede interna do Kubernetes.
  * Os **Contêineres A e B** processam as requisições e retornam as respostas para P.
  * O **Contêiner P** compila as respostas e as envia de volta para o navegador via **HTTP**.