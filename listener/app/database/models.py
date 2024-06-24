import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .engine import Base


class Block(Base):
    __tablename__ = "blocks"

    id = Column(String, primary_key=True,  default=lambda: str(uuid.uuid4()))
    block_hash = Column(String(64), unique=True, nullable=False)
    block_height = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    transactions = relationship("Transaction", back_populates="block")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True,  default=lambda: str(uuid.uuid4()))
    tx_hash = Column(String(64), unique=True, nullable=False)
    block_id = Column(String, ForeignKey("blocks.id"))
    block = relationship("Block", back_populates="transactions")


class OpReturnData(Base):
    __tablename__ = "op_return_data"

    id = Column(String, primary_key=True,  default=lambda: str(uuid.uuid4()))
    op_return_data = Column(String(255), index=True, nullable=False)


class TransactionOpReturn(Base):
    __tablename__ = "transaction_op_return"

    transaction_id = Column(String, ForeignKey("transactions.id"), primary_key=True)
    op_return_id = Column(String, ForeignKey("op_return_data.id"), primary_key=True)
