import uuid
from sqlalchemy.orm import Session
from . import models, schemas


def create_block(db: Session, block: schemas.Block):
    db_block = models.Block(
        id=str(uuid.uuid4()),
        block_hash=block.block_hash,
        block_height=block.block_height,
        timestamp=block.timestamp
    )
    db.add(db_block)
    db.commit()
    db.refresh(db_block)
    return db_block

def create_transaction(db: Session, transaction: schemas.Transaction):
    db_transaction = models.Transaction(
        id=str(uuid.uuid4()),
        tx_hash=transaction.tx_hash,
        block_id=transaction.block_id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def create_op_return_data(db: Session, op_return_data: str):
    db_op_return_data = models.OpReturnData(
        id=str(uuid.uuid4()),
        op_return_data=op_return_data
    )
    db.add(db_op_return_data)
    db.commit()
    db.refresh(db_op_return_data)
    return db_op_return_data

def create_transaction_op_return(db: Session, transaction_op_return: schemas.TransactionOpReturn):
    db_transaction_op_return = models.TransactionOpReturn(
        transaction_id=transaction_op_return.transaction_id,
        op_return_id=transaction_op_return.op_return_id
    )
    db.add(db_transaction_op_return)
    db.commit()
    db.refresh(db_transaction_op_return)
    return db_transaction_op_return
