import grpc
from concurrent import futures
import time

import calculadora_pb2
import calculadora_pb2_grpc

class ServidorCalculadora(calculadora_pb2_grpc.CalculadoraServicer):
  
    def Somar(self, requisicao, contexto):
        print(f"Requisição recebida: {requisicao}")
        
        resultado_soma = requisicao.num1 + requisicao.num2
        
        return calculadora_pb2.RespostaSoma(resultado=resultado_soma)


def iniciar_servidor():
   
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    calculadora_pb2_grpc.add_CalculadoraServicer_to_server(ServidorCalculadora(), servidor)
    
    print("Iniciando o servidor. Escutando na porta 50051.")
    servidor.add_insecure_port('[::]:50051')
    servidor.start()
    
    try:
        while True:
            time.sleep(86400) # Dorme por um dia
    except KeyboardInterrupt:
        servidor.stop(0)

if __name__ == '__main__':
    iniciar_servidor()