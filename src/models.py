import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime, BigInteger

from src.db import Base


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    target_url = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.now)


class Browser(Base):
    __tablename__ = "browsers"

    id = Column(Integer, primary_key=True)
    user_agent = Column(String, unique=True, index=True)
    browser_family = Column(String, nullable=True)
    os = Column(String, nullable=True)
    device = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)


class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True)
    link_id = Column(Integer, index=True)
    browser_id = Column(Integer, nullable=True)
    ip_address = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)
