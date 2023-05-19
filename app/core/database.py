#mongo
from urllib.parse import quote
import motor.motor_asyncio
from starlette.config import Config

config = Config('.env')

        
mongo_uri = "mongodb://{}:{}@{}:{}/".format(
    config('mongo_id'), config('mongo_pw'), config('mongo_ip'), config('mongo_port')
    )

client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
db = client.eventAnalysis