import grpc

import downloader_pb2
import downloader_pb2_grpc

def executar_cliente():
    with grpc.insecure_channel('localhost:50052') as canal:
        cliente = downloader_pb2_grpc.DownloaderStub(canal)
        
        print("Pedindo para baixar o arquivo 'meu_relatorio.txt'...")
        requisicao = downloader_pb2.RequisicaoArquivo(nome_do_arquivo="meu_relatorio.txt")
      
        respostas_stream = cliente.BaixarArquivo(requisicao)
        arquivo_completo = b""
        
        for resposta in respostas_stream:
            print(f"Recebeu um chunk de {len(resposta.pedaco_de_dados)} bytes.")
            arquivo_completo += resposta.pedaco_de_dados
            
        print("\n--- Download Concluído ---")
        print(arquivo_completo.decode('utf-8'))
        print("--------------------------")


if __name__ == '__main__':
    executar_cliente()