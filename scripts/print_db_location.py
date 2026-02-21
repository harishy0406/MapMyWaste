from app import create_app

app = create_app()
import os
print('cwd:', os.getcwd())
print('app.root_path:', app.root_path)
print('SQLALCHEMY_DATABASE_URI:', app.config.get('SQLALCHEMY_DATABASE_URI'))
uri = app.config.get('SQLALCHEMY_DATABASE_URI')
if uri and uri.startswith('sqlite:///'):
    path = uri.replace('sqlite:///', '')
    print('resolved DB path:', os.path.abspath(path), os.path.exists(path))
else:
    print('DB not sqlite or not set')
