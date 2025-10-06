from flask import Flask, jsonify, render_template
import os
import grpc
import requests

import produtos_pb2
import produtos_pb2_grpc

app = Flask(__name__)

CATALOGO_HOST = os.getenv('MODULO_A_HOST', 'localhost')
CATALOGO_PORT = os.getenv('MODULO_A_PORT', '50051')
INVENTARIO_HOST = os.getenv('MODULO_B_HOST', 'localhost')
INVENTARIO_PORT = os.getenv('MODULO_B_PORT', '50052')

CATALOGO_ADDRESS = f'{CATALOGO_HOST}:{CATALOGO_PORT}'
INVENTARIO_ADDRESS = f'{INVENTARIO_HOST}:{INVENTARIO_PORT}'

@app.route('/produtos-rest/<string:produto_id>', methods=['GET'])
def get_produto_detalhes_rest(produto_id):
    try:
        # 1. Chamar o Módulo A via REST
        resposta_a = requests.get(f'http://localhost:8081/produto/{produto_id}')
        resposta_a.raise_for_status() # Lança um erro se a resposta for 4xx ou 5xx
        info_basica = resposta_a.json()

        # 2. Chamar o Módulo B via REST
        resposta_b = requests.get(f'http://localhost:8082/estoque/{produto_id}')
        resposta_b.raise_for_status()
        estoque_info = resposta_b.json()

        # 3. Combinar as respostas
        resultado_combinado = {
            "id": info_basica.get("id"),
            "nome": info_basica.get("nome"),
            "descricao": info_basica.get("descricao"),
            "preco": estoque_info.get("preco"),
            "quantidade": estoque_info.get("quantidade")
        }

        return jsonify(resultado_combinado)

    except requests.exceptions.RequestException as e:
        return jsonify({"erro": "Falha ao comunicar com os serviços de backend via REST", "detalhes": str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/produtos/<string:produto_id>', methods=['GET'])
def get_produto_detalhes(produto_id):
    try:
        # --- 1. Conectar e chamar o Módulo A (Catálogo) ---
        with grpc.insecure_channel(CATALOGO_ADDRESS) as channel_a:
            stub_a = produtos_pb2_grpc.CatalogoStub(channel_a)
            requisicao_a = produtos_pb2.ProdutoRequest(id=produto_id)
            info_basica = stub_a.GetInfoBasica(requisicao_a)
            print(f"Recebido do serviço Catálogo: {info_basica}")

        # --- 2. Conectar e chamar o Módulo B (Inventário) ---
        with grpc.insecure_channel(INVENTARIO_ADDRESS) as channel_b:
            stub_b = produtos_pb2_grpc.InventarioStub(channel_b)
            requisicao_b = produtos_pb2.ProdutoRequest(id=produto_id)
            estoque_info = stub_b.GetEstoque(requisicao_b)
            print(f"Recebido do serviço Inventário: {estoque_info}")

        # --- 3. Combinar as respostas ---
        resultado_combinado = {
            "id": info_basica.id,
            "nome": info_basica.nome,
            "descricao": info_basica.descricao,
            "preco": estoque_info.preco,
            "quantidade": estoque_info.quantidade
        }

        # --- 4. Retornar a resposta HTTP em formato JSON ---
        return jsonify(resultado_combinado)

    except grpc.RpcError as e:
        # Trata erros caso um dos serviços gRPC falhe ou não encontre o produto
        print(f"Erro no gRPC: {e.details()}")
        return jsonify({"erro": f"Produto com ID {produto_id} não encontrado ou serviço indisponível.", "detalhes": e.details()}), 404

if __name__ == '__main__':
    # Roda o servidor web na porta 5000
    app.run(host='0.0.0.0', debug=True, port=5000)