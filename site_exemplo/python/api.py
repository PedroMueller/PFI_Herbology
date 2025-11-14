from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import controller

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})

@app.route('/')
def home():
    return "Welcome to the API!"

@app.route('/data', methods=['GET'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_data():
    # Example data
    data = controller.get_users()
    return jsonify(data)

@app.route('/submit', methods=['POST'])
def submit_data():
    if request.is_json:
        received_data = request.get_json()
        # Process the received data
        return jsonify({"status": "success", "received_data": received_data})
    return jsonify({"status": "error", "message": "Request must be JSON"}), 400

if __name__ == '__main__':
    app.run(debug=True)