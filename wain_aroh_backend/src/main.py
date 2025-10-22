import os
import sys
import secrets
import warnings
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.api import api_bp
from src.routes.telephony import telephony_bp
from src.routes.enhanced_api import enhanced_api_bp
from src.routes.conversation_api import conversation_api_bp
from src.routes.settings_api import settings_api_bp
from src.routes.admin_api import admin_api_bp
from src.routes.recommendations_api import recommendations_bp
from src.routes.search_api import search_bp
from src.routes.metrics_api import metrics_bp
from src.routes.appointment_api import appointment_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'))

# Configure SECRET_KEY - use environment variable or generate secure random key with warning
if 'SECRET_KEY' not in os.environ:
    warnings.warn(
        "SECRET_KEY not set in environment. Using auto-generated key. "
        "Sessions will be invalidated on restart. "
        "Set SECRET_KEY in Replit Secrets for production!",
        UserWarning
    )
    app.config['SECRET_KEY'] = secrets.token_hex(32)
else:
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

# Enable CORS
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(telephony_bp)
app.register_blueprint(enhanced_api_bp)
app.register_blueprint(conversation_api_bp)
app.register_blueprint(settings_api_bp)
app.register_blueprint(admin_api_bp, url_prefix='/api/admin')
app.register_blueprint(recommendations_bp)
app.register_blueprint(search_bp)
app.register_blueprint(metrics_bp)
app.register_blueprint(appointment_bp)

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        response = send_from_directory(static_folder_path, path)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            response = send_from_directory(static_folder_path, 'index.html')
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
