from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__, static_folder="public")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app)

# PostgreSQL configuration
db_config = {
    'host': 'localhost',
    'database': 'road_damage',
    'user': 'postgres',
    'password': 'aristo0407',
}

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "GET" :
        if 'logined' in session :
            return redirect(url_for('maps'))
        return render_template('index.html', error=error)
    else :
        conn = psycopg2.connect(**db_config)

        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM code_access WHERE code = %s", (request.form['code_access'],))
            result = cursor.fetchone()
            if result:
                session["logined"] = True
                return redirect(url_for('maps'))
            else:
                error = "Kode akses salah atau tidak terdaftar"
            
        return render_template('index.html', error=error)

@app.get('/maps')
def maps():

    connection = psycopg2.connect(**db_config)
        
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM detections;")

    maps = cursor.fetchall()

    cursor.close()
    connection.close()    

    if 'logined' not in session :
        return redirect(url_for('login'))
    
    return render_template('maps.html', date_now=datetime.now().strftime("%d/%m/%Y %H:%M"), maps=maps)

@app.get('/logout')
def logout():
    if 'logined' not in session :
        return redirect(url_for('login'))
    session.pop('logined', None)
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)