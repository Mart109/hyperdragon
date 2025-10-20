from pydantic import BaseModel
from datetime import datetime

class UserProfile(BaseModel):
    user_id: int
    username: str
    first_name: str
    level: int = 1
    experience: int = 0
    coins: int = 100
    created_at: datetime
    last_login: datetime