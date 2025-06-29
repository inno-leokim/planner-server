# from fastapi import APIRouter, Body, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException, status, Request
from database.connection import get_session
from models.events import Event, EventUpdate
from typing import List

from sqlmodel import select

event_router = APIRouter(
    tags=["Events"]
)

events:List[Event] = []

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(session=Depends(get_session)) -> List[Event]:
    statement = select(Event)
    events = session.exec(statement).all()
    return events 

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        return event
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Event with supplied ID does not exist"
    )
    
    
    # for event in events:
    #     if event.id == id:
    #         return event
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Event with supplied ID does not exist"
    #     )

# @event_router.post("/new")
# async def create_event(body: Event = Body(...)) -> dict:
#     events.append(body)
#     return {
#         "message": "Event created successfully"
#     }

@event_router.post("/new")
async def create_event(new_event: Event, session=Depends(get_session)) -> dict:
    
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    
    return {
        "message": "Event created successfully"
    }
    
    
@event_router.put("/edit/{id}", response_model=Event)
async def update_event(id: int, new_data: EventUpdate, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        event_data = new_data.model_dump(exclude_unset=True)
        for key, value in event_data.items():
            setattr(event, key, value) #event.key = value
        session.add(event)
        session.commit()
        session.refresh(event)
    
        return event 
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )
    
@event_router.delete("/{id}")
async def delete_event(id: int, session=Depends(get_session)) -> dict:
    event = session.get(Event, id)
    
    if event:
        session.delete(event)
        session.commit()
        return {
            "message": "Event deleted successfully."
        }
    
    # for event in events:
    #     if event.id == id:
    #         events.remove(event)
    #         return {
    #             "message": "Event deleted susccessfully"
    #         }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )
    
@event_router.delete("/")
async def delete_all_events(session=Depends(get_session)) -> dict:
    # events.clear()
    deleted_count = session.query(Event).delete()
    session.commit()
    
    if deleted_count > 0:
        return {
            "message": f"Events delete {deleted_count} successfully"
        }
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Events do not exist at all"
    )