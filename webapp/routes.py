import secrets, os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from webapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, TransactionForm, MineForm
from webapp.models import User, Post
from webapp import app, db, bcrypt, KWCblockchain
from flask_login import login_user, current_user, logout_user, login_required

# blockchain imports
from blockchain import *


 

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html') # gives us a variable

@app.route("/users")
def users():
    users = User.query.all()
    
    return render_template('users.html', title = "Users", users = users)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in', 'success')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # hash the pw
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # crewate user
        user = User(username=form.username.data, 
                    email=form.email.data, 
                    password=hashed_pw)
        # add user to DataBase
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created, you may now log in', 'success')
        return redirect(url_for('login')) #function name
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods =['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in', 'success')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # check iun DataBase if user exists
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') # getordefault
            
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username & password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))


def save_picture(form_picture):
    randomHex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = randomHex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail (output_size)

    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.picture.data:
        picture_file = save_picture(form.picture.data)
        current_user.image_file = picture_file
    if form.validate_on_submit():
        current_user.username = form.username.data # updates data in DatabAse directly
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title=current_user.username, image_file=image_file, form= form)


@app.route("/transaction", methods = ['GET', 'POST'])
def transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        receiver = User.query.filter_by(username = form.receiver.data).first()
        if receiver:
            trans = KWCblockchain.makeTransaction(current_user, form.receiver.data, form.amount.data)
            if trans == "OK":
                flash('Transaction done successfully', 'success')
            elif trans == "money problem":
                flash('Balance insufficient, please buy more KWC', 'danger')
            else:
                flash('Error', 'danger')
        else:
            flash('User does not exist', 'danger')
    
    return render_template('transaction.html', title = 'Transaction', form= form)




@app.route("/blockchain_status", methods = ['GET', 'POST'])
def blockchain_status():
    """ lastBlock = KWCblockchain.getLastBlock()
    i = lastBlock.getIndex()
    total = lastBlock.getTransactionsTotal()
    prevHash = lastBlock.getPrevHash()
    totalBlocks = KWCblockchain.chainLength()

    return render_template('blockchain_status.html', 
                            title = 'Status', index = i, 
                            total = total, prevHash = prevHash, 
                            totalBlocks = totalBlocks) """
    return render_template('blockchain_status.html',totalBlocks = KWCblockchain.chainLength(), chain= KWCblockchain.chain)



@app.route("/mine", methods=['GET', 'POST'])
def mine():
    form = MineForm()
    if form.validate_on_submit():
        print("mine")
        if KWCblockchain.minePendingTransactions():
            flash('Thank you mining a Block! \n Check your rewards!', 'Success')
        else:
            flash('There was no transaction to mine...', 'danger')
    return render_template('mine.html', form = form)