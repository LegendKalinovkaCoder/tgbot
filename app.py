from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clicker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class UserScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=True, nullable=False)
    score = db.Column(db.Integer, default=0)

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/api/update_score', methods=['POST'])
def update_score():
    data = request.json
    user_id = data.get('user_id')
    score = data.get('score')

    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    user = UserScore.query.filter_by(user_id=user_id).first()
    if user:
        user.score = score
    else:
        user = UserScore(user_id=user_id, score=score)
        db.session.add(user)
    
    db.session.commit()
    return jsonify({'message': 'Score updated successfully!'})

@app.route('/api/get_score/<user_id>', methods=['GET'])
def get_score(user_id):
    user = UserScore.query.filter_by(user_id=user_id).first()
    if user:
        return jsonify({'user_id': user.user_id, 'score': user.score})
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
