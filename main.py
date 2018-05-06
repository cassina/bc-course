#!/usr/bin/env python
import webapp2
from coursechain.blockchain import Blockchain


class MainHandler(webapp2.RequestHandler):
    def get(self):
        blockchain = Blockchain()
        blockchain.forge_block([])
        # print(b.__hash__())
        self.response\
            .write('Chan#1: {} ------> Chain#2: {} ------ |'
                   .format(blockchain.chain[0].__str__(),
                           blockchain.chain[1].__str__()))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)


