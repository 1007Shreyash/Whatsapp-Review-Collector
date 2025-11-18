import os
from typing import List, Dict, Optional
from datetime import datetime
from fastapi import FastAPI, Form, Depends, Request, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from twilio.twiml.messaging_response import MessagingResponse

# --- Configuration ---
# Defaults to SQLite for easy local testing. 
# For the assignment submission, change this to your Postgres URL:
# DATABASE_URL = "postgresql://user:password@localhost/dbname"
DATABASE_URL = "sqlite:///./reviews.db"

app = FastAPI(title="WhatsApp Review Collector")

# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database Setup ---
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Models ---
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    contact_number = Column(String, index=True)
    user_name = Column(String)
    product_name = Column(String)
    product_review = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- In-Memory Conversation State ---
# In a production Redis would be better, but a dict is perfect for this assignment scope.
# Structure: { "whatsapp:+123...": { "step": "wait_product", "data": {...} } }
conversation_state: Dict[str, Dict] = {}

# Steps Constants
STEP_START = "start"
STEP_WAIT_PRODUCT = "wait_product"
STEP_WAIT_NAME = "wait_name"
STEP_WAIT_REVIEW = "wait_review"

# --- Routes ---

@app.get("/")
def read_root():
    return {"status": "ok", "message": "WhatsApp Review Backend is running"}

@app.get("/api/reviews")
def get_reviews(db: Session = Depends(get_db)):
    """
    Fetch all reviews from the database.
    """
    reviews = db.query(Review).order_by(Review.created_at.desc()).all()
    return reviews

@app.post("/whatsapp")
async def whatsapp_webhook(From: str = Form(...), Body: str = Form(...), db: Session = Depends(get_db)):
    """
    Handle incoming WhatsApp messages from Twilio.
    """
    sender_id = From
    message_body = Body.strip()
    
    # Initialize response
    resp = MessagingResponse()
    
    # Get current state or initialize
    current_session = conversation_state.get(sender_id)

    # Reset command for debugging
    if message_body.lower() == "reset":
        conversation_state.pop(sender_id, None)
        resp.message("Conversation reset. Say 'Hi' to start over.")
        return str(resp)

    # Logic Flow
    if not current_session:
        # New conversation
        conversation_state[sender_id] = {
            "step": STEP_WAIT_PRODUCT,
            "data": {"contact_number": sender_id}
        }
        resp.message("Which product is this review for?")
    
    elif current_session["step"] == STEP_WAIT_PRODUCT:
        # User sent Product Name
        current_session["data"]["product_name"] = message_body
        current_session["step"] = STEP_WAIT_NAME
        resp.message("What's your name?")
        
    elif current_session["step"] == STEP_WAIT_NAME:
        # User sent Name
        current_session["data"]["user_name"] = message_body
        product_name = current_session["data"]["product_name"]
        current_session["step"] = STEP_WAIT_REVIEW
        resp.message(f"Please send your review for {product_name}.")
        
    elif current_session["step"] == STEP_WAIT_REVIEW:
        # User sent Review
        review_text = message_body
        data = current_session["data"]
        
        # Save to Database
        new_review = Review(
            contact_number=data["contact_number"],
            product_name=data["product_name"],
            user_name=data["user_name"],
            product_review=review_text
        )
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        
        # Clear state
        conversation_state.pop(sender_id, None)
        
        resp.message(f"Thanks {data['user_name']} your review for {data['product_name']} has been recorded.")
        
    else:
        # Fallback for unknown state
        conversation_state.pop(sender_id, None)
        resp.message("Something went wrong. Let's start over. Which product is this review for?")

    return Response(content=str(resp), media_type="application/xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)