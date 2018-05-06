import unittest

from hamcrest import *
from mock import patch

from coursechain.blockchain import Blockchain, BlockchainError
from coursechain.block import Block


class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.blockchain_0 = Blockchain()
        self.blockchain_1 = Blockchain()

    def tearDown(self):
        pass

    # Test __init__
    #
    # ------------------------------------------------------------------------------------------------------------------
    def test___init___0(self):
        """Should have a chain property."""
        new_bc = Blockchain()

        assert_that(new_bc.chain, is_(not_none()))

    def test___init___1(self):
        """Should have a chain of length == 1."""
        new_bc = Blockchain()

        assert_that(len(new_bc.chain), is_(equal_to(1)))

    def test___init___2(self):
        """Should set a Block instance as the first element of the chain."""
        new_bc = Blockchain()

        assert_that(new_bc.chain[0], is_(instance_of(Block)))

    def test___init___3(self):
        """The first element of the chain should not have a previous hash."""
        new_bc = Blockchain()

        assert_that(new_bc.chain[0].previous_hash, is_(equal_to(None)))

    @patch('coursechain.block.Block.genesis')
    def test___init___4(self, genesis):
        """Should call Block.genesis."""
        Blockchain()

        genesis.assert_called_once()

    # Test append_block
    #
    # ------------------------------------------------------------------------------------------------------------------
    def test_append_block_0(self):
        """Should add a block to the chain."""
        bc = Blockchain()
        block = bc.forge_block([])
        bc.append_block(block)

        assert_that(len(bc.chain), is_(2))

    def test_append_block_1(self):
        """Should add the expected block."""
        bc = Blockchain()
        block = bc.forge_block([])
        bc.append_block(block)

        assert_that(bc.chain[1], is_(equal_to(block)))

    def test_append_block_2(self):
        """Should raise BlockchainError if forged_block is NOT instance of Block"""
        assert_that(calling(self.blockchain_1.append_block).with_args('not a block'), raises(BlockchainError))

    # Test forge_block
    #
    # ------------------------------------------------------------------------------------------------------------------
    def test_forge_block_0(self):
        """Should return a Block instance"""
        forged = self.blockchain_0.forge_block([])

        assert_that(forged, is_(instance_of(Block)))

    def test_forge_block_1(self):
        """Should return a Block instance with expected transactions"""
        expected = ['1', '2', '3']
        forged = self.blockchain_0.forge_block(expected)

        for index, tx in enumerate(forged.transactions):
            assert_that(expected[index], is_(equal_to(tx)))

    # Test chain_is_valid
    #
    # ------------------------------------------------------------------------------------------------------------------
    def test_chain_is_valid_0(self):
        """Should return True if all hashes match"""
        for i in range(10):
            block = self.blockchain_1.forge_block([])
            self.blockchain_1.append_block(block)

        # print([f.__str__() for f in self.blockchain_1.chain])

        assert_that(self.blockchain_0.chain_is_valid(self.blockchain_1.chain), is_(equal_to(True)))

    def test_chain_is_valid_1(self):
        """Should return False if chain is corrupted."""
        for i in range(10):
            block = self.blockchain_1.forge_block([])
            self.blockchain_1.append_block(block)

        self.blockchain_1.chain[5] = self.__invalid_block()

        assert_that(self.blockchain_0.chain_is_valid(self.blockchain_1.chain), is_(equal_to(False)))

    # Test replaced_chain
    #
    # ------------------------------------------------------------------------------------------------------------------
    def test_replaced_chain_0(self):
        """Should return True if chain was replaced"""
        b = self.blockchain_1.forge_block([])
        self.blockchain_1.append_block(b)
        replaced_chain = self.blockchain_0.replaced_chain(self.blockchain_1.chain)

        assert_that(replaced_chain, is_(equal_to(True)))

    def test_replaced_chain_1(self):
        """Should return False if chain was NOT replaced"""
        self.blockchain_0.forge_block([])
        replaced_chain = self.blockchain_0.replaced_chain(self.blockchain_1.chain)

        assert_that(replaced_chain, is_(equal_to(False)))

    def test_replaced_chain_2(self):
        """Should raise BlockchainError if input chain is not valid"""
        for i in range(10):
            block = self.blockchain_1.forge_block([])
            self.blockchain_1.append_block(block)

        self.blockchain_1.chain[5] = self.__invalid_block()

        # print([f.__str__() for f in self.blockchain_1.chain])

        assert_that(
            calling(self.blockchain_0.replaced_chain).with_args(self.blockchain_1.chain),
            raises(BlockchainError)
        )

    def test_replace_chain_3(self):
        """Should raise BlockchainError if self.chain is not valid TODO ???? Should it"""
        self.skipTest('TODO')

    # Test mine
    #
    # ------------------------------------------------------------------------------------------------------------------
    @patch('coursechain.blockchain.Blockchain.forge_block')
    def test_mine_0(self, forge_block):
        self.skipTest("TODO fails for receiving <MagicMock name='forge_block()' id='4523594448'> instead of Block")
        """Should call forge_block with transactions"""
        transactions = ['1']
        self.blockchain_0.mine(transactions)
        forge_block.assert_called_with(transactions)

    @patch('coursechain.blockchain.Blockchain.append_block')
    def test_mine_1(self, append_block):
        self.skipTest("TODO fails for receiving <MagicMock name='forge_block()' id='4523594448'> instead of Block")
        """Should call append_block with forged block"""
        pass

    # Private methods/helpers
    #
    # ------------------------------------------------------------------------------------------------------------------
    def __invalid_block(self):
        return Block('00011MUAJAJA', [], 5)
