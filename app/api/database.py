from sqlalchemy import ForeignKey, create_engine, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from ..core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
DatabaseSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class BaseUser:
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    role = Column(String)
    token = Column(String)


class User(BaseUser, Base):
    __tablename__ = "users"
    purchases = relationship(
        "Purchase", back_populates="user", cascade="all, delete-orphan"
    )


class Admin(BaseUser, Base):
    __tablename__ = "admins"
    reports = relationship(
        "Report", back_populates="admin", cascade="all, delete-orphan"
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


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    status = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("admins.id"), nullable=False)
    admin = relationship("Admin", back_populates="reports")

    def to_string(self):
        import json

        return json.dumps(
            {
                "id": self.id,
                "title": self.title,
                "status": self.status,
            }
        )


Base.metadata.create_all(bind=engine)
