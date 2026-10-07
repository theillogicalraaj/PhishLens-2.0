from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RegisterIn(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=160)
    password: str = Field(min_length=8, max_length=128)

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    created_at: datetime

class CampaignCreate(BaseModel):
    name: str = Field(min_length=3, max_length=180)
    scenario: str = Field(default="Password Reset", max_length=80)
    subject: str = Field(min_length=3, max_length=220)
    body: str = Field(min_length=10, max_length=12000)

class RecipientCreate(BaseModel):
    display_name: str = Field(min_length=2, max_length=160)
    email: EmailStr
    department: str = Field(default="General", max_length=100)

class EventIn(BaseModel):
    recipient_id: int
    event_type: str = Field(pattern="^(delivered|opened|clicked|reported|completed)$")

class CaseUpdate(BaseModel):
    status: str = Field(pattern="^(draft|active|completed|archived)$")

