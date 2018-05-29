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


    def __init__(self, name, email, password):
        """initialize with name, email, password"""
        self.name = name
        self.email = email
        self.password = password

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