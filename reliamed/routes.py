from reliamed import app
from flask import render_template, redirect, url_for, flash, request, session
from reliamed.models import Pharmaceuticals, User
from reliamed.forms import RegisterForm, LoginForm, PurchaseProductForm, SellProductForm, AdminUserForm, AdminLoginForm, MedicineForm
from reliamed import db
from flask_login import login_user, logout_user, login_required, current_user
from .trained_model import save_image, predict_image_class, display_uploaded_image

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
        # Purchase Product Logic
        purchased_product = request.form.get('purchased_product')
        p_product_object = Pharmaceuticals.query.filter_by(name=purchased_product).first()
        if p_product_object:
            if current_user.can_purchase(p_product_object):
                p_product_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_product_object.name} for ₱{p_product_object.price}.00", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_product_object.name}!", category='danger')
        
        # Sell Product Logic
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
            if attempted_user.is_admin:
                flash('Admins must log in through the admin login page.', category='danger')
                return redirect(url_for('admin_login_page'))
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password do not match! Please try again', category='danger')

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
    relative_image_path = image_path.replace('/home/hecavi/appDevProj/reliamed/static/', '')

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

from reliamed.decorators import admin_required

# From Admin Panel --> This is where admin user is redirected
@app.route('/admin-home', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_home():
    return render_template('admin/dashboard.html')

@app.route('/admin-main', methods=['GET', 'POST'])
def admin_main():
    return render_template('admin/adminhome.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login_page():
    form = AdminLoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ) and attempted_user.is_admin:
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('admin_home'))
        else:
            flash('Invalid credentials or not an admin account! Please try again', category='danger')

    return render_template('admin/adminlogin.html', form=form)

# A button in admin panel to create a new user --> if new user created, return to admin_home
@app.route('/create-user', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    form = AdminUserForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password.data,
                              is_admin=form.is_admin.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash(f'User {user_to_create.username} created successfully! Go to `view_user` to check.', category='success')
        return redirect(url_for('admin_main'))

    users = User.query.all()
    return render_template('admin/create_user.html', form=form, users=users)

# From view_users.html, the admin can update, delete or grant users for admin rights.
@app.route('/view-users', methods=['GET', 'POST'])
@login_required
@admin_required
def view_users():
    users = User.query.all()
    return render_template('admin/view_users.html', users=users)

# In view_users.html, the admin can click on the user to edit the user credentials
@app.route('/edit_user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = AdminUserForm(original_username=user.username, original_email=user.email_address, obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email_address = form.email_address.data
        user.is_admin = form.is_admin.data
        # The update is optional whether admin wants to update the password or not
        if form.password.data:
            user.password = form.password.data
        db.session.commit()
        flash(f'User {user.username} updated successfully!', category='success')
        return redirect(url_for('view_users'))
    return render_template('admin/edit_user.html', form=form, user=user)

# In view_users.html, the admin can click on the user to delete the user credentials
@app.route('/view-users/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} deleted successfully!', category='success')
    return redirect(url_for('view_users'))

# ----------------- add route for viewing the admin/view_medicine.html page -----------------

@app.route('/view-medicines')
@login_required
@admin_required
def view_medicines():
    medicines = Pharmaceuticals.query.all()
    return render_template('admin/view_medicines.html', medicines=medicines)

@app.route('/add_medicine', methods=['GET', 'POST'])
@login_required
@admin_required
def add_medicine():
    form = MedicineForm()
    if form.validate_on_submit():
        new_medicine = Pharmaceuticals(
            name=form.name.data,
            price=form.price.data,
            barcode=form.barcode.data,
            description=form.description.data
        )
        db.session.add(new_medicine)
        db.session.commit()
        flash(f'Medicine {new_medicine.name} added successfully!', category='success')
        return redirect(url_for('view_medicines'))
    return render_template('admin/create_medicine.html', form=form)

@app.route('/edit_medicine/edit/<int:medicine_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_medicine(medicine_id):
    medicine = Pharmaceuticals.query.get_or_404(medicine_id)
    form = MedicineForm(obj=medicine)
    if form.validate_on_submit():
        medicine.name = form.name.data
        medicine.price = form.price.data
        medicine.barcode = form.barcode.data
        medicine.description = form.description.data
        db.session.commit()
        flash(f'Medicine {medicine.name} updated successfully!', category='success')
        return redirect(url_for('view_medicines'))
    return render_template('admin/edit_medicine.html', form=form, medicine=medicine)

@app.route('/delete_medicine/<int:medicine_id>', methods=['POST'])
@login_required
@admin_required
def delete_medicine(medicine_id):
    medicine = Pharmaceuticals.query.get_or_404(medicine_id)
    db.session.delete(medicine)
    db.session.commit()
    flash(f'Medicine {medicine.name} deleted successfully!', category='success')
    return redirect(url_for('view_medicines'))