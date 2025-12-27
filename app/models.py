from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)
    points = db.Column(db.Integer, default=0, nullable=False)
    reports_count = db.Column(db.Integer, default=0, nullable=False)
    tasks_completed = db.Column(db.Integer, default=0, nullable=False)
    badges = db.Column(db.Text, default='[]')  # JSON array of badge names
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    reports = db.relationship('WasteReport', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_badges(self):
        try:
            return json.loads(self.badges) if self.badges else []
        except:
            return []
    
    def add_badge(self, badge_name):
        badges = self.get_badges()
        if badge_name not in badges:
            badges.append(badge_name)
            self.badges = json.dumps(badges)
            return True
        return False
    
    def add_points(self, points):
        self.points += points
    
    def __repr__(self):
        return f'<User {self.email}>'


class WasteReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    location_source = db.Column(db.String(20), nullable=False)  # EXIF, BROWSER, MANUAL
    address = db.Column(db.String(255))
    cluster_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<WasteReport {self.id} by {self.user_id}>'


class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<ContactMessage {self.id} from {self.email}>'


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    status = db.Column(db.String(20), default='available', nullable=False)  # available, busy, off-duty
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    trucks = db.relationship('Truck', backref='driver', lazy='dynamic')
    assignments = db.relationship('Assignment', backref='driver', lazy='dynamic')

    def __repr__(self):
        return f'<Driver {self.name} - {self.license_number}>'


class Truck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    truck_number = db.Column(db.String(20), unique=True, nullable=False)
    capacity = db.Column(db.Float, nullable=False)  # in cubic meters
    truck_type = db.Column(db.String(50), nullable=False)  # garbage truck, compactor, etc.
    status = db.Column(db.String(20), default='available', nullable=False)  # available, in-use, maintenance
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=True)
    current_location_lat = db.Column(db.Float, nullable=True)
    current_location_lng = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    assignments = db.relationship('Assignment', backref='truck', lazy='dynamic')

    def __repr__(self):
        return f'<Truck {self.truck_number} - {self.status}>'


class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    estimated_duration = db.Column(db.Integer, nullable=False)  # in minutes
    distance_km = db.Column(db.Float, nullable=False)
    stops = db.Column(db.Text, nullable=True)  # JSON array of stop coordinates
    status = db.Column(db.String(20), default='active', nullable=False)  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    assignments = db.relationship('Assignment', backref='route', lazy='dynamic')

    def get_stops(self):
        try:
            return json.loads(self.stops) if self.stops else []
        except:
            return []

    def set_stops(self, stops_list):
        self.stops = json.dumps(stops_list) if stops_list else None

    def __repr__(self):
        return f'<Route {self.route_name} - {self.estimated_duration}min>'


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    truck_id = db.Column(db.Integer, db.ForeignKey('truck.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)
    assignment_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=True)
    status = db.Column(db.String(20), default='scheduled', nullable=False)  # scheduled, in-progress, completed, cancelled
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Assignment Truck:{self.truck_id} Route:{self.route_id} on {self.assignment_date}>'

