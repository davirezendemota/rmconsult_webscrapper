from typing import Generic, Type, TypedDict, TypeVar

from sqlalchemy import UniqueConstraint, func, text
from sqlmodel import Session, null, select
from sqlmodel.sql.expression import SelectOfScalar
from sqlalchemy.dialects.postgresql import insert

from core.BaseModel import BaseModel
from core.BaseModel import update_model

TModel = TypeVar("TModel", bound=BaseModel)


class PageRef(TypedDict):
    page_number: int
    page_size: int


class Page(Generic[TModel], TypedDict):
    items: list[TModel]
    page_number: int
    page_size: int
    next_page: int | None
    last_page: int
    quantity_itens: int


class BaseRepository(Generic[TModel]):
    def __init__(self, model: Type[TModel], session: Session):
        self.model = model
        self.session = session

    def count(self, *conditions) -> int:
        query = select(func.count()).select_from(self.model).filter(*conditions)
        return self.session.exec(query).first() or 0

    def exists(self, *conditions) -> bool:
        query = select(self.model).filter(*conditions)
        return self.session.exec(query).first() is not None

    def find_all(self) -> list[TModel]:
        query = select(self.model)
        return list(self.session.exec(query).all())

    def find_all_page(self, page: PageRef = PageRef(page_number=1, page_size=25)):
        query = select(self.model)
        return self._build_page(query, page)

    def find_many(self, *conditions) -> list[TModel]:
        query = select(self.model).filter(*conditions)
        return list(self.session.exec(query).all())

    def find_many_page(self, *conditions, page: PageRef):
        query = select(self.model).filter(*conditions)
        return self._build_page(query, page)

    def find_one(self, *conditions) -> TModel | None:
        query = select(self.model).filter(*conditions)
        return self.session.exec(query).first()

    def upsert(self, model: TModel, new_data: dict | None = None) -> TModel:
        if new_data:
            model = update_model(model, new_data)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def upsert_fast(self, model: TModel, new_data: dict | None = None) -> TModel:
        if new_data:
            model = update_model(model, new_data)
        self.session.add(model)
        self.session.flush()
        self.session.refresh(model)
        return model


    def upsert_fast_by(self, conditions: list | tuple, data: dict):
        """
        UPSERT nativo PostgreSQL — genérico e seguro
        - Detecta UniqueConstraint OU colunas unique=True
        - Usa a PK se nada for encontrado
        - Evita qualquer erro de duplicidade
        """
        table = self.model.__table__
        stmt = insert(table).values(**data)

        # 1️⃣ Detecta automaticamente as colunas únicas
        unique_fields = []

        # UniqueConstraint explícitas
        for constraint in table.constraints:
            if isinstance(constraint, UniqueConstraint):
                for col in constraint.columns:
                    unique_fields.append(col.name)

        # Também pega colunas com unique=True
        for col in table.columns:
            if col.unique and col.name not in unique_fields:
                unique_fields.append(col.name)

        # Se não achou, tenta pegar a PK
        if not unique_fields:
            unique_fields = [c.name for c in table.primary_key.columns]

        # Ou deduz pelo condition (caso tenha sido passado)
        if not unique_fields and conditions:
            try:
                unique_fields = [c.left.name for c in conditions]
            except Exception:
                pass

        # Fallback final
        if not unique_fields:
            unique_fields = ["id"]

        # Campos que serão atualizados no conflito
        update_dict = {
            col: stmt.excluded[col]
            for col in data.keys()
            if col not in ("id", "created_at")
        }

        # Monta o UPSERT real
        stmt = stmt.on_conflict_do_update(
            index_elements=unique_fields,
            set_=update_dict
        ).returning(table)

        result = self.session.exec(stmt)
        row = result.first()
        self.session.flush()

        if not row:
            return None

        # Retorna como objeto do modelo (não só o ID)
        if isinstance(row[0], self.model):
            return row[0]
        else:
            # PostgreSQL pode retornar uma tupla simples com os campos
            # então recriamos o modelo com base nas colunas
            return self.model(**row._mapping)

    def upsert_by(self, conditions: list | tuple, data: dict):
        model = self.find_one(*conditions)
        if model:
            model = update_model(model, data)
        else:
            model = self.model(**data)
        return self.upsert(model)

    def bulk_upsert(self, models: list[TModel]) -> list[TModel]:
        self.session.add_all(models)
        self.session.commit()
        for m in models:
            self.session.refresh(m)
        return models

    def bulk_delete(self, models: list[TModel]) -> None:
        for model in models:
            self.session.delete(model)
        self.session.commit()

    def delete(self, model: TModel) -> None:
        self.session.delete(model)
        self.session.commit()

    def hard_delete(self, model: TModel) -> None:
        """Remove permanentemente o registro do banco de dados, ignorando o soft delete."""
        table_name = self.model.__tablename__
        primary_key_value = getattr(model, "id")

        if primary_key_value is None:
            raise ValueError("Não é possível fazer hard delete de um modelo sem ID")

        delete_sql = text(f"DELETE FROM {table_name} WHERE id = :id")
        self.session.execute(delete_sql, {"id": primary_key_value})
        self.session.commit()

    def delete_by(self, *conditions) -> None:
        query = select(self.model).filter(*conditions)
        instances = self.session.exec(query).all()
        for instance in instances:
            self.session.delete(instance)
        self.session.commit()

    def hard_delete_by(self, *conditions) -> None:
        """Remove permanentemente registros do banco de dados por condições, ignorando o soft delete."""

        table_name = self.model.__tablename__

        where_clause = " AND ".join([f"{condition.left.name} = :param_{i}" for i, condition in enumerate(conditions)])
        delete_sql = text(f"DELETE FROM {table_name} WHERE {where_clause}")

        params = {f"param_{i}": condition.right.value for i, condition in enumerate(conditions)}

        self.session.execute(delete_sql, params)
        self.session.commit()

    def hard_bulk_delete(self, models: list[TModel]) -> None:
        """Remove permanentemente múltiplos registros do banco de dados, ignorando o soft delete."""
        if not models:
            return

        table_name = self.model.__tablename__
        ids = [getattr(model, "id") for model in models if getattr(model, "id") is not None]

        if not ids:
            raise ValueError("Nenhum modelo com ID válido encontrado para hard delete")

        placeholders = ", ".join([f":id_{i}" for i in range(len(ids))])
        delete_sql = text(f"DELETE FROM {table_name} WHERE id IN ({placeholders})")

        params = {f"id_{i}": id_value for i, id_value in enumerate(ids)}

        self.session.execute(delete_sql, params)
        self.session.commit()

    def _build_page_query(self, query: SelectOfScalar[TModel], page_number: int, page_size: int):
        if not page_number or page_number < 1:
            raise ValueError("Page number must be greater than 0")
        if not page_size or page_size < 1:
            raise ValueError("Page size must be greater than 0")
        offset = (page_number - 1) * page_size
        limit = page_size
        return query.offset(offset).limit(limit)

    def _build_page(self, query: SelectOfScalar[TModel], page: PageRef) -> Page[TModel]:
        page_number = page.get("page_number")
        page_size = page.get("page_size")

        if page_number is None or page_size is None:
            raise ValueError("Page number and page size are required")

        if hasattr(self.model, "deleted_at"):
            stmt = select(func.count()).select_from(self.model).where(self.model.deleted_at == null())
        else:
            stmt = select(func.count()).select_from(self.model)
        total = self.session.exec(stmt).first()
        total = total if total else 0

        last_page = (total // page_size) + (1 if total % page_size else 0)
        next_page = page_number + 1 if page_number < last_page else None
        query = self._build_page_query(query, page_number, page_size)

        items = list(self.session.exec(query).all())

        return Page(
            items=items,
            page_number=page_number,
            page_size=page_size,
            next_page=next_page,
            last_page=last_page,
            quantity_itens=total,
        )
