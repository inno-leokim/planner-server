# from pydantic import BaseModel
# from typing import List

# class Event(BaseModel):
#     id: int
#     title: str
#     image: str 
#     description: str 
#     tags: List[str]
#     location: str
    
#     class Config:
#         schema_extra = {
#             "example": {
#                 "titie": "FastAPI Book launch",
#                 "image": "https:linktomyimage.com/image.png",
#                 "description": "We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifits!",
#                 "tags": ["python", "fastapi", "book", "launch"],        
#                 "location": "Google Meet"
#             }
#         }

from sqlmodel import JSON, SQLModel, Field, Column
from typing import Optional, List
class Event(SQLModel, table=True):
    # None이 없으면 필수값이 되어 버린다.
    id: int = Field(default=None, primary_key=True)
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    # tags: str  # Store JSON as string
    tags: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    location: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {  # 최신 Pydantic v2 기준
            "example": {
                "title": "FastAPI Book launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
                "tags": '["python", "fastapi", "book", "launch"]',
                "location": "Google Meet"
            }
        }

class EventUpdate(SQLModel):
    # None이 없으면 필수값이 되어 버린다.
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "titie": "FastAPI Book launch",
                "image": "https:linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifits!",
                "tags": ["python", "fastapi", "book", "launch"],        
                "location": "Google Meet"
            }
        }