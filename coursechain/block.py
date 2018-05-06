import os
from collections import OrderedDict
from time import time

from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import datetime

AES.new(os.getenv('GENESIS_BLOCK_AES', 'super-secret-byte-string'))


class Block:
    # TODO Should refactor this class
    """
    A block is - basically - a list of transactions.

    A block has these properties:
      - timestamp: time of creation.
      - previous_hash: previous block hash.
      - hash: this block's hash.
      - transactions: a list of transactions.
      - index
    """
    # Magic methods
    def __init__(self, previous_hash, transactions, index):
        """
        This method performs the mining process.

        Set block properties.
        Create ordered properties OrderedDict.

        :type index: object
        :param previous_hash: previous block hash.
        :param transactions: string list of transactions
        """
        self.timestamp = self.get_now()
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.index = index

    def __str__(self):
        """
        Return a string representation of the ordered properties of this block.
        We need the block to have the same order so the hash is the same when
        creating a new block using this method's return value.

        :return: string
        """
        block_data = self.__get_ordered_properties()
        block_data['hash'] = self.hash

        return unicode(u'Block \n {}'.format(block_data))

    def __hash__(self):
        """Create new hash using timestamp, last hash and data"""
        return unicode(
            SHA256.new(
                '{}{}{}'.format(self.timestamp, self.previous_hash, str(self.__get_ordered_properties()))
            ).hexdigest()
        )

    def to_serializable(self):
        block_dict = self.__get_ordered_properties()
        block_dict['hash'] = self.hash
        return unicode({key: value for key, value in block_dict.items()})

    # Computed properties
    @property
    def hash(self):
        return self.__hash__()

    # Static methods
    @staticmethod
    def get_now():
        return unicode(datetime.datetime.now())

    @classmethod
    def genesis(cls):
        """
        # TODO improve this method so the genesis block has always the same hash
        Create the genesis block
        :return:
        """
        return cls(None, [], 1)

    # Private methods
    def __get_ordered_properties(self):
        """
        Loop through properties to set self.properties key/value pairs.

        :param properties: list of strings that match instance properties
        :return:
        """
        ordered_properties = OrderedDict()
        ordered_properties[u'timestamp'] = self.timestamp
        ordered_properties[u'previous_hash'] = self.previous_hash
        ordered_properties[u'index'] = self.index
        ordered_properties[u'transactions'] = self.transactions

        return ordered_properties


# Neo4j
def set_block_node():
    """'(Chain: 1)-[PRECEDES]->(Chain: 2)'"""
    pass


def set_transaction_relationship():
    pass