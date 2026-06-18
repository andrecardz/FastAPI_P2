from sqlalchemy.orm import Session

from app.models.produto import Produto
from app.schemas.produto_schema import ProdutoCreate


class ProdutoRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        return self.db.query(Produto).order_by(Produto.id).all()

    def buscar_por_id(self, produto_id: int):
        return self.db.get(Produto, produto_id)

    def criar(self, produto: ProdutoCreate):
        novo_produto = Produto(**produto.model_dump())
        self.db.add(novo_produto)
        self.db.commit()
        self.db.refresh(novo_produto)
        return novo_produto

    def deletar(self, produto: Produto):
        self.db.delete(produto)
        self.db.commit()
