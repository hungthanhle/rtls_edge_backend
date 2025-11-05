from fastapi import FastAPI, HTTPException, Depends
import socket
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db import SessionLocal, Tag, get_db
from typing import List
import datetime

app = FastAPI(title="RTLS Edge Tag Management")

# Pydantic models
class TagCreate(BaseModel):
    id: str
    description: str

class TagResponse(BaseModel):
    tag_id: str
    description: str
    last_cnt: int
    last_seen: datetime.datetime | None

    class Config:
        from_attributes = True

# API endpoints
@app.post("/tags", response_model=TagResponse)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    existing_tag = db.query(Tag).filter(Tag.tag_id == tag.id).first()
    if existing_tag:
        raise HTTPException(status_code=400, detail="Tag already registered")
    
    db_tag = Tag(
        tag_id=tag.id,
        description=tag.description,
        last_cnt=0,
        last_seen=None
    )
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

@app.get("/tags", response_model=List[TagResponse])
def get_tags(db: Session = Depends(get_db)):
    return db.query(Tag).all()

@app.get("/tag/{tag_id}", response_model=TagResponse)
def get_tag(tag_id: str, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.tag_id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@app.get("/health")
def health_check():
    return {
        "status": "OK",
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.post("/simulator/refresh")
def refresh_simulator_tags():
    """Manually trigger simulator to refresh tags from database"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 5000))
            s.send("REFRESH".encode('utf-8'))
        return {"status": "success", "message": "Refresh command sent to simulator"}
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to communicate with simulator: {str(e)}"
        )
