import grpc
from concurrent import futures
import time

import downloader_pb2
import downloader_pb2_grpc

class ServidorDownloader(downloader_pb2_grpc.DownloaderServicer):

    def BaixarArquivo(self, requisicao, contexto):
        print(f"Cliente pediu para baixar o arquivo: {requisicao.nome_do_arquivo}")


        conteudo_arquivo_simulado = [
            "Primeira linha do arquivo.\n",
            "Esta é a segunda parte dos dados.\n",
            "Aqui vem um pouco mais de informação.\n",
            "Continuando o envio de dados em pedaços.\n",
            "Este é o último chunk. Download concluído.\n"
        ]

        for pedaco in conteudo_arquivo_simulado:

            pedaco_bytes = pedaco.encode('utf-8')

            resposta = downloader_pb2.Chunk(pedaco_de_dados=pedaco_bytes)
            
            print(f"Enviando chunk: {pedaco.strip()}")
            
            yield resposta
            
            time.sleep(1)

def iniciar_servidor():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    downloader_pb2_grpc.add_DownloaderServicer_to_server(ServidorDownloader(), servidor)
    
    print("Iniciando o servidor de download. Escutando na porta 50052.")
    servidor.add_insecure_port('[::]:50052') # Usando uma porta diferente para não conflitar
    servidor.start()
    servidor.wait_for_termination()

if __name__ == '__main__':
    iniciar_servidor()