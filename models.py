import datetime
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)

class LinkToken(Base):
    __tablename__ = "link_tokens"
    token = Column(String, primary_key=True)
    tg_id = Column(BigInteger, ForeignKey("users.tg_id"))
    link_key = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class LinkClick(Base):
    __tablename__ = "link_clicks"
    id = Column(Integer, primary_key=True)
    token = Column(String, ForeignKey("link_tokens.token"))
    tg_id = Column(BigInteger, nullable=True)
    link_key = Column(String, nullable=True)
    clicked_at = Column(DateTime, default=datetime.datetime.utcnow)
    ip = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)

def init_db(db_url="sqlite:///family_bot.db"):
    # support sqlite with check_same_thread, fallback to generic engine for other DBs
    if db_url.startswith("sqlite"):
        engine = create_engine(db_url, connect_args={"check_same_thread": False})
    else:
        engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session
