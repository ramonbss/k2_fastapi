from sqlalchemy import ForeignKey, create_engine, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from ..core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
DatabaseSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    role = Column(String)
    token = Column(String)

    purchases = relationship(
        "Purchase", back_populates="user", cascade="all, delete-orphan"
    )


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="purchases")

    def to_string(self):
        import json

        return json.dumps(
            {
                "id": self.id,
                "item": self.item,
                "price": self.price,
            }
        )


Base.metadata.create_all(bind=engine)
