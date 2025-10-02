import grpc
from concurrent import futures
import time

import chat_pb2
import chat_pb2_grpc

class ServidorChat(chat_pb2_grpc.ChatServicer):

    def Conversar(self, requisicao_stream, contexto):
        print("Cliente conectou ao chat.")
        
        for mensagem_cliente in requisicao_stream:
            print(f"[{mensagem_cliente.usuario}]: {mensagem_cliente.texto}")

            resposta_texto = f"Servidor ouviu sua mensagem: '{mensagem_cliente.texto}'"
            if "oi" in mensagem_cliente.texto.lower():
                resposta_texto = "Olá! Como posso ajudar?"
   
            mensagem_servidor = chat_pb2.Mensagem(
                usuario="Servidor",
                texto=resposta_texto
            )
            
            yield mensagem_servidor

def iniciar_servidor():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(ServidorChat(), servidor)
    
    print("Iniciando o servidor de chat. Escutando na porta 50054.")
    servidor.add_insecure_port('[::]:50054') # Usando a última porta para o exemplo
    servidor.start()
    servidor.wait_for_termination()

if __name__ == '__main__':
    iniciar_servidor()