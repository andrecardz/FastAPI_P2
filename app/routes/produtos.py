from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.produto_schema import ProdutoCreate, ProdutoResponse
from app.services.produto_service import ProdutoService


router = APIRouter(prefix="/produtos", tags=["produtos"])


def get_produto_service(db: Session = Depends(get_db)):
    return ProdutoService(db)


@router.get("", response_model=list[ProdutoResponse])
def listar_produtos(service: ProdutoService = Depends(get_produto_service)):
    return service.listar()


@router.post("", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(
    produto: ProdutoCreate,
    service: ProdutoService = Depends(get_produto_service),
):
    return service.criar(produto)


@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(
    produto_id: int,
    service: ProdutoService = Depends(get_produto_service),
):
    produto = service.buscar_por_id(produto_id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(
    produto_id: int,
    service: ProdutoService = Depends(get_produto_service),
):
    removido = service.deletar(produto_id)
    if not removido:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
