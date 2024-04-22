from pydantic import BaseModel, Field
from enum import Enum


class TypeOfSwipe(str, Enum):
    LIKE = "Like"
    DISLIKE = "Dislike"


class SwipeBase(BaseModel):
    swiper: str = Field(description="ID from the User that made the swipe.")
    swiped: str = Field(description="ID from the User"
                        " that was evaluated by the swiper.")
    type: TypeOfSwipe
