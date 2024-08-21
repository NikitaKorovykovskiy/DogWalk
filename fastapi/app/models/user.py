import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID


metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(255)),
    sqlalchemy.Column("last_name", sqlalchemy.String(255)),
    sqlalchemy.Column("email", sqlalchemy.String(255)),
    sqlalchemy.Column("password", sqlalchemy.String(255)),
)

tokens = sqlalchemy.Table(
    "tokens",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "token",
        UUID(as_uuid=False),
        server_default=sqlalchemy.text("uuid_generate_v4()"),
        unique=True,
        nullable=False,
        index=True,
    ),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
)

prodct = sqlalchemy.Table(
    "product",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(255)),
    sqlalchemy.Column("description", sqlalchemy.String(255)),
    sqlalchemy.Column("price", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("count", sqlalchemy.Integer, nullable=True),
)