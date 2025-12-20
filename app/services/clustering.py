from app import db
from app.models import WasteReport
from sklearn.cluster import KMeans
import numpy as np
from config import Config

def run_clustering(k=None):
    """
    Run K-means clustering on waste reports with valid coordinates.
    Returns dict with cluster info and centroids.
    """
    # Fetch all reports with valid coordinates
    reports = WasteReport.query.filter(
        WasteReport.latitude.isnot(None),
        WasteReport.longitude.isnot(None)
    ).all()
    
    if len(reports) < 2:
        return {
            'success': False,
            'message': 'Not enough reports for clustering (need at least 2)',
            'clusters': 0,
            'centroids': []
        }
    
    # Prepare data
    coords = np.array([[r.latitude, r.longitude] for r in reports])
    
    # Determine k if not provided
    if k is None:
        k = min(Config.DEFAULT_CLUSTERS, max(1, len(reports) // Config.MIN_REPORTS_PER_CLUSTER))
        k = max(1, min(k, len(reports)))  # Ensure k is between 1 and n_reports
    
    if k > len(reports):
        k = len(reports)
    
    # Run K-means
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(coords)
    
    # Update cluster_id for each report
    for i, report in enumerate(reports):
        report.cluster_id = int(labels[i])
    
    # Calculate centroids
    centroids = []
    for cluster_id in range(k):
        cluster_reports = [r for r in reports if r.cluster_id == cluster_id]
        if cluster_reports:
            avg_lat = sum(r.latitude for r in cluster_reports) / len(cluster_reports)
            avg_lon = sum(r.longitude for r in cluster_reports) / len(cluster_reports)
            centroids.append({
                'cluster_id': cluster_id,
                'latitude': avg_lat,
                'longitude': avg_lon,
                'count': len(cluster_reports)
            })
    
    db.session.commit()
    
    return {
        'success': True,
        'message': f'Clustering completed: {k} clusters created',
        'clusters': k,
        'centroids': centroids,
        'total_reports': len(reports)
    }

