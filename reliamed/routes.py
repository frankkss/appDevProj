from reliamed import app
from flask import render_template, redirect, url_for, flash, request
from reliamed.models import Pharmaceuticals, User
from reliamed.forms import RegisterForm
from reliamed import db

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    products = Pharmaceuticals.query.all()
    return render_template('market.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            print(f'There was an error with creating a user: {err_msg}')

    return render_template('register.html', form=form)

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