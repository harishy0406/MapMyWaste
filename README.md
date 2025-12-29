

## Features

- 📸 **Image Upload with GPS Extraction**: Automatically extract GPS coordinates from EXIF data or use browser geolocation
- 🗺️ **Interactive Maps**: View waste reports and clusters on Leaflet.js maps
- 🤖 **K-Means Clustering**: AI-powered clustering groups reports into optimal collection zones
- 🎮 **Gamification**: Earn points, unlock badges, and compete on leaderboards
- 👥 **User Management**: Registration, authentication, and user profiles
- 🔐 **Admin Dashboard**: Manage reports, run clustering, and view analytics

## Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML/CSS/JavaScript with Bootstrap 5
- **Maps**: Leaflet.js with OpenStreetMap
- **ML**: scikit-learn KMeans clustering
- **Image Processing**: Pillow for EXIF extraction

## Installation

1. **Clone the repository** (or navigate to project directory)

2. **Create a virtual environment**:
```bash
python -m venv venv
```

3. **Activate the virtual environment**:
   - Windows:
   ```bash
   venv\Scripts\activate
   ```
   - Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

5. **Initialize the database**:
```bash
python run.py
```
This will create the database tables and an admin user:
- Email: `admin@mapmywaste.com`
- Password: `admin123`

**⚠️ Important**: Change the admin password in production!

6. **Run the application**:
```bash
python run.py
```

The app will be available at `http://localhost:5000`

## Project Structure

```
MapMyWaste/
├── app/
│   ├── __init__.py          # App factory
│   ├── models.py            # Database models
│   ├── auth/                # Authentication blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── main/                # Main blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── admin/               # Admin blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── services/            # Service utilities
│   │   ├── exif_utils.py    # GPS extraction from images
│   │   ├── clustering.py    # K-means clustering
│   │   └── gamification.py  # Points and badges
│   ├── templates/           # Jinja2 templates
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── main/
│   │   └── admin/
│   └── static/              # Static files
│       ├── css/
│       ├── js/
│       └── uploads/         # Uploaded images
├── config.py                # Configuration
├── run.py                   # Application entry point
└── requirements.txt         # Python dependencies
```

## Usage

### For Users

1. **Register/Login**: Create an account or login
2. **Report Waste**: Upload an image with GPS coordinates (from EXIF or device location)
3. **Earn Points**: Get points for each report and unlock badges
4. **View Leaderboard**: See top contributors

### For Administrators

1. **Dashboard**: View statistics and recent reports
2. **Run Clustering**: Group reports into clusters using K-means
3. **View Map**: See all reports and centroids on an interactive map
4. **Route Links**: Get Google Maps routes from depot to cluster centroids

## Configuration

Edit `config.py` to customize:

- **Depot Location**: Set `DEPOT_LAT` and `DEPOT_LON` for route links
- **Clustering**: Adjust `DEFAULT_CLUSTERS` and `MIN_REPORTS_PER_CLUSTER`
- **Gamification**: Modify point values and badge thresholds
- **Upload Settings**: Change `MAX_CONTENT_LENGTH` and `ALLOWED_EXTENSIONS`

## Badges

- **Rookie Reporter**: Submit your first report
- **Neighborhood Watcher**: Submit 5 reports
- **Waste Warrior**: Submit 20 reports

## API Endpoints

- `GET /` - Landing page
- `GET /auth/register` - Registration page
- `GET /auth/login` - Login page
- `POST /auth/logout` - Logout
- `GET /upload` - Upload waste report (login required)
- `GET /profile` - User profile (login required)
- `GET /leaderboard` - Leaderboard
- `GET /admin` - Admin dashboard (admin only)
- `POST /admin/cluster` - Run clustering (admin only)
- `GET /admin/map` - Admin map view (admin only)

## Development

### Database Reset

To reset the database, delete `mapmywaste.db` and run `python run.py` again.

### Adding New Features

1. Create new routes in appropriate blueprint
2. Add templates in `app/templates/`
3. Update models if database changes needed
4. Run migrations or recreate database

## License

This project is open source and available for educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please contact through the contact form on the website.

