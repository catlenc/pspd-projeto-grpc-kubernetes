import grpc

import calculadora_pb2
import calculadora_pb2_grpc

def executar_cliente():
    print("Tentando chamar o RPC Somar...")

    with grpc.insecure_channel('localhost:50051') as canal:
     
        cliente = calculadora_pb2_grpc.CalculadoraStub(canal)
   
        requisicao = calculadora_pb2.RequisicaoSoma(num1=10, num2=5)
   
        resposta = cliente.Somar(requisicao)
        
        print(f"O cliente recebeu a resposta: {resposta.resultado}")

if __name__ == '__main__':
    executar_cliente()