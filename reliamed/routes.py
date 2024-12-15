from reliamed import app
from flask import render_template, redirect, url_for, flash, request
from reliamed.models import Pharmaceuticals, User
from reliamed.forms import RegisterForm, LoginForm, PurchaseProductForm, SellProductForm
from reliamed import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchased_form = PurchaseProductForm()
    selling_form = SellProductForm()
    if request.method == "POST":
        #Purchase Product Logic
        purchased_product = request.form.get('purchased_product')
        p_product_object = Pharmaceuticals.query.filter_by(name=purchased_product).first()
        if p_product_object:
            if current_user.can_purchase(p_product_object):
                p_product_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_product_object.name} for {p_product_object.price}$", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_product_object.name}!", category='danger')
        #Sell Product Logic
        sold_pharmaceutical = request.form.get('sold_pharmaceutical')
        s_pharmaceutical_object = Pharmaceuticals.query.filter_by(name=sold_pharmaceutical).first()
        if s_pharmaceutical_object:
            if current_user.can_sell(s_pharmaceutical_object):
                s_pharmaceutical_object.sell(current_user)
                flash(f"Congratulations! You sold {s_pharmaceutical_object.name} back to market!", category='success')
            else:
                flash(f"Something went wrong with selling {s_pharmaceutical_object.name}", category='danger')
        
        return redirect(url_for('market_page'))

    if request.method == "GET":
        pharmaceuticals = Pharmaceuticals.query.filter_by(owner=None)
        owned_pharmaceuticals = Pharmaceuticals.query.filter_by(owner=current_user.id)
        return render_template('market.html', pharmaceuticals=pharmaceuticals, purchased_form=purchased_form, owned_pharmaceuticals=owned_pharmaceuticals, selling_form=selling_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            print(f'There was an error with creating a user: {err_msg}')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))