from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# DB Config
db_config = {
    'host': 'http://mysql.ns-o9qm0o1m.svc.cluster.local',
    'user': 'root',               # Your DB username
    'password': 'Unitec123', # Your DB password
    'database': 'iscg7444'              # Your DB name
}

def get_db():
    return mysql.connector.connect(**db_config)

# GET /grades - list all grades
@app.route('/grades', methods=['GET'])
def grade_list():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(result)

# GET /grades/<id> - get one grade
@app.route('/grades/<int:id>', methods=['GET'])
def grade_detail(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return jsonify(result)
    else:
        return jsonify({'error': 'Grade not found'}), 404

# POST /grades - add new grade
@app.route('/grades', methods=['POST'])
def grade_add():
    data = request.get_json()
    name = data.get('name')
    grade = data.get('grade')
    if not name or not grade:
        return jsonify({'error': 'Missing name or grade'}), 400
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, grade) VALUES (%s, %s)", (name, grade))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({'id': new_id, 'name': name, 'grade': grade}), 201

# PUT /grades/<id> - update grade
@app.route('/grades/<int:id>', methods=['PUT'])
def grade_update(id):
    data = request.get_json()
    name = data.get('name')
    grade = data.get('grade')
    if not name or not grade:
        return jsonify({'error': 'Missing name or grade'}), 400
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET name = %s, grade = %s WHERE id = %s", (name, grade, id))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    if affected == 0:
        return jsonify({'error': 'Grade not found'}), 404
    return jsonify({'id': id, 'name': name, 'grade': grade})

# DELETE /grades/<id> - delete grade
@app.route('/grades/<int:id>', methods=['DELETE'])
def grade_delete(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    if affected == 0:
        return jsonify({'error': 'Grade not found'}), 404
    return jsonify({'message': f'Grade with id {id} deleted'})

# Main entry
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
