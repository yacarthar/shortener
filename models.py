"""database model
"""

from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy


db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_name = os.environ["DB_NAME"]
db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]


url = sqlalchemy.engine.url.URL.create(
    drivername="postgresql",
    username=db_user,
    password=db_pass,
    database=db_name,
    query={
        "unix_sock": "{}/{}/.s.PGSQL.5432".format(
            db_socket_dir,
            instance_connection_name)
    }
)
print(url)
# db = SQLAlchemy(engine_options={"url": url})
db = SQLAlchemy()

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250), nullable=False)
    short_url = db.Column(db.String(250), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
