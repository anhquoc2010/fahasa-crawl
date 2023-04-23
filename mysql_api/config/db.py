from sqlalchemy import create_engine, MetaData
from dotenv.main import load_dotenv
import os

load_dotenv()
MYSQL_DATABASE=os.getenv("MYSQL_DATABASE")
MYSQL_USER=os.getenv("MYSQL_USER")
MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD")
if os.environ.get('DOCKER_CONTAINER') == "true":
    MYSQL_HOST = os.getenv('LOCALHOSTDOCKER')
else:
    MYSQL_HOST = os.getenv('LOCALHOST')

string_connect = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"

engine = create_engine(string_connect)

meta = MetaData()

conn = engine.connect()