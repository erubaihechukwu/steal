import os
import random
from stealapp import app
from flask import render_template,make_response,request,abort,redirect,flash,session,url_for
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from stealapp import db,app,csrf
from stealapp.models import *
from stealapp.forms import *

@app.route('/store/home', methods=['POST','GET'])
def store_home_launch():
    loggedin = session.get("store")
    if loggedin != None:
        if request.method =="GET":
            store_deets = db.session.query(Store).filter(Store.store_id == loggedin).first()
            categories = db.session.query(Category).all()
            listings = db.session.query(Listing).filter(Listing.listing_store_id == loggedin,Listing.listing_deleted == "no").all()
            pending = db.session.query(Cart).filter(Cart.cart_store_id == loggedin,Cart.cart_listing_deleted == "no",Cart.cart_listing_status == "paid").all()
            orders = db.session.query(Cart).filter(Cart.cart_user_id == loggedin,Cart.cart_listing_deleted == "no",Cart.cart_listing_status != "notpaid").all()
            return render_template('store/home.html', categories=categories, listings=listings, store_deets=store_deets,pending=pending,orders=orders)
        else:
            lid = request.form["id"]
            dellisting = db.session.query(Listing).filter(Listing.listing_id == lid).first()
            dellisting.listing_deleted = "yes"
            db.session.commit()
            flash("cart item deleted")
            return redirect("/store/home")    
    else:
        return redirect("/store/login")
@app.route('/store/signup', methods=['POST','GET'])
def store_signup():
    sign = StoreSignupForm()
    if request.method =="GET":
        return render_template('store/signup.html',sign=sign)
    else:
        if sign.validate_on_submit():
            storename = sign.storename.data
            email = sign.email.data
            pswd = sign.password.data
            phone = sign.phone.data
            hashed = generate_password_hash(pswd)
            store = Store(store_name=storename, store_email=email, store_pwd=hashed, store_image='',store_phone=phone)
            db.session.add(store)
            db.session.commit()
            storeid = store.store_id  # retrieve the guest id
            session["store"] = storeid  # save the id in session so you can use it elsewhere
            flash('Successfully Registered!')
            return redirect('/store/home')
        else:
            return render_template('store/signup.html', sign=sign)
@app.route('/store/login', methods=["POST","GET"])
def store_login():
    if request.method =="GET":
        return render_template('store/login.html')
    else:
        email = request.form["email"]
        password = request.form["password"]
        storedeets = Store.query.filter(Store.store_email==email).first()
        if storedeets and check_password_hash(storedeets.store_pwd,password):
            session["store"] = storedeets.store_id
            return redirect('/store/profile')
        else:
            flash('Invalid Credentials', category='Invalid')
            return redirect("/store/login")
@app.route('/store/logout')
def store_logout():
    session.pop('store',None)
    return redirect('/store/login')
@app.route('/store/profile')
def store_profilelaunch():
    loggedin = session.get("store")
    if loggedin != None:
        store_deets = db.session.query(Store).filter(Store.store_id==loggedin).first()
        return render_template('store/profile.html',store_deets=store_deets)
    else:
        return redirect("/store/login")
@app.route('/store/post',methods=["POST","GET"])
def store_post():
    categories = db.session.query(Category).all()
    loggedin = session.get("store")
    if request.method =="GET":
        return render_template('store/post.html',categories=categories)
    else:
        if loggedin != None:
            #retrieve for data and upload
            cp = request.files['cover_image']
            if cp.filename != "":
                allowed = ['.jpg','.png','.jpeg']
                name = cp.filename

                newname = random.random() * 10000000
                picturename, ext = os.path.splitext(name)  # splits file into two parts on the extension
                if ext in allowed:
                    path = "stealapp/static/lp/" + str(newname) + ext
                    cp.save(f"{path}")
                else:
                    flash('unsupported image')
                    return render_template('/store/post')

                id = session.get("store")
                title = request.form['title']
                quantity = request.form['quantity']
                description = request.form['description']
                category = request.form['category']
                price = request.form['price']

                listing = Listing(listing_title=title, listing_qty=quantity, listing_description=description, listing_store_id=id, listing_category_id=category, listing_price=price, listing_image=str(newname) + ext)
                db.session.add(listing)
                db.session.commit()
                ll = listing.listing_id
                return redirect('/store/profile')
            else:
                flash('please select a valid image')
                return 'you must have a cover photo'
        else:
            return redirect("/store/login")
@app.route('/store/logo',methods=["POST","GET"])
def submit_logo():
    loggedin = session.get('store')
    if loggedin != None:
        if request.method == "GET":
            return render_template('store/usl.html')
        else:
            if request.files != "":
                allowed = ['.jpg', '.png', '.jpeg']
                id = session.get("store")
                fileobj = request.files['storelogo']
                name = fileobj.filename

                newname = random.random() * 10000000
                picturename, ext = os.path.splitext(name)  # splits file into two parts on the extension
                if ext in allowed:
                    path = "stealapp/static/pp/" + str(newname) + ext
                    fileobj.save(f"{path}")

                    store = db.session.query(Store).get(id)
                    store.store_image = str(newname) + ext
                    db.session.commit()
                    flash("image successfully uploaded", category='Success')
                    return redirect('/store/profile')
                else:
                    flash("invalid format", category='Invalid')
                    return redirect('/store/profile')
            else:
                flash('please select a valid image', category='Invalid')
                return redirect('/store/login')
    else:
        return redirect('/store/login')
@app.route("/store/deli",methods=["POST"])        
def deli():
    lid = request.form["ici"]
    cartit = db.session.query(Cart).filter(Cart.cart_id == lid).first()
    cartit.cart_listing_status = "delivered"
    db.session.commit()
    flash("listing status successfully updated")
    return redirect("/store/home")