from flask import Flask, render_template, request, redirect
import sqlite3
import subprocess

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    server_url = request.form['server_url']
    try:
        subprocess.check_output(["ping", "-c", "1", server_url])
        status = 'Server is running normally.'
        add_server(server_url, 'Running')
    except subprocess.CalledProcessError:
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
    app.run(debug=True)
