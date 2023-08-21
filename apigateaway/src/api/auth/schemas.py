from pydantic import BaseModel, EmailStr, Field, SecretStr, validator


class UserRegister(BaseModel):
    username: str = Field(max_length=40)
    email: EmailStr
    password: SecretStr
    confirmPassword: SecretStr
    firstName: str = Field(max_length=40)
    lastName: str = Field(max_length=40)

    @classmethod
    @validator("confirmPassword")
    def passwords_match(cls, v, values, **kwargs):
        if v != values["password"]:
            raise ValueError("passwords do not match")
        return v


class UserCreated(BaseModel):
    username: str
    email: str
    firstName: str
    lastName: str


class UserLogin(BaseModel):
    username: str
    password: str
