from flask import Flask, jsonify, request, redirect

from coursechain.blockchain import Blockchain

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

blockchain = Blockchain()


@app.route('/blocks')
def blocks():
    return jsonify([block.to_serializable() for block in blockchain.chain[:50]])  # limit results


@app.route('/mine', methods=['POST'])
def mine():
    transactions = request.form['transactions']

    blockchain.mine(transactions)

    return redirect('/blocks')
