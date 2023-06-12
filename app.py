from flask import Flask, render_template, request, redirect
import sqlite3
import socket

app = Flask(__name__)
DATABASE = 'database.db'

def create_database():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS servers
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 url TEXT,
                 status TEXT)''')
    conn.commit()
    conn.close()

def add_server(url, status):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO servers (url, status) VALUES (?, ?)", (url, status))
    conn.commit()
    conn.close()

def get_servers():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM servers")
    servers = c.fetchall()
    conn.close()
    return servers

def check_server_status(server_url):
    try:
        host = socket.gethostbyname(server_url)
        socket.create_connection((host, 80), timeout=5)
        return True  # Server is reachable
    except (socket.gaierror, socket.timeout, ConnectionRefusedError):
        return False  # Server is unreachable

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    server_url = request.form['server_url']
    if check_server_status(server_url):
        status = 'Server is running normally.'
        add_server(server_url, 'Running')
    else:
        status = 'Server is down.'
        add_server(server_url, 'Down')

    return render_template('result.html', server_url=server_url, status=status)

@app.route('/servers')
def servers():
    servers = get_servers()
    return render_template('servers.html', servers=servers)

@app.route('/delete', methods=['POST'])
def delete():
    server_id = request.form['server_id']
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM servers WHERE id=?", (server_id,))
    conn.commit()
    conn.close()
    return redirect('/servers')

if __name__ == '__main__':
    create_database()
    app.run(host='0.0.0.0', port=5000, debug=True)
