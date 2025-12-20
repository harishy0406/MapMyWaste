from flask import render_template, redirect, url_for, flash, jsonify, abort, request
from flask_login import login_required, current_user
from functools import wraps
from app.admin import bp
from app.models import User, WasteReport
from app import db
from app.services.clustering import run_clustering
from config import Config
from collections import defaultdict

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
@admin_required
def dashboard():
    total_reports = WasteReport.query.count()
    total_users = User.query.count()

    # Debug output
    print(f"Debug - Total reports: {total_reports}, Total users: {total_users}")

    # Count clusters
    reports_with_clusters = WasteReport.query.filter(WasteReport.cluster_id.isnot(None)).all()
    cluster_count = len(set(r.cluster_id for r in reports_with_clusters if r.cluster_id is not None))

    # Recent reports
    recent_reports = WasteReport.query.order_by(WasteReport.created_at.desc()).limit(10).all()

    return render_template('admin/dashboard.html',
                         total_reports=total_reports,
                         total_users=total_users,
                         cluster_count=cluster_count,
                         recent_reports=recent_reports)

@bp.route('/cluster', methods=['POST'])
@login_required
@admin_required
def cluster():
    try:
        print("Starting clustering...")  # Debug
        k = request.form.get('k', type=int)
        print(f"Clustering with k={k}")  # Debug
        result = run_clustering(k=k)
        print(f"Clustering result: {result}")  # Debug

        if result['success']:
            flash(f"Clustering completed! {result['clusters']} clusters created from {result['total_reports']} reports.", 'success')
        else:
            flash(result['message'], 'error')
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        flash(f"Clustering failed: {str(e)}", 'error')
        print(f"Clustering error details: {error_details}")  # Debug

    return redirect(url_for('admin.dashboard'))

@bp.route('/map')
@login_required
@admin_required
def map():
    # Get all reports with coordinates
    reports = WasteReport.query.filter(
        WasteReport.latitude.isnot(None),
        WasteReport.longitude.isnot(None)
    ).all()
    
    # Calculate centroids
    centroids = []
    if reports:
        cluster_groups = defaultdict(list)
        for report in reports:
            if report.cluster_id is not None:
                cluster_groups[report.cluster_id].append(report)
        
        for cluster_id, cluster_reports in cluster_groups.items():
            avg_lat = sum(r.latitude for r in cluster_reports) / len(cluster_reports)
            avg_lon = sum(r.longitude for r in cluster_reports) / len(cluster_reports)
            centroids.append({
                'cluster_id': cluster_id,
                'latitude': avg_lat,
                'longitude': avg_lon,
                'count': len(cluster_reports)
            })
    
    return render_template('admin/map.html',
                         reports=reports,
                         centroids=centroids,
                         depot_lat=Config.DEPOT_LAT,
                         depot_lon=Config.DEPOT_LON)

@bp.route('/clear_reports', methods=['POST'])
@login_required
@admin_required
def clear_reports():
    try:
        # Delete all Waste Reports
        report_count = WasteReport.query.count()
        WasteReport.query.delete()

        # Delete all non-admin users and reset admin stats
        user_count = 0
        for user in User.query.all():
            if user.role != 'admin':
                db.session.delete(user)
                user_count += 1
            else:
                # Reset admin user stats
                user.reports_count = 0
                user.points = 0
                user.tasks_completed = 0
                user.badges = '[]'

        # Ensure admin user exists
        admin = User.query.filter_by(email='admin@mapmywaste.com').first()
        if not admin:
            admin = User(
                name='Admin',
                email='admin@mapmywaste.com',
                role='admin',
                points=0,
                reports_count=0,
                tasks_completed=0,
                badges='[]'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

        flash(f'Database reset complete! Deleted {report_count} reports and {user_count} users. Admin user recreated.', 'success')
        print(f"Cleared {report_count} reports and deleted {user_count} users")  # Debug
    except Exception as e:
        db.session.rollback()
        flash(f'Error clearing database: {str(e)}', 'error')
        print(f"Error clearing database: {str(e)}")  # Debug

    return redirect(url_for('admin.dashboard'))

@bp.route('/seed-data', methods=['POST'])
@login_required
@admin_required
def seed_data():
    """Generate sample data for prototyping"""
    try:
        print("Starting sample data generation...")  # Debug
        from app.services.sample_data import generate_sample_data
        result = generate_sample_data()
        print(f"Sample data result: {result}")  # Debug

        # Verify the data was created
        actual_users = User.query.count()
        actual_reports = WasteReport.query.count()

        flash(f'Sample data created: {result["users_created"]} users, {result["reports_created"]} reports. Total: {actual_users} users, {actual_reports} reports', 'success')
        print(f"Final counts - Users: {actual_users}, Reports: {actual_reports}")  # Debug
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        flash(f'Error creating sample data: {str(e)}', 'error')
        print(f"Sample data error details: {error_details}")  # Debug output

    return redirect(url_for('admin.dashboard'))

@bp.route('/debug')
@login_required
@admin_required
def debug():
    """Debug route to check database state"""
    users = User.query.all()
    reports = WasteReport.query.all()

    debug_info = {
        'total_users': len(users),
        'total_reports': len(reports),
        'users': [{'id': u.id, 'name': u.name, 'email': u.email, 'reports_count': u.reports_count, 'points': u.points} for u in users],
        'reports': [{'id': r.id, 'user_id': r.user_id, 'latitude': r.latitude, 'longitude': r.longitude, 'cluster_id': r.cluster_id} for r in reports[:5]]  # First 5 reports
    }

    return jsonify(debug_info)

@bp.route('/api/reports')
@login_required
@admin_required
def api_reports():
    """API endpoint for map data"""
    reports = WasteReport.query.filter(
        WasteReport.latitude.isnot(None),
        WasteReport.longitude.isnot(None)
    ).all()

    reports_data = []
    for report in reports:
        reports_data.append({
            'id': report.id,
            'latitude': report.latitude,
            'longitude': report.longitude,
            'cluster_id': report.cluster_id,
            'description': report.description or '',
            'image_filename': report.image_filename,
            'user_name': report.user.name,
            'created_at': report.created_at.isoformat()
        })

    return jsonify(reports_data)

