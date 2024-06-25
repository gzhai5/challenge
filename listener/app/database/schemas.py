from pydantic import BaseModel


class Block(BaseModel):
    id: int
    block_hash: str
    block_height: int
    timestamp: str

    class Config:
        from_attributes = True

class Transaction(BaseModel):
    id: str
    tx_hash: str
    block_id: str

    class Config:
        from_attributes = True

class OpReturnData(BaseModel):
    id: str
    op_return_data: str

    class Config:
        from_attributes = True

class TransactionOpReturn(BaseModel):
    transaction_id: str
    op_return_id: str

    class Config:
        from_attributes = True
