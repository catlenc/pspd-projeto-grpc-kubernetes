# pspd-projeto-grpc-kubernetes
Projeto da disciplina de PSPD sobre gRPC, Kubernetes e Microserviços.


/pspd-projeto-grpc-kubernetes
|
|-- .gitignore
|-- README.md
|
|-- exemplos-grpc/
|   |-- 01-unary-call/
|   |-- 02-server-streaming/
|   |-- 03-client-streaming/
|   `-- 04-bidirectional-streaming/
|
|-- app-principal/
|   |-- produtos.proto
|   |-- modulo-a/        (Serviço de Catálogo)
|   |-- modulo-b/        (Serviço de Inventário)
|   `-- modulo-p/        (Gateway)
|
`-- kubernetes/
    |-- deployment-a.yaml
    |-- service-a.yaml
    |-- ... (e assim por diante para B e P)
