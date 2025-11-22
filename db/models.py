from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase): ...


class URL_Pair(Base):
    __tablename__ = "url_pairs"
    slug: Mapped[str] = mapped_column(primary_key=True)
    original_url: Mapped[str]
