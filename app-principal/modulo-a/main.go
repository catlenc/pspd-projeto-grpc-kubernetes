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
	pb.UnimplementedCatalogoServer 
}

var produtos = map[string]*pb.InfoBasicaResponse{
	"1": {Id: "1", Nome: "Mouse Gamer Pro", Descricao: "Mouse óptico com 16.000 DPI"},
	"2": {Id: "2", Nome: "Teclado Mecânico RGB", Descricao: "Teclado com switches blue e iluminação customizável"},
}

func (s *servidor) GetInfoBasica(ctx context.Context, req *pb.ProdutoRequest) (*pb.InfoBasicaResponse, error) {
	idProduto := req.GetId()
	log.Printf("Requisição recebida para o produto ID: %v", idProduto)

	produto, existe := produtos[idProduto]

	if existe {
		return produto, nil
	}

	return nil, fmt.Errorf("produto com ID %s não encontrado", idProduto)
}

func main() {
	porta := ":50051"
	lis, err := net.Listen("tcp", porta)
	if err != nil {
		log.Fatalf("Falha ao escutar na porta %s: %v", porta, err)
	}

	s := grpc.NewServer()

	pb.RegisterCatalogoServer(s, &servidor{})

	log.Printf("Servidor Catálogo escutando em %v", lis.Addr())

	if err := s.Serve(lis); err != nil {
		log.Fatalf("Falha ao iniciar o servidor: %v", err)
	}
}