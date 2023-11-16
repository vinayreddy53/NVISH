from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'data.db'

# Cache dictionary to store key-value pairs temporarily
cache = {}

# Function to fetch data from the database or cache
def get_data(key):
    if key in cache:
        return cache[key]
    else:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM data WHERE key=?', (key,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            cache[key] = {'key': result[1], 'value': result[2]}
            return cache[key]
        else:
            return None

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
    
    # Update cache with the new data
    cache[data['key']] = {'key': data['key'], 'value': data['value']}
    
    return jsonify({'message': 'Data saved successfully'})

# Endpoint to retrieve data based on key
@app.route('/get/<key>', methods=['GET'])
def get(key):
    result = get_data(key)
    if result:
        return jsonify(result)
    else:
        return jsonify({'message': 'Data not found'}), 404

# Endpoint to delete data based on key
@app.route('/delete/<key>', methods=['DELETE'])
def delete(key):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM data WHERE key=?', (key,))
    conn.commit()
    conn.close()
    
    # Remove data from cache on deletion
    if key in cache:
        del cache[key]
    
    return jsonify({'message': 'Data deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)

