from flask import Flask, request, jsonify

app = Flask(__name__)

# Pre-shared key (this could be loaded from a secure location)
pre_shared_key = "secret_key"

@app.route('/authorize', methods=['POST'])
def authorize():
    # Get the authorization header from the request
    auth_header = request.headers.get('Authorization')

    # Check if the header matches the pre-shared key
    if auth_header == pre_shared_key:
        return jsonify({'message': 'Authorized!'})
    else:
        return jsonify({'message': 'Unauthorized'}), 401

if __name__ == '__main__':
    app.run(debug=True)
