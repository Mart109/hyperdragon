from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum
import uuid
from datetime import datetime

class UserProfile(BaseModel):
    id: str
    username: str
    level: int = 1
    experience: int = 0
    coins: int = 100
    created_at: datetime
    last_login: datetime
