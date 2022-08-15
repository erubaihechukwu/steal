import os
import random
from stealapp import app
from flask import render_template,make_response,request,abort,redirect,flash,session,url_for
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from stealapp import db,app,csrf
from stealapp.models import *
from stealapp.forms import *

@app.route('/admin/home', methods=["POST","GET"])
def admin_home_launch():
    loggedin = session.get("admin")
    if loggedin != None:
        if request.method == "GET":
            admin_deets = db.session.query(Admin).filter(Admin.admin_id == loggedin).first()
            categories = db.session.query(Category).all()
            listings = db.session.query(Listing).filter(Listing.listing_deleted == "no").all()
            total = 0
            for i in listings:
                total = total + 1
            return render_template('admin/home.html', admin_deets=admin_deets, categories=categories, listings=listings, total=total)
        else:
            lid = request.form["id"]
            dellisting = db.session.query(Listing).filter(Listing.listing_id == lid).first()
            dellisting.listing_deleted = "yes"
            db.session.commit()
            flash("cart item deleted")
            return redirect("/admin/home")
    else:
        return redirect("/admin/login")
@app.route('/admin/login', methods=["POST","GET"])
def admin_login():
    if request.method =="GET":
        return render_template('admin/login.html')
    else:
        id = request.form["id"]
        password = request.form["password"]
        admindeets = Admin.query.filter(Admin.admin_id==id).first()
        admindeets2 = Admin.query.filter(Admin.admin_pwd==password).first()
        if admindeets and admindeets2:
            session["admin"] = admindeets.admin_id #or = admindeets
            return redirect('/admin/home')
        else:
            flash('Invalid Credentials', category='Invalid')
            return redirect("/admin/login")
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin',None)
    return redirect('/admin/login')