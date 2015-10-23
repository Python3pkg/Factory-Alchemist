from sqlalchemy import create_engine, MetaData, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///')
metadata = MetaData(bind=engine)
BaseModel = declarative_base(metadata=metadata)
Session = sessionmaker(bind=engine, autoflush=True, autocommit=False)


class Spam(BaseModel):
    __tablename__ = 'spam'

    id = Column(Integer, primary_key=True)
    purpose = Column(String)
    flavor = Column(Integer, nullable=False)


class Ham(BaseModel):
    __tablename__ = 'ham'

    id = Column(Integer, primary_key=True)
    spam_id = Column(Integer, ForeignKey('spam.id'), nullable=False)
