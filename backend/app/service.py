from fastapi import HTTPException
from sqlalchemy.orm import Session
from loguru import logger
from app.database.models import OpReturnData, Transaction, Block, TransactionOpReturn


class BitcoinService():
    def __init__(self):
        pass
    
    def get_op_return_data(self, op_return_data: str, db: Session):
        op_return_data_hex = self.str_to_hex(op_return_data)
        op_return_records = db.query(OpReturnData).filter(OpReturnData.op_return_data == op_return_data_hex).all()
        if not op_return_records:
            logger.error(f"OP_RETURN data not found for this query: {op_return_data}\n with hex: {op_return_data_hex}")
            raise HTTPException(status_code=404, detail="OP_RETURN data not found for this query.")

        transactions = []
        for op_return in op_return_records:
            transaction_op_return_records = db.query(TransactionOpReturn).filter(TransactionOpReturn.op_return_id == op_return.id).all()
            for transaction_op_return in transaction_op_return_records:
                transaction = db.query(Transaction).filter(Transaction.id == transaction_op_return.transaction_id).first()
                if transaction:
                    block = db.query(Block).filter(Block.id == transaction.block_id).first()
                    if block:
                        transactions.append({
                            "transaction_hash": transaction.tx_hash,
                            "block_hash": block.block_hash
                        })

        return {
            "op_return_data_text": op_return_data,
            "op_return_data_hex": op_return_data_hex,
            "transactions": transactions
        }
    
    @staticmethod
    def str_to_hex(s: str) -> str:
        return s.encode('latin1').hex()


bitcoin_service = BitcoinService()