from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User model"""

    __tablename__ = "users"

    username = db.Column(db.Text,
                         primary_key=True)
    
    password = db.Column(db.Text,
                         nullable=False)
    
    email = db.Column(db.Text,
                      unique=True,
                      nullable=False)
    
    first_name = db.Column(db.Text,
                           nullable=False)
    
    last_name = db.Column(db.Text,
                          nullable=False)
    

    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """Register user with hashed password and return user"""
        
        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, first_name=first_name, last_name=last_name, email=email)
    
    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct. Return user if valid; else return False."""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False
        
        
class Trip(db.Model):
    """User trip"""

    __tablename__ = "trips"

    id = db.Column(db.Integer,
                   primary_key=True)
    
    name = db.Column(db.Text,
                          unique=True,
                          nullable=False)

    username = db.Column(db.Text,
                        db.ForeignKey('users.username', ondelete='CASCADE'),
                        nullable=False)
    
    
class Stop(db.Model):
    """Trip stop (location)"""

    __tablename__ = "stops"

    id = db.Column(db.Integer,
                   primary_key=True)
    
    latitude = db.Column(db.Text,
                         nullable=False)
    
    longitude = db.Column(db.Text,
                          nullable=False)
    
    trip_id = db.Column(db.Integer,
                        db.ForeignKey('trips.id', ondelete='CASCADE'),
                        nullable=False)
    
    trip = db.relationship('Trip')
    
    stop_name = db.Column(db.Text)

    def serialize(self):
        """Returns a dict representation of stop"""
        return { 'id': self.id,
                 'lat': self.latitude,
                 'lng': self.longitude,
                  'stop_name': self.stop_name }
    
        
class PackItem(db.Model):
    """User packing list"""

    __tablename__ = "pack_items"

    id = db.Column(db.Integer,
                   primary_key=True)
    
    trip_id = db.Column(db.Integer,
                        db.ForeignKey('trips.id', ondelete='CASCADE'),
                        nullable=False)
    
    trip = db.relationship('Trip')

    item_name = db.Column(db.Text,
                          nullable=False)
    
    pack_status = db.Column(db.Boolean,
                            nullable=False,
                            default=False)
    

class ItineraryItem(db.Model):
    """User packing list"""

    __tablename__ = "itinerary_items"

    id = db.Column(db.Integer,
                   primary_key=True)
    
    stop_id = db.Column(db.Integer,
                        db.ForeignKey('stops.id', ondelete='CASCADE'),
                        nullable=False)
    
    stop = db.relationship('Stop')

    item_name = db.Column(db.Text,
                          nullable=False)


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)

