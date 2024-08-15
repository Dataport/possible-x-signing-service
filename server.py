from flask import Flask, jsonify, request
from utils import normalize, sha256_normalized_vc

# Initialize the Flask application
app = Flask(__name__)

@app.route('/normalize/urdna2015', methods=['POST'])
def normalize_urdna2015():
    print("*** Inside /normalize/urdna2015")
    data = request.json
    print("Data: ", data)

    doc = data['document']
    print("Doc: ", doc)
    h = hash_jsonld(doc)

    response = {
        'message': 'VC document successfully normalized and hashed!',
        'data': h
    }
    return jsonify(response), 201

def hash_jsonld(doc):
    '''
    Function that normalizes JSON-LD using the URDNA2015 algorithm
    Input: JSON-LD document
    Output: Sha-256 hash of URDNA2015-normalized data
    '''
    print("*** Inside hash_jsonld")
    normalized_doc = normalize(doc)
    print("Normalized doc: ", normalized_doc)
    h = sha256_normalized_vc(normalized_doc)
    print("Hash: ", h.hexdigest())

    return h.hexdigest()

# Error handling: 404 Not Found
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Page not found!'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=2021)
