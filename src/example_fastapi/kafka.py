from typing_extensions import Annotated
from faststream import FastStream, Depends
from faststream.kafka import KafkaBroker
from example_fastapi.dependencies.services import get_users_service_faststream
from example_fastapi.schemas.user import UserCreate
from example_fastapi.services.user_service import UserService
import os
from dotenv import load_dotenv

load_dotenv()

kafka_url = os.getenv("KAFKA_URL", "localhost:9092")

broker = KafkaBroker(kafka_url)
kafka_app = FastStream(broker)


@broker.subscriber("create-user")
async def on_user_created(
    user_data: UserCreate,
    user_service: Annotated[UserService, Depends(get_users_service_faststream)],
):
    await user_service.create_user(user_data)


@broker.subscriber("source-topic")
@broker.publisher("destination-topic")
async def transform_data(data: dict):
    transformed_data = {
        "id": data.get("id"),
        "email": data.get("email", "").lower(),
        "firstname": data.get("firstname", "").upper(),
        "lastname": data.get("lastname", "").upper(),
        "processor": "transform_data_v1"
    }
    return transformed_data


@broker.subscriber("source-topic")
async def process_user_activity(data: dict):
    user_id = data.get("id")
    email = data.get("email", "")
    print(f"Consumer 2 processing user activity for user {user_id} with email {email}")


@broker.subscriber("source-topic")
async def log_user_data(data: dict):
    print(f"Consumer 3 logging user data: {data}")
