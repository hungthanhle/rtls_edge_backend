from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Database Configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///tag_data.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Models
class Tag(Base):
    __tablename__ = "tags"

    tag_id = Column(String, primary_key=True, index=True)
    description = Column(String)
    last_cnt = Column(Integer)
    last_seen = Column(DateTime)

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database Initialization
def init_db():
    Base.metadata.create_all(bind=engine)
    
    # Initialize with default tags
    db = SessionLocal()
    default_tags = [
        Tag(
            tag_id="fa451f0755d8",
            description="Helmet Tag for worker A",
            last_cnt=0,
            last_seen=datetime.datetime.now()
        ),
        Tag(
            tag_id="fb892e1866c9",
            description="Helmet Tag for worker B",
            last_cnt=0,
            last_seen=datetime.datetime.now()
        ),
        Tag(
            tag_id="fc234a7944b2",
            description="Helmet Tag for worker C",
            last_cnt=0,
            last_seen=datetime.datetime.now()
        )
    ]
    
    for tag in default_tags:
        existing = db.query(Tag).filter(Tag.tag_id == tag.tag_id).first()
        if not existing:
            db.add(tag)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
