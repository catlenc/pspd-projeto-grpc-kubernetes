import grpc
import time

import chat_pb2
import chat_pb2_grpc

def gerar_mensagens():
    mensagens = [
        chat_pb2.Mensagem(usuario="Cliente", texto="Oi, servidor!"),
        chat_pb2.Mensagem(usuario="Cliente", texto="Tudo bem por aí?"),
        chat_pb2.Mensagem(usuario="Cliente", texto="Vou encerrar a conexão."),
    ]
    for msg in mensagens:
        print(f"Enviando para o servidor: '{msg.texto}'")
        yield msg
        time.sleep(2) 

def executar_cliente():
    with grpc.insecure_channel('localhost:50054') as canal:
        cliente = chat_pb2_grpc.ChatStub(canal)
        
        print("Iniciando chat bidirecional...")
        
        respostas = cliente.Conversar(gerar_mensagens())
        
        for resposta in respostas:
            print(f"[{resposta.usuario}]: {resposta.texto}")

if __name__ == '__main__':
    executar_cliente()