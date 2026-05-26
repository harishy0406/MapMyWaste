# MapMyWaste

MapMyWaste is a Flask-based waste reporting and route optimization platform built to help communities identify garbage hotspots, cluster reports, and support smarter collection planning.

## Overview

The application lets users submit waste reports with images and location data, then uses clustering and mapping tools to help administrators visualize patterns and plan efficient collection routes.

## Key Features

- Image upload with GPS extraction from EXIF metadata or browser geolocation
- Interactive maps for report visualization and cluster review
- K-means clustering to group nearby reports into collection zones
- Gamification with points, badges, and leaderboards
- User authentication, profiles, and reporting history
- Admin dashboard for review, clustering, routing, and operations

## Tech Stack

- Backend: Python Flask
- Database: SQLite with SQLAlchemy ORM
- Frontend: HTML, CSS, JavaScript, and Bootstrap 5
- Maps: Leaflet.js with OpenStreetMap
- Machine Learning: scikit-learn KMeans clustering
- Image Processing: Pillow for EXIF extraction

## Getting Started

1. Create and activate a virtual environment.

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install the project dependencies.

   ```bash
   pip install -r requirements.txt
   ```

3. Start the application.

   ```bash
   python run.py
   ```

The app will be available at `http://localhost:5000`.

## Usage

### For Users

- Register or sign in
- Submit a waste report with an image and location
- Earn points and unlock badges
- Track progress on the leaderboard

### For Administrators

- Review dashboard metrics and recent reports
- Run clustering to group waste reports
- View reports and centroids on the map
- Generate route links from the depot to cluster centroids

## Snapshot

Add your application screenshots here.

- Dashboard screenshot: replace this line with your image
- Map view screenshot: replace this line with your image
- Report upload screenshot: replace this line with your image
- Leaderboard screenshot: replace this line with your image

You can add images in a folder such as `images/` and link them here when ready.

## Hackathon Recognition

MapMyWaste won first prize at a national hackathon in Chennai. This section can be used to highlight the achievement and add your photo when you want to present the project story more strongly.

- Award title: First Prize, National Hackathon, Chennai
- Photo placeholder: add your photo here

## Project Structure

```
MapMyWaste/
├── app/
│   ├── admin/
│   ├── auth/
│   ├── main/
│   ├── services/
│   ├── static/
│   └── templates/
├── config.py
├── requirements.txt
├── run.py
└── scripts/
```

## Configuration

Edit `config.py` to customize the application:

- Depot location for route generation
- Clustering defaults and minimum report thresholds
- Gamification point values and badge rules
- Upload limits and allowed file types

## Badges

- Rookie Reporter: Submit your first report
- Neighborhood Watcher: Submit 5 reports
- Waste Warrior: Submit 20 reports

## API Endpoints

- `GET /` - Landing page
- `GET /auth/register` - Registration page
- `GET /auth/login` - Login page
- `POST /auth/logout` - Logout
- `GET /upload` - Upload waste report
- `GET /profile` - User profile
- `GET /leaderboard` - Leaderboard
- `GET /admin` - Admin dashboard
- `POST /admin/cluster` - Run clustering
- `GET /admin/map` - Admin map view

## Development Notes

- To reset the database, delete the local database file and run `python run.py` again.
- Add new routes in the appropriate blueprint under `app/`.
- Add new templates in `app/templates/`.
- Update models when the database schema changes.

## Contributing

Contributions are welcome. Please open a pull request for improvements, bug fixes, or feature additions.

## License

This project is open source and intended for educational and demonstration purposes.

## Support

For questions or issues, use the contact form in the application.


