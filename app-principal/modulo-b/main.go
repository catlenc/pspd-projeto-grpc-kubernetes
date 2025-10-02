package main

import (
	"context"
	"fmt"
	"log"
	"net"

	"google.golang.org/grpc"
	
	pb "projeto-catalogo/proto"
)

type servidor struct {
	pb.UnimplementedInventarioServer 
}

var estoque = map[string]*pb.EstoqueResponse{
	"1": {Id: "1", Preco: 249.99, Quantidade: 78},
	"2": {Id: "2", Preco: 450.50, Quantidade: 42},
}

func (s *servidor) GetEstoque(ctx context.Context, req *pb.ProdutoRequest) (*pb.EstoqueResponse, error) {
	idProduto := req.GetId()
	log.Printf("Requisição recebida para o estoque do produto ID: %v", idProduto)

	produto, existe := estoque[idProduto]

	if existe {
		return produto, nil
	}

	return nil, fmt.Errorf("estoque para o produto com ID %s não encontrado", idProduto)
}

func main() {
	porta := ":50052"
	lis, err := net.Listen("tcp", porta)
	if err != nil {
		log.Fatalf("Falha ao escutar na porta %s: %v", porta, err)
	}

	s := grpc.NewServer()

	pb.RegisterInventarioServer(s, &servidor{})

	log.Printf("Servidor Inventário escutando em %v", lis.Addr())

	if err := s.Serve(lis); err != nil {
		log.Fatalf("Falha ao iniciar o servidor: %v", err)
	}
}