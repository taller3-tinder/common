from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum
from typing import List


class Genre(Enum):
    WOMAN = "Woman"
    MAN = "Man"
    OTHER = "Other"


class Tags(Enum):
    ANIMALS = "Animals"
    SPORT = "Sport"
    UNIVERSITY = "University"
    WORKAHOLIC = "Workaholic"
    SMOKER = "Smoker"
    PARTY = "Party"
    COFFEE = "Coffee"
    MUSIC = "Music"
    LGBTIQ = "LGBTIQ+"
    GYM = "Gym"


class RegisterUser(BaseModel):
    name: str = Field(example="Camile")
    surname: str = Field(example="Buena Onda")
    description: str = Field(example="I like having fun!")
    date_of_birth: str = Field(example="03-03-2000")
    photo: str = Field(description="base64 codified photo.",
                       example='base64-photo')
    genre: Genre = Field(example="Other")
    preffered_genre: Genre = Field(example="Woman")
    tags: List[Tags] = Field(example=["University", "Sport", "Music"])

    @validator('date_of_birth')
    def validate_date_of_birth(cls, v):
        expected_format = "%d-%m-%Y"
        try:
            datetime.strptime(v, expected_format)
        except ValueError:
            raise ValueError(f"Formato de fecha de nacimiento incorrecto."
                             f" Se espera formato {expected_format}")
        return v
