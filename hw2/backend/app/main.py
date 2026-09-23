import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import DateTime, Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class Party(Base):
    __tablename__ = "parties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    size: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(16), default="waiting")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class NewParty(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    size: int = Field(ge=1, le=20, strict=True)

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be blank")
        return value


class UpdateParty(BaseModel):
    status: Literal["seated", "removed"]


class PartyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    size: int
    status: Literal["waiting", "seated", "removed"]
    created_at: datetime


def create_app(database_url: str | None = None) -> FastAPI:
    if database_url is None:
        database_url = os.getenv("DATABASE_URL", f"sqlite:///{Path(__file__).resolve().parents[1] / 'tableturn.db'}")
    engine = create_engine(database_url, connect_args={"check_same_thread": False} if database_url.startswith("sqlite:") else {})
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)

    app = FastAPI(title="TableTurn API")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_methods=["GET", "POST", "PATCH"],
        allow_headers=["Content-Type"],
    )

    def get_session():
        with session_factory() as session:
            yield session

    @app.get("/api/parties", response_model=list[PartyOut])
    def list_parties(status: Literal["waiting", "seated", "removed"] | None = None, db: Session = Depends(get_session)):
        query = select(Party).order_by(Party.created_at, Party.id)
        if status:
            query = query.where(Party.status == status)
        return db.scalars(query).all()

    @app.post("/api/parties", response_model=PartyOut, status_code=status.HTTP_201_CREATED)
    def add_party(payload: NewParty, db: Session = Depends(get_session)):
        party = Party(name=payload.name, size=payload.size, status="waiting", created_at=datetime.now(timezone.utc))
        db.add(party)
        db.commit()
        db.refresh(party)
        return party

    @app.patch("/api/parties/{party_id}", response_model=PartyOut)
    def update_party(party_id: int, payload: UpdateParty, db: Session = Depends(get_session)):
        party = db.get(Party, party_id)
        if party is None:
            raise HTTPException(status_code=404, detail="Party not found")
        if party.status != "waiting":
            raise HTTPException(status_code=409, detail="Party is no longer waiting")
        party.status = payload.status
        db.commit()
        db.refresh(party)
        return party

    return app


app = create_app()
