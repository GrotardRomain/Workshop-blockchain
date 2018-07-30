# On importe toute les librairie pour faire fonctionner le block

# import hashlib
# import json
# from time import time
# from urllib.parse import urlparse
# from uuid import uuid4

# import requests
# from flask import Flask, jsonify, request


class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Crée un nouveau block
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address):

        # Ajoute un nouveau node à la liste des nodes
        


        def valid_chain(self, chain):

        # Determine si le blockchain qu'il a reçu est valide

            last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            
            # Vérifie si le hash du block est correct

            return True

    def resolve_conflicts(self):

        # Prend la plus longue chaine du réseau
        

        # On regarde si la chaine est plus grande que la nôtre
        max_length = len(self.chain)

        # Attrape et vérifie si la chaine du réseau
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Regarde si c'est plus long et si la chaine est valide
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Remplace la chaine si on découvre une nouvelle, valide la chaine plus longue que la notre
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash):
        
        # Crée un nouveau block dans la chaine

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Fait un reset de la liste des transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):

        # Crée une nouvelle transaction
        
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):

        # Hash en SHA256 du block
        

        # Vérifier si le dico est ordonné sinon il hash n'importe comment
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):

        # 'Proof of work'

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        
        # Valide la preuve

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# Instantie Node
app = Flask(__name__)

# Génrere une adresse global et unique
node_identifier = str(uuid4()).replace('-', '')

# Instantie le Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # On fait tourner la proof of work pour atteindre la prochaine preuve
    

    # On recoit une compensation pour avoir trouvé la preuve
    # Le 'sender' est "0" pour signifier qu'on a miné une nouveau coin
    

    # Forge le nouveau block en l'ajoutant à la chaine
    

    response = {
        'message': "Nouveau block forgé",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Vérifie si tout les chamlps sont bien rempli
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Crée une nouvelle transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)