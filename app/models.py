from app import db

class User(db.Model):
    """This class represents the user in Maintenance Tracker."""

    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
   

    def __init__(self, name, email, password, public_id, admin):
        """initialize with name, email, password"""
        self.name = name
        self.email = email
        self.password = password
        self.public_id = public_id
        self.admin = admin

    def json_dump(self):
        return dict(
            name=self.name,
            email=self.email,
            password=self.password,
            public_id=self.public_id,
            admin=self.admin
        )

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create_user(self):
        db.session.add(User)
        db.session.commit()

    def get_all_users(self):
        return User.query.all(User)

    def get_one_user(self):
        return User.query.first(User)

    def delete(self):
        db.session.delete(User)
        db.session.commit()

    def __repr__(self):
        return "<User: {}>".format(self.name)   


class Requests(db.Model):
    """This class represents the requests in Maintenance Tracker."""

    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    decription = db.Column(db.String(100))
    category = db.Column(db.String(50))
    department = db.Column(db.String(50))
    user_id = db.Column(db.Integer)
    

    def __init__(self, name, description, category, department, user_id):
        """Initialize with name, description, category, department."""
        self.name = name
        self.description = description
        self.category = category
        self.department = department
        self.user_id = user_id

    def json_dump(self):
        return dict(
            name = self.name,
            description = self.decription,
            category = self.category,
            department = self.department,
            user_id = self.user_id
        )

    def save(self):
        db.session.add(self)
        db.session.commit()    