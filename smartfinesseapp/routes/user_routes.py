from collections import ChainMap
from heapq import merge
from multiprocessing import Value
import os
import random
from ssl import AlertDescription
from smartfinesseapp import app
from flask import render_template,make_response,request,abort,redirect,flash,session,url_for
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from smartfinesseapp import db,app,csrf
from smartfinesseapp.models import *
from smartfinesseapp.forms import *
@app.route('/search', methods=['POST','GET'])
def search_engiene():
    tag = request.form["?"]
    search = "%{}%".format(tag)
    listings = db.session.query(Listing).filter(Listing.listing_deleted == "no",Listing.listing_title.like(search)).all()
    total = 0
    for i in listings:
        total = total + 1
    return render_template('user/search.html',listings=listings,search=search,tag=tag,total=total)
@app.route('/home')
def homelaunch():
    categories = db.session.query(Category).filter(Category.deleted == "no").all()
    listings = db.session.query(Listing).filter(Listing.listing_deleted == "no").all()
    return render_template('user/home.html', categories=categories,listings=listings)
@app.route('/')
def blanklaunch():
    categories = db.session.query(Category).all()
    listings = db.session.query(Listing).filter(Listing.listing_deleted == "no").all()
    return render_template('user/home.html',categories=categories,listings=listings)
@app.route('/signup', methods=['POST','GET'])
def signup():
    sign = SignupForm()
    if request.method =="GET":
        return render_template('user/signup.html',sign=sign)
    else:
        if sign.validate_on_submit():
            firstname = sign.firstname.data
            lastname = sign.lastname.data
            email = sign.email.data
            pswd = sign.password.data
            hashed = generate_password_hash(pswd)
            user = User(user_fname=firstname, user_lname=lastname, user_email=email, user_pwd=hashed, user_image='')
            db.session.add(user)
            db.session.commit()
            userid = user.user_id  # retrieve the guest id
            session["user"] = userid  # save the id in session so you can use it elsewhere
            flash('Successfully Registered!')
            return redirect('/profile')
        else:
            return render_template('user/signup.html', sign=sign)

@app.errorhandler(404)
def mypagenotfound(error):
    #method 1
    return render_template('user/error.html',error=error),404
    #method 2
    rsp = make_response(render_template('error.html'))
@app.route('/login', methods=["POST","GET"])
def login():
    if request.method =="GET":
        return render_template('user/login.html')
    else:
        email = request.form["email"]
        password = request.form["password"]
        userdeets = User.query.filter(User.user_email==email).first()
        if userdeets and check_password_hash(userdeets.user_pwd,password):
            session["user"] = userdeets.user_id
            return redirect('/profile')
        else:
            flash('Invalid Credentials', category='Invalid')
            return redirect("/login")
@app.route('/profile')
def profilelaunch():
    loggedin = session.get("user")
    cart = session.get("usercart")
    if loggedin != None:
        user_deets = db.session.query(User).filter(User.user_id==loggedin).first()
        return render_template('user/profile.html',user_deets=user_deets,cart=cart)
    else:
        return redirect("/login")
@app.route('/logout')
def guest_logout():
    session.pop('user',None)
    return redirect('/login')
@app.route('/categories')
def categories_launch():
    return render_template("user/categories.html")
@app.route('/edit_profile',methods=["POST","GET"])
def submit_upload():
    loggedin = session.get("user")
    user_deets = db.session.query(User).filter(User.user_id == loggedin).first()
    if loggedin != None:
        if request.method == "GET":
            return render_template('user/edit.html',user_deets=user_deets)
        else:
        #retrieve for data and upload
            if request.files != "":
                allowed = ['.jpg','.png','.jpeg']
                id = session.get("user")
                fileobj = request.files['profilepix']
                name = fileobj.filename

                newname = random.random() * 10000000
                picturename, ext = os.path.splitext(name)#splits file into two parts on the extension
                if ext in allowed:
                    path = "stealapp/static/pp/" + str(newname) + ext
                    fileobj.save(f"{path}")

                    user = db.session.query(User).get(id)
                    firstname = request.form["firstname"]
                    lastname = request.form["lastname"]
                    email = request.form["email"]
                    phone = request.form["phone"]
                    user.user_image = str(newname) + ext
                    user.user_fname = firstname
                    user.user_lname = lastname
                    user.user_email = email
                    user.user_phone = phone
                    db.session.commit()
                    flash("image successfully uploaded")
                    return redirect('/edit_profile')
                else:
                    flash("invalid format")
                    return redirect('/profile')
            else:
                flash('please select a valid image')
                return redirect('/user/upp')
    else:
        return redirect('/login')
@app.route('/more_details',methods=["POST","GET"])
def details():
    loggedin = session.get("user")
    bp = request.form["id"]
    user_deets = db.session.query(User).filter(User.user_id == loggedin).first()
    listing_deets = db.session.query(Listing).filter(Listing.listing_id == bp).first()
    si = db.session.query(Store).filter(Store.store_id == listing_deets.listing_store_id).first()
    listings = db.session.query(Listing).filter(Listing.listing_deleted == "no").all()
    return render_template('user/listingmain.html',listing_deets=listing_deets,si=si,user_deets=user_deets,listings=listings)
@app.route('/addtocart',methods=["POST","GET"])
def addtocart():
        cartcreated = session.get("usercart")
        li = request.form["cli"]
        lq = request.form["qty"]
        addtocart = (li,lq)
        createcart = [(li,lq)]
        itemExists = ""
        if cartcreated == None:
            session["usercart"] = createcart
            return redirect('/cart')
        else:
            if not any(li in i for i,x in session["usercart"]):
                session["usercart"].append((li,lq))
            elif any(li in i for i in session["usercart"]):
                for i in session["usercart"]:
                    i.update(())  
        return redirect('/cart')
        
@app.route('/cart',methods=["POST","GET"])
def cartfunct():
    cart = session.get("usercart")
    if cart != None:
        presentcart = []
        for i,j in cart:
            listings = db.session.query(Listing).filter(Listing.listing_deleted == "no",Listing.listing_id == i).first()
            presentcart.append((listings,j))
        return render_template("user/cart.html",cart=cart,listings=listings,presentcart=presentcart)
    else:
        presentcart = ""
        listings = db.session.query(Listing).filter(Listing.listing_deleted == "no").all()
        return render_template("user/cart.html",cart=cart,listings=listings,presentcart=presentcart)
    
@app.route("/aboutus")
def aboutus():
    loggedin = session.get("store")
    return render_template("user/aboutus.html",loggedin=loggedin)
@app.route("/support")
def support():
    return render_template("user/support.html")
@app.route("/transact",methods=["POST"])
def transact():
    loggedin = session.get("user")
    if loggedin != None:
        amount = request.form['amount']
        ref = request.form["ref"]
        trans = Transaction(transaction_amount=amount, transaction_user_id=loggedin, transaction_ref=ref,)
        db.session.add(trans)
        db.session.commit()
        cart_listings = db.session.query(Cart).filter(Cart.cart_user_id == loggedin,Cart.cart_listing_deleted == "no",Cart.cart_listing_status == "notpaid").all()
        for i in cart_listings:
            i.cart_listing_status = "paid"
            db.session.commit()
            flash("cart item deleted")
        return redirect("/cart")
    else:
        return redirect("/login")
@app.route('/catty')
def gust_logout():
    session.pop('usercart',None)
    return redirect('/cart')
@app.route('/adaa')
def addad():
    q = session['usercart']
    q.append(('9','5'))
    session["usercart"] = q
    return redirect('/cart')    