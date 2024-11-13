from flask import Flask, jsonify, request, abort
from models import db, User, SessionLocal, init_db
import os

# Initialize Flask app and configure SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('connection_string')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize the database
with app.app_context():
    init_db()

# Route to get all users
@app.route('/user', methods=['GET'])
def get_users():
    session = SessionLocal()  # Create a session instance
    users = session.query(User).all()
    session.close()  # Close session to release resources
    return jsonify([{
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "access": user.access
    } for user in users])

# Sample route to create a user
@app.route('/create/user', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        access=data['access']
    )
    session = SessionLocal()
    session.add(new_user)
    session.commit()
    session.close()
    return jsonify({"message": "User created successfully"}), 201

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
