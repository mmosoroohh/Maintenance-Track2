
class Api_Request():
    """This class represents the requests in Maintenance Tracker."""

    def __init__(self, name, description, category, department):
        """initialize with name, description, category, department"""
        self.name = name
        self.description = description
        self.category = category
        self.department = department

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Api_Request.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Api_Request: {}>".format(self.name)
