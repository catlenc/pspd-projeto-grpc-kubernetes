package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"encoding/json"
    "net/http"
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

func iniciarServidorHttp() {
    http.HandleFunc("/produto/", func(w http.ResponseWriter, r *http.Request) {
        id := r.URL.Path[len("/produto/"):]
        log.Printf("[REST] Requisição recebida para o produto ID: %v", id)

        produto, existe := produtos[id]
        if existe {
            w.Header().Set("Content-Type", "application/json")
            json.NewEncoder(w).Encode(produto)
        } else {
            http.NotFound(w, r)
        }
    })
    log.Println("Servidor REST Catálogo escutando em :8081")
    http.ListenAndServe(":8081", nil)
}

func main() {
	go iniciarServidorHttp()
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