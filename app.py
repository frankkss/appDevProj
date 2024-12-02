from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)

    def __repr__(self):
        return f'Item {self.name}'
    
    
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    return render_template('market.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM ADET_USERS WHERE username = %s AND password = %s', (username, hashed_password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['f_name'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            errorData = {"Username": username, "error": "Invalid Username or Password"}
            return render_template('login.html', data=errorData)
    """
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)