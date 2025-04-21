from sqlalchemy import Column, Float, ForeignKey, Table, String, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Jugadores(Base):
    __tablename__ =  "JUGADORES"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
