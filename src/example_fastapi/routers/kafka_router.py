from fastapi import APIRouter, HTTPException
import asyncio
import json

from example_fastapi.kafka import broker

router = APIRouter(prefix="/kafka", tags=["kafka"])

@router.post("/publish-100-messages")
async def publish_100_messages():
    """Publish 100 test messages to source-topic"""
    try:
        for i in range(1, 101):
            msg = {
                "id": f"message_{i}",
                "email": f"user{i}@example.com",
                "firstname": f"FirstName{i}",
                "lastname": f"LastName{i}",
                "timestamp": asyncio.get_event_loop().time()
            }
            await broker.publish(msg, topic="source-topic")
        
        return {
            "message": f"Successfully published 100 messages to source-topic",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error publishing messages: {str(e)}")

@router.post("/publish-custom-messages")
async def publish_custom_messages(
    count: int = 10,
    topic: str = "source-topic"
):
    """Publish custom number of test messages to specified topic"""
    try:
        if count <= 0 or count > 100:  # Set a reasonable limit
            raise HTTPException(status_code=400, detail="Count must be between 1 and 1000")
        
        for i in range(1, count + 1):
            msg = {
                "id": f"message_{i}",
                "email": f"user{i}@example.com",
                "firstname": f"FirstName{i}",
                "lastname": f"LastName{i}",
                "timestamp": asyncio.get_event_loop().time(),
            }
            # Serialize the message to JSON string before publishing
            await broker.publish(json.dumps(msg), topic=topic)
        
        return {
            "message": f"Successfully published {count} messages to {topic}",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error publishing messages: {str(e)}")