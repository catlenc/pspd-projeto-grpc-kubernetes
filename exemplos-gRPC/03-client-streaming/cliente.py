import grpc
import time

import calcular_media_pb2
import calcular_media_pb2_grpc

def gerar_numeros():
    numeros_para_enviar = [5, 10, 15, 20, 25, 30]
    
    for numero in numeros_para_enviar:
        print(f"Enviando número: {numero}")
        yield calcular_media_pb2.NumeroRequest(valor=numero)
        time.sleep(1)

def executar_cliente():
 
    with grpc.insecure_channel('localhost:50053') as canal:
        cliente = calcular_media_pb2_grpc.CalculadorDeMediaStub(canal)
        stream_de_requisicoes = gerar_numeros()
        
        print("Enviando stream de números para o servidor calcular a média...")
        
        resposta = cliente.CalcularMedia(stream_de_requisicoes)
        
        print(f"\nO servidor calculou a média! Resultado: {resposta.valor}")

if __name__ == '__main__':
    executar_cliente()