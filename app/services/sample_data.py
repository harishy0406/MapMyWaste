"""
Sample data generator for testing and prototyping
"""
from app import db
from app.models import User, WasteReport
from config import Config
import random
from datetime import datetime, timedelta

def generate_sample_data():
    """Generate sample users and reports for prototyping"""
    
    # Sample users with Indian names
    sample_users_data = [
        {'name': 'Arun Kumar', 'email': 'arun@example.com', 'points': 250, 'reports': 15},
        {'name': 'Priya Sharma', 'email': 'priya@example.com', 'points': 180, 'reports': 12},
        {'name': 'Vijay Rajan', 'email': 'vijay@example.com', 'points': 320, 'reports': 22},
        {'name': 'Meera Patel', 'email': 'meera@example.com', 'points': 150, 'reports': 8},
        {'name': 'Karthik Nair', 'email': 'karthik@example.com', 'points': 200, 'reports': 14},
        {'name': 'Anjali Reddy', 'email': 'anjali@example.com', 'points': 280, 'reports': 18},
        {'name': 'Suresh Babu', 'email': 'suresh@example.com', 'points': 220, 'reports': 16},
        {'name': 'Divya Krishnan', 'email': 'divya@example.com', 'points': 190, 'reports': 13},
    ]

    # Sample locations in Tamil Nadu
    sample_locations = [
        (13.0827, 80.2707),  # Chennai Central
        (13.0569, 80.2425),  # T. Nagar, Chennai
        (13.0820, 80.2785),  # Adyar, Chennai
        (13.0648, 80.2470),  # Velachery, Chennai
        (13.0480, 80.2080),  # Porur, Chennai
        (12.9200, 80.2400),  # Tambaram, Chennai
        (10.7905, 78.7047),  # Trichy (Tiruchirappalli)
        (11.0168, 76.9558),  # Coimbatore
        (9.9252, 78.1198),   # Madurai
        (11.6643, 78.1460),  # Salem
        (8.7642, 78.1348),   # Nagercoil
        (8.3143, 77.1693),   # Tirunelveli
        (9.2839, 79.3000),   # Jaffna (Sri Lanka, but Tamil area)
        (10.9661, 79.3940),  # Thanjavur
        (10.7669, 79.8425),  # Kumbakonam
    ]
    
    sample_descriptions = [
        'Plastic bottles and containers found near park',
        'Cardboard boxes and packaging materials',
        'Food waste and organic materials',
        'Mixed waste including paper and plastic',
        'Construction debris',
        'Household waste bags',
        'Electronic waste components',
        'Glass bottles and containers',
        'Metal cans and scrap',
        'General litter and debris'
    ]
    
    users_created = []
    
    # Create sample users
    for user_data in sample_users_data:
        user = User.query.filter_by(email=user_data['email']).first()
        if not user:
            user = User(
                name=user_data['name'],
                email=user_data['email'],
                role='user',
                points=user_data['points'],
                reports_count=user_data['reports']
            )
            user.set_password('password123')
            db.session.add(user)
            users_created.append(user)
        else:
            # Update existing user's stats if they have fewer reports than expected
            if user.reports_count < user_data['reports']:
                user.points = user_data['points']
                user.reports_count = user_data['reports']
            users_created.append(user)
    
    db.session.commit()
    
    # Create sample reports
    reports_created = 0
    for user in users_created:
        num_reports = user.reports_count
        for i in range(num_reports):
            lat, lon = random.choice(sample_locations)
            # Add some randomness to locations
            lat += random.uniform(-0.01, 0.01)
            lon += random.uniform(-0.01, 0.01)
            
            # Random date within last 30 days
            days_ago = random.randint(0, 30)
            created_at = datetime.utcnow() - timedelta(days=days_ago)
            
            report = WasteReport(
                user_id=user.id,
                image_filename=f'sample_{user.id}_{i}.jpg',  # Placeholder
                description=random.choice(sample_descriptions),
                latitude=lat,
                longitude=lon,
                location_source=random.choice(['EXIF', 'BROWSER', 'MANUAL']),
                created_at=created_at
            )
            db.session.add(report)
            reports_created += 1
    
    db.session.commit()
    
    return {
        'users_created': len(users_created),
        'reports_created': reports_created
    }

