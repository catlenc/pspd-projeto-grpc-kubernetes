import grpc
from concurrent import futures

import calcular_media_pb2
import calcular_media_pb2_grpc

class ServidorCalculadorDeMedia(calcular_media_pb2_grpc.CalculadorDeMediaServicer):

    def CalcularMedia(self, requisicao_stream, contexto):
        print("Cliente conectou. Aguardando stream de números...")
        
        soma = 0
        contador = 0

        for req in requisicao_stream:
            print(f"Recebeu número: {req.valor}")
            soma += req.valor
            contador += 1
        
        media = soma / contador if contador > 0 else 0
        print(f"Stream do cliente finalizado. Média calculada: {media}")
    
        return calcular_media_pb2.MediaResponse(valor=media)

def iniciar_servidor():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calcular_media_pb2_grpc.add_CalculadorDeMediaServicer_to_server(
        ServidorCalculadorDeMedia(), servidor)
    
    print("Iniciando o servidor de média. Escutando na porta 50053.")
    servidor.add_insecure_port('[::]:50053')
    servidor.start()
    servidor.wait_for_termination()

if __name__ == '__main__':
    iniciar_servidor()