from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import jwt
import datetime
from functools import wraps

# https://www.youtube.com/watch?v=WxGBoY5iNXY

# Create the application instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisismysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///d:\\hpe\\git\\olivier\\rest\\database.db'

db = SQLAlchemy(app)

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
    
    return jsonify({'users' : output})

@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_user(current_user, public_id):

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user' : user_data})

@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=0)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})

@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'})

@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def modify_user(current_user, public_id):

    data = request.get_json()

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})
    
    user.admin = data['admin']

    db.session.commit()

    return jsonify({'message' : 'User has been modified!'})

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    print("username: {} password: {}".format(auth.username, auth.password))
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-authenticate' : 'Basic realm = "Login required!"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-authenticate' : 'Basic realm = "Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=5)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-authenticate' : 'Basic realm = "Login required!"'})


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)