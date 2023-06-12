from flask import Flask, render_template, request
import sqlite3
import os

host = os.getenv('IP', '0.0.0.0')
port = int(os.getenv('PORT', 5000))


app = Flask(__name__)
db_name = 'servers.db'

def create_table():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS servers (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT)')
    conn.commit()
    conn.close()

def get_servers():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('SELECT * FROM servers')
    servers = c.fetchall()
    conn.close()
    return servers

def add_server(url):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('INSERT INTO servers (url) VALUES (?)', (url,))
    conn.commit()
    conn.close()

def remove_server(server_id):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('DELETE FROM servers WHERE id = ?', (server_id,))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    create_table()
    servers = get_servers()
    return render_template('index.html', servers=servers)

@app.route('/check', methods=['POST'])
def check():
    server_url = request.form['server_url']
    
    # Simulasi pemeriksaan server down
    # Ubah logika ini sesuai dengan kebutuhan Anda
    if server_url == 'http://example.com':
        status = 'Server is down.'
        add_server(server_url)
    else:
        status = 'Server is running normally.'

    servers = get_servers()
    return render_template('result.html', server_url=server_url, status=status, servers=servers)

@app.route('/remove', methods=['POST'])
def remove():
    server_id = request.form['server_id']
    remove_server(server_id)
    servers = get_servers()
    return render_template('index.html', servers=servers)

if __name__ == '__main__':
    app.run(host=host, port=port)
