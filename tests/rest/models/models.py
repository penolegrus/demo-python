from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- Auth ---
class AuthRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class AuthFullResponse(BaseModel):
    token: str
    user: Optional['UserResponseDto']

# --- User ---
class UserResponseDto(BaseModel):
    id: Optional[int]
    username: str
    email: str
    role: Optional[str]

class UserRequestDto(BaseModel):
    username: str
    email: str
    password: str
    role: Optional[str]

class UserDto(BaseModel):
    id: Optional[int]
    username: str

# --- Notification ---
class NotificationDto(BaseModel):
    id: Optional[int]
    message: str
    type: Optional[str]
    orderId: Optional[int]
    status: Optional[str]
    createdAt: Optional[datetime]

# --- Ingredient ---
class IngredientRequestDto(BaseModel):
    name: str
    quantity: int

class IngredientResponseDto(BaseModel):
    id: Optional[int]
    name: str
    quantity: int

# --- Order ---
class CreateOrderDto(BaseModel):
    ingredientIds: List[int]
    comment: Optional[str]

class UpdateOrderStatusRequest(BaseModel):
    status: str

class OrderResponse(BaseModel):
    id: Optional[int]
    user: Optional[UserDto]
    ingredients: Optional[List[IngredientResponseDto]]
    createdAt: Optional[datetime]
    status: Optional[str]
    comment: Optional[str]

# --- Message ---
class MessageRequestDto(BaseModel):
    senderId: int
    receiverId: int
    content: str

class MessageResponseDto(BaseModel):
    id: Optional[int]
    content: str
    sentAt: Optional[datetime]
    sender: Optional[UserDto]
    receiver: Optional[UserDto]

# Для вложенных моделей
AuthFullResponse.update_forward_refs()
OrderResponse.update_forward_refs()
MessageResponseDto.update_forward_refs() 