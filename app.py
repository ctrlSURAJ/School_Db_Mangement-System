from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_pyfile("config.py")

db = SQLAlchemy(app)

# Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Routes
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400
    student = Student(name=name)
    db.session.add(student)
    db.session.commit()
    return jsonify({"message": "Student added successfully"}), 201

@app.route("/students", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([{"id": s.id, "name": s.name} for s in students])

@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify({"id": student.id, "name": student.name})

# ✅ Create DB and Run App
if __name__ == "__main__":
    if not os.path.exists("database"):
        os.makedirs("database")
    
    with app.app_context():     # ✅ This line is crucial
        db.create_all()

    app.run(debug=True)
