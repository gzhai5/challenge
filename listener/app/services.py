import sys
import time
import uuid
import os
from datetime import datetime
from contextlib import contextmanager
from bitcoinrpc.authproxy import AuthServiceProxy
from database.models import Block, Transaction, TransactionOpReturn
from database.crud import create_block, create_transaction, create_op_return_data, create_transaction_op_return
from database.engine import SessionLocal
from config import settings


@contextmanager
def managed_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        raise
    finally:
        session.close()


class BitcoinCoreService:
    def __init__(self):
        self.rpc_connection = self.connect_rpc()

    def listen(self, first_block_handle=False):
        latest_block_hash = self.rpc_connection.getbestblockhash()
        print(f"Initial block hash: {latest_block_hash}")

        if first_block_handle:
            print(f"Processing the starting block: {latest_block_hash}")
            self.process_block(self.rpc_connection, latest_block_hash)

        while True:
            print("waiting for new block...")
            new_block_hash = self.rpc_connection.getbestblockhash()
            if new_block_hash != latest_block_hash:
                print(f"New block detected: {new_block_hash}")
                self.process_block(self.rpc_connection, new_block_hash)
                latest_block_hash = new_block_hash
            time.sleep(10)
    
    def process_block(self, rpc_connection, block_hash):
        try:
            block = rpc_connection.getblock(block_hash)
        except Exception as e:
            print(f"Failed to retrieve block {block_hash}: {e}")
            return

        with managed_session() as session:
            try:
                block_model = create_block(session, Block(
                    id=str(uuid.uuid4()),
                    block_hash=block_hash,
                    block_height=block['height'],
                    timestamp=datetime.fromtimestamp(block['time']).strftime('%Y-%m-%d %H:%M:%S')
                ))
                print('Block model gets created:', block_model.__dict__)

                for txid in block['tx']:
                    transaction_model = create_transaction(session, Transaction(
                        id=str(uuid.uuid4()),
                        tx_hash=txid,
                        block_id=block_model.id
                    ))
                    print('Transaction model gets created:', transaction_model.__dict__)

                    op_return_data = self.get_op_return_data(rpc_connection, txid)
                    for op_return_hex in op_return_data:
                        op_return_model = create_op_return_data(session, op_return_hex)
                        transaction_op_return_model = create_transaction_op_return(session, TransactionOpReturn(
                            transaction_id=transaction_model.id,
                            op_return_id=op_return_model.id
                        ))
                        print('TransactionOpReturn model gets created:', transaction_op_return_model.__dict__)

                print(f"Block {block_hash} processed successfully")
            except Exception as e:
                print(f"Failed to process block {block_hash}: {e}")
                raise

    @staticmethod
    def connect_rpc():
        try:
            rpc_connection = AuthServiceProxy(settings.rpc_url)
            print("Connected to the bitcoin rpc")
            return rpc_connection
        except Exception as e:
            print(f"Failed to connect to the bitcoin rpc: {e}")
            sys.exit(1)

    @staticmethod
    def get_op_return_data(connection, txid):
        raw_tx = connection.getrawtransaction(txid, True)
        op_return_data = []
        for vout in raw_tx['vout']:
            if vout['scriptPubKey']['type'] == 'nulldata':
                op_return_hex = vout['scriptPubKey']['asm'].split(' ')[1]
                op_return_data.append(op_return_hex)
        return op_return_data
    
bitcoin_core_service = BitcoinCoreService()


