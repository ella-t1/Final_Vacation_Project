from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional


class RoleName(str, Enum):
    ADMIN = "Admin"
    USER = "User"


@dataclass
class RoleDTO:
    id: int
    name: RoleName


@dataclass
class UserDTO:
    id: int
    first_name: str
    last_name: str
    email: str
    username: Optional[str]
    role_id: int


@dataclass
class CountryDTO:
    id: int
    name: str


@dataclass
class VacationDTO:
    id: int
    country_id: int
    description: str
    start_date: date
    end_date: date
    price: float
    image_name: Optional[str]


@dataclass
class LikeDTO:
    user_id: int
    vacation_id: int


