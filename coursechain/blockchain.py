from block import Block


class Blockchain:
    def __init__(self):
        self.chain = [Block.genesis()]  # Create genesis block and add it to the chain

    # Instance methods
    #
    # ------------------------------------------------------------------------------------------------------------------
    def forge_block(self, transactions):
        """ Forge a new block using transactions param and append it to the current chain.

        :param transactions: list of transactions.
        :return: Block: new forged block.
        """
        forged_block = Block(
            transactions=transactions,
            previous_hash=self.chain[-1].hash,
            index=len(self.chain) + 1,
        )

        return forged_block

    def append_block(self, forged_block):
        """Only accept Block instance and append it to the chain"""
        if not isinstance(forged_block, Block):
            print(forged_block)
            raise BlockchainError('forged_block type should Block.')

        self.chain.append(forged_block)

        return forged_block

    def chain_is_valid(self, chain):
        """ Test integrity of blockchain and each block previous hash to match current block.
        # TODO validate genesis block

        :param chain: Blockchain.chain
        :return: boolean: False if any current block previous_hash does not match previous block hash.
        """
        for index, block in enumerate(chain[1:]):
            # TODO improve this
            if index != 0:
                current = chain[index]
                previous = chain[index - 1]

                if current.previous_hash != previous.hash:
                    return False

        return True

    def replaced_chain(self, chain):
        """ Measure theirs with ours and replace chain with longer chain.

        If the input chain is longer than self.chain, replace chain and return True
        Else return False, chain was not replaced.

        :param chain: Blockchain.chain
        :return: boolean
        """
        ours = len(self.chain)
        theirs = len(chain)

        if not self.chain_is_valid(chain):
            raise BlockchainError('Hashes are not valid')

        if theirs > ours:
            self.chain = chain
            print('Theirs was longer than ours, replacing => \n - Their chain len: {} vs Our chain len: {}'.format(theirs, ours))
            return True

        return False

    def mine(self, transactions):
        # TODO test
        self.append_block(
            self.forge_block(transactions)
        )


class BlockchainError(Exception):
    pass
