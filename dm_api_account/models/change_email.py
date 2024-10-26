from pydantic import BaseModel, Field, ConfigDict


class ChangeEmail(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str = Field(...)
    password: str = Field(...)
    email: str = Field(...)
