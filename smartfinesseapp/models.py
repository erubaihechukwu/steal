from datetime import datetime
from smartfinesseapp import db
class Listing(db.Model):
    __tablename__ = 'listing'
    listing_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    listing_store_id = db.Column(db.Integer(), db.ForeignKey('store.store_id'), nullable=False)
    listing_status = db.Column(db.String(255), nullable=True)
    listing_title = db.Column(db.String(55), nullable=True)
    listing_description = db.Column(db.String(255), nullable=True)
    listing_qty = db.Column(db.Integer(), nullable=True)
    listing_created_on = db.Column(db.DateTime(), default=datetime.utcnow(), onupdate=datetime.utcnow())
    listing_category_id = db.Column(db.Integer(), db.ForeignKey('category.category_id'), nullable=False)
    listing_image = db.Column(db.String(255), nullable=False)
    listing_price = db.Column(db.Integer(), nullable=False)
    all_lists_cart = db.relationship('Cart', backref='lister_info')
    listing_deleted = db.Column(db.String(5), nullable=False)
    #how you want to show it
#    def __repr__(self):
#        return f"{self.id} {self.post_title}"
    # set up the relationship
#    comments = db.relationship('Comment', backref='dpost')
#    cat = db.relationship('Category', backref='allpost')
class Lga(db.Model):
    __tablename__ = 'lga'
    lga_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    lga_state_id = db.Column(db.Integer(), db.ForeignKey('state.state_id'), nullable=False)
    lga_name = db.Column(db.Text(), nullable=False)
class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    category_name = db.Column(db.Text(), nullable=False)
    category_image = db.Column(db.Text(), nullable=False)
    category_links = db.Column(db.Text(), nullable=False)
    deleted = db.Column(db.Text(), nullable=False)
#    def __repr__(self):
#        return f"{self.cat_name}"
class State(db.Model):
    __tablename__ = 'state'
    state_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    state_name = db.Column(db.Text(), nullable=False)
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_fname = db.Column(db.String(255), nullable=False)
    user_lname = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.Text(), nullable=False)
    user_phone = db.Column(db.String(11), nullable=True)
    user_lga_id = db.Column(db.Integer(), db.ForeignKey('lga.lga_id'), nullable=False)
    user_state_id = db.Column(db.Integer(), db.ForeignKey('state.state_id'), nullable=False)
    user_pwd = db.Column(db.String(255), nullable=True)
    user_reg_date = db.Column(db.DateTime(), default=datetime.utcnow())
    user_dob = db.Column(db.DateTime(), nullable=False)
    user_image = db.Column(db.String(255), nullable=False)
class Li(db.Model):
    __tablename__ = 'li'
    li_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    li_listing_id = db.Column(db.Integer(), db.ForeignKey('listing.listing_id'), nullable=False)
    li_image = db.Column(db.String(255), nullable=False)
class Store(db.Model):
    __tablename__ = 'store'
    store_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    store_name = db.Column(db.String(255), nullable=False)
    store_email = db.Column(db.Text(), nullable=False)
    store_phone = db.Column(db.String(11), nullable=True)
    store_pwd = db.Column(db.String(255), nullable=True)
    store_reg_date = db.Column(db.DateTime(), default=datetime.utcnow(), onupdate=datetime.utcnow())
#    store_reg_date = db.Column(db.DateTime(), default=datetime.utcnow(), onupdate=datetime.utcnow())
    store_image = db.Column(db.String(255), nullable=False)
class ListingReview(db.Model):
    __tablename__ = 'lr'
    lr_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    lr_text = db.Column(db.Text(), nullable=False)
    lr_star = db.Column(db.Text(), nullable=False)
    lr_listing_id = db.Column(db.Integer(), db.ForeignKey('listing.listing_id'), nullable=False)
    lr_store_id = db.Column(db.Integer(), db.ForeignKey('store.store_id'), nullable=False)
class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    admin_name = db.Column(db.String(255), nullable=False)
    admin_pwd = db.Column(db.String(255), nullable=True)
    user_reg_date = db.Column(db.DateTime(), default=datetime.utcnow(), onupdate=datetime.utcnow())
class Cart(db.Model):
    __tablename__ = 'cart'
    cart_listing_id = db.Column(db.Integer(), db.ForeignKey('listing.listing_id'), nullable=False)
    cart_user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'), nullable=False)
    cart_listing_status = db.Column(db.String(255), nullable=True)
    cart_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    cart_listing_qty = db.Column(db.Integer(),nullable=False)
    cart_listing_deleted = db.Column(db.String(5), nullable=False)
    cart_store_id = db.Column(db.String(5), nullable=False)
class Transaction(db.Model):
    __tablename__ = 'transaction'
    transaction_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    transaction_ref = db.Column(db.Integer(),nullable=False)
    transaction_amount = db.Column(db.Integer(),nullable=False)
    transaction_date = db.Column(db.DateTime(), default=datetime.utcnow())
    transaction_user_id = db.Column(db.Integer(),nullable=False)