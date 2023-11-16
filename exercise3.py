
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'data.db'

# Endpoint to save key/value pair into the database
@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    if 'key' not in data or 'value' not in data:
        return jsonify({'message': 'Invalid data format'}), 400
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO data (key, value) VALUES (?, ?)', (data['key'], data['value']))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Data saved successfully'})

# Endpoint to retrieve data based on key from the database
@app.route('/get/<key>', methods=['GET'])
def get(key):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM data WHERE key=?', (key,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return jsonify({'key': result[1], 'value': result[2]})
    else:
        return jsonify({'message': 'Data not found'}), 404

# Endpoint to delete data based on key from the database
@app.route('/delete/<key>', methods=['DELETE'])
def delete(key):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM data WHERE key=?', (key,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Data deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)


# Before run this module need to create database in sqllite with name data.db to done this run below code sinpet with this command "python create_db.py" then 
'''
import sqlite3

# Create a connection to the database (this will create a new file if it doesn't exist)
conn = sqlite3.connect('data.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create the 'data' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT NOT NULL,
        value TEXT NOT NULL
    )
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database 'data.db' with table 'data' created successfully.")

'''
##################################################################33
'''
{
    "key": "5",
    "value": "Sudha"
}

'''
