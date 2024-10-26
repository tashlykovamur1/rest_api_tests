from datetime import datetime
from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict


class UserRole(str, Enum):
    GUEST = "Guest"
    PLAYER = "Player"
    ADMINISTRATOR = "Administrator"
    NANNY_MODERATOR = "NannyModerator"
    REGULAR_MODERATOR = "RegularModerator"
    SENIOR_MODERATOR = "SeniorModerator"


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


class ParseMode(str, Enum):
    """Common, Info, Post, Chat"""
    COMMON = "Common"
    INFO = "Info"
    POST = "Post"
    CHAT = "Chat"


class Info(BaseModel):
    model_config = ConfigDict(extra='forbid')
    value: Optional[str] = Field(None)
    parse_mode: Optional[ParseMode] = Field(None, alias='parseMode')


class PagingSettings(BaseModel):
    posts_per_page: int = Field(..., alias='postsPerPage')
    comments_per_page: int = Field(..., alias='commentsPerPage')
    topics_per_page: int = Field(..., alias='topicsPerPage')
    messages_per_page: int = Field(..., alias='messagesPerPage')
    entities_per_page: int = Field(..., alias='entitiesPerPage')


class ColorSchema(str, Enum):
    MODERN = "Modern"
    PALE = "Pale"
    CLASSIC = "Classic"
    CLASSIC_PALE = "ClassicPale"
    NIGHT = "Night"


class Settings(BaseModel):
    color_schema: str = ColorSchema
    nanny_greetings_message: str = Field(None, alias='nannyGreetingsMessage')
    paging: PagingSettings


class UserDetails(BaseModel):
    login: str
    roles: List[UserRole]
    medium_picture_url: str = Field(None, alias='mediumPictureUrl')
    small_picture_url: str = Field(None, alias='smallPictureUrl')
    status: str = Field(None)
    rating: Rating
    online: str
    online: datetime = Field(None)
    name: str = Field(None)
    location: str = Field(None)
    registration: datetime = Field(None)
    icq: str = Field(None)
    skype: str = Field(None)
    original_picture_url: str = Field(None, alias='originalPictureUrl')
    info: Optional[Union[Info, str, None]] = Field(None)
    settings: Settings


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resource: Optional[UserDetails] = None
    metadata: Optional[str] = None
