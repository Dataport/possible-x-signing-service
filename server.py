import logging
from flask import Flask, jsonify, request
from jwcrypto import jwk
from werkzeug.exceptions import BadRequest

from utils import normalize, sha256_normalized_vc, sign_doc

# Initialize the Flask application
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

@app.route('/normalize/urdna2015', methods=['POST'])
def normalize_urdna2015():
    '''
    Description: This function normalizes and hashes JSON-LD
        The URDNA2015 normalization and SHA256 hash algorithms are used
    Input: JSON-LD document
    Output: SHA256 hash of the normalized JSON-LD document
    '''
    logger.debug("*** Inside /normalize/urdna2015")
    
    try:
        data = request.json
        logger.debug(f"Received data: {data}")

        doc = data['document']
        logger.debug(f"Document: {doc}")
        
        h = hash_jsonld(doc)
        logger.debug(f"Hash: {h}")

        return jsonify(
            {
                'data': h,
                'message': 'VC document successfully normalized and hashed!'
            }
        ), 201
    
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        return jsonify(
            {
                'error': 'Missing data', 
                'message': str(e)
            }
        ), 400
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify(
            {
                'error': 'Internal Server Error', 
                'message': str(e)
            }
        ), 500

@app.route('/sign', methods=['POST'])
def sign_vc():
    '''
    Description: This function signs a Verifiable Credential (VC) document.
        First, it normalizes and hashes the VC document
        Next, it signs this hash
        Finally, it adds a proof section to the VC document with this signature
    Input: VC document
    Output: VC
    '''
    logger.info("*** Inside /sign")
    
    try:
        data = request.json
        logger.debug(f"Received data: {data}")

        doc = data['document']
        verification_method = data['verification_method']
        logger.debug(f"doc: {doc}")
        logger.debug(f"verification method: {verification_method}")
        
        with open('privkey.pem', 'r') as file:
            priv_key_string = file.read()
            priv_key = jwk.JWK.from_pem(priv_key_string.encode("UTF-8"))

        vc = sign_doc(doc, priv_key, verification_method)
        logger.debug(f"Signed VC: {vc}")

        response = {
            'message': 'VC document successfully signed',
            'data': vc
        }
        return jsonify(response), 201
    
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        return jsonify(
            {
                'error': 'Missing data', 
                'message': str(e)
            }
        ), 400
    
    except FileNotFoundError as e:
        logger.error("Private key file not found.")
        return jsonify(
            {
                'error': 'Private key file not found',
                'message': str(e)
            }
        ), 500

    except Exception as e:
        logger.error(f"Unexpected error in sign_vc: {e}")
        return jsonify(
            {
                'error': 'Internal Server Error', 
                'message': str(e)
            }
        ), 500

def hash_jsonld(doc):
    '''
    Function that normalizes JSON-LD using the URDNA2015 algorithm
    Input: JSON-LD document
    Output: Sha-256 hash of URDNA2015-normalized data
    '''
    logger.debug("*** Inside hash_jsonld")
    
    try:
        normalized_doc = normalize(doc)
        logger.debug(f"Normalized document: {normalized_doc}")
        
        h = sha256_normalized_vc(normalized_doc)
        logger.debug(f"Hash: {h.hexdigest()}")
         
        return h.hexdigest()
    
    except Exception as e:
        logger.error(f"Error in hash_jsonld: {e}")
        raise

# Error handling: 404 Not Found
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Page not found!'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
