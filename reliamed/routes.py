from reliamed import app
from flask import render_template, redirect, url_for, flash, request, session
from reliamed.models import Pharmaceuticals , User
from reliamed.forms import RegisterForm, LoginForm, PurchaseProductForm, SellProductForm
from reliamed import db
from flask_login import login_user, logout_user, login_required, current_user
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from .trained_model import save_image, predict_image_class, display_uploaded_image  # Import the functions from trained_model.py

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseProductForm()
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
        return render_template('market.html', pharmaceuticals=pharmaceuticals, purchase_form=purchase_form, owned_pharmaceuticals=owned_pharmaceuticals, selling_form=selling_form)

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

@app.route('/predict', methods=['GET'])
@login_required
def predict():
    # Render the prediction page where users can upload an image for classification.
    return render_template('predict.html')

@app.route('/predicted', methods=['POST'])
def predicted():
    imagefile = request.files['imagefile']
    
    # Save the uploaded image and get its path
    image_path = save_image(imagefile)
    print(f"Image saved at: {image_path}")  # Debug statement
    
    # Display image
    disp_uploadedIMG = display_uploaded_image(imagefile)
    print(f"Image displayed: {disp_uploadedIMG}")

    # Get the prediction
    predicted_class, confidence_score = predict_image_class(image_path)
    print(f"Predicted class: {predicted_class}, Confidence Score: {confidence_score}")  # Debug statement

    # Extract the relative path to the image for display
    relative_image_path = image_path.replace('/workspaces/appDevProj/reliamed/static/', '')

    return render_template('predict.html', prediction_text=f'This medicine is classified as: {predicted_class} ({confidence_score * 100:.2f}%)', image_path=relative_image_path)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

# -------------------------user area----------------------------
"""
@app.route('/user/change-password', methods=['GET', 'POST'])
def change_password_page():
    if not 
    return render_template('change_password.html')
"""

# -------------------------Admin area----------------------------

# table of users
@app.route('/table')
@login_required
def table():
    users = User.query.all()
    return render_template('table.html', users=users)

# admin control panel | http://127.0.0.1:5000/admin --> login required | !!ISSUE -- Can't edit/create but can delete!! 
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        return super(MyAdminIndexView, self).index()

class MyModelView(ModelView):
    def is_accessible(self):
        return login_required(lambda: True)()

admin = Admin(app, name='Admin Panel', template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))

@app.route('/admin-dashboard')
def admin_dashboard():
    return render_template('./admin/admin-dashboard.html')

# Admin login
# @app.route('/admin/', methods=['GET', 'POST'])
# def adminLogin():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         if username == "" and password == "":
#             flash('Please fill all the field', 'danger')
#             return redirect('/admin/')
#         else:
#             # Login admin by username
#             admins = Admin.query.filter_by(username=username).first()
#             if admins and bcrypt.check_password_hash(admins.password, password):
#                 session['admin_id'] = admins.id
#                 session['admin_name'] = admins.username
#                 flash('Login Successfully', 'success')
#                 return redirect('/admin/dashboard')
#             else:
#                 flash('Invalid Email and Password', 'danger')
#                 return redirect('/admin/')
#     else:
#         return render_template('admin/index.html', title="Admin Login")