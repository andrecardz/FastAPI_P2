from sqlalchemy.orm import Session

from app.repositories.produto_repository import ProdutoRepository
from app.schemas.produto_schema import ProdutoCreate


class ProdutoService:
    def __init__(self, db: Session):
        self.repository = ProdutoRepository(db)

    def listar(self):
        return self.repository.listar()

    def buscar_por_id(self, produto_id: int):
        return self.repository.buscar_por_id(produto_id)

    def criar(self, produto: ProdutoCreate):
        return self.repository.criar(produto)

    def deletar(self, produto_id: int):
        produto = self.repository.buscar_por_id(produto_id)
        if produto is None:
            return False
        self.repository.deletar(produto)
        return True
