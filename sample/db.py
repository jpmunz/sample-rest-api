from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis

sql = SQLAlchemy()
redis_store = FlaskRedis(decode_responses=True)
