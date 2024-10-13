import uuid
from datetime import date, datetime

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    birthdate: date | None = Field(default=None)
    phone_number: str | None = Field(default=None, max_length=15)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str = Field(min_length=1, max_length=255)


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


class Team(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    size: int = Field(default=0)
    players: list[User] = Relationship(back_populates="team")


class SportEquipmentType(SQLModel, table=True):
    # Ball, field
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    description: str = Field(max_length=255)


class SportEquipment(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    description: str = Field(max_length=255)
    type: SportEquipmentType | None = Relationship(back_populates="sport_equipment")


class Sport(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    sport_equipment_needed: list[SportEquipment] | None = Relationship(back_populates="sport")


class Match(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    tournament_id: uuid.UUID = Field(foreign_key="tournament.id", nullable=False, ondelete="CASCADE")
    # tournament: Tournament = Relationship(back_populates="matches", cascade="all, delete-orphan")
    round_number: int = Field(default=1)
    time: datetime | None = Field(default=None)
    team1_id: uuid.UUID | None = Field(default=None, foreign_key="team.id")
    team2_id: uuid.UUID | None = Field(default=None, foreign_key="team.id")
    team1_score: int = Field(default=0)
    team2_score: int = Field(default=0)
    winner_id: uuid.UUID | None = Field(default=None, foreign_key="team.id")
    reserved_equipment_id: uuid.UUID | None = Field(default=None, foreign_key="sport_equipment.id")


class TournamentBase(SQLModel):
    name: str = Field(max_length=255)
    sport: Sport | None = Relationship(back_populates="tournaments")
    location: str = Field(max_length=255)
    datetime_begin: datetime | None = Field(default=None)
    datetime_end: datetime | None = Field(default=None)
    description: str | None = Field(default=None, max_length=1000)
    players: list[User] = Relationship(back_populates="tournament")


class TournamentCreate(TournamentBase):
    pass


class TournamentUpdate(TournamentBase):
    name: str | None = Field(default=None, max_length=255)
    sport: str | None = Field(default=None, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    datetime_begin: datetime | None = Field(default=None)
    datetime_end: datetime | None = Field(default=None)
    description: str | None = Field(default=None, max_length=1000)


class Tournament(TournamentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    sport: Sport | None = Relationship(back_populates="tournaments")
    location: str = Field(max_length=255)
    datetime_begin: datetime | None = Field(default=None)
    datetime_end: datetime | None = Field(default=None)
    num_teams: int = Field(default=0)
    teams: list[Team] = Relationship(back_populates="tournament")
    description: str | None = Field(default=None, max_length=1000)
    # matches: list[Match] = Relationship(back_populates="tournament")


class TournamentPublic(TournamentBase):
    id: uuid.UUID
    organizer_id: uuid.UUID


class TournamentsPublic(SQLModel):
    data: list[TournamentPublic]
    count: int
