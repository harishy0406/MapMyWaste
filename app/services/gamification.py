from app.models import User
from app import db
from config import Config

def update_user_achievements(user):
    """
    Update user badges, tasks, and bonus points based on reports_count.
    Returns list of newly earned badges.
    """
    new_badges = []
    
    # Check badge thresholds
    if user.reports_count >= Config.BADGE_ROOKIE_REPORTER:
        if user.add_badge('Rookie Reporter'):
            new_badges.append('Rookie Reporter')
            user.tasks_completed += 1
            user.add_points(Config.BONUS_POINTS_FIRST_REPORT)
    
    if user.reports_count >= Config.BADGE_NEIGHBORHOOD_WATCHER:
        if user.add_badge('Neighborhood Watcher'):
            new_badges.append('Neighborhood Watcher')
            user.tasks_completed += 1
            user.add_points(Config.BONUS_POINTS_5_REPORTS)
    
    if user.reports_count >= Config.BADGE_WASTE_WARRIOR:
        if user.add_badge('Waste Warrior'):
            new_badges.append('Waste Warrior')
            user.tasks_completed += 1
            user.add_points(Config.BONUS_POINTS_20_REPORTS)
    
    db.session.commit()
    return new_badges

