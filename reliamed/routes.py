from reliamed import app
from flask import render_template
from reliamed.models import Pharmaceuticals

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    products = Pharmaceuticals.query.all()
    return render_template('market.html', products=products)

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