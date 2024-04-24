from pydantic import BaseModel, Field
from enum import Enum


class TypeOfSwipe(str, Enum):
    LIKE = "Like"
    DISLIKE = "Dislike"


class UserSwipe(BaseModel):
    swiped: str = Field(description="ID from the User"
                        " that was evaluated by the swiper.")
    type: TypeOfSwipe


class SwipeBase(UserSwipe):
    swiper: str = Field(description="ID from the User that made the swipe.")
