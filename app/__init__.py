# app/__init__.py

import os
import yaml
from flask import Flask, send_from_directory, request, render_template
from .extensions import mongo
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app():
    from flask import Flask, send_from_directory, request, render_template
    from werkzeug.middleware.proxy_fix import ProxyFix
    import os
    import yaml
    from .extensions import mongo

    # 1) Create the Flask app
    app = Flask(__name__, static_folder='../static')

    # 2) Trust X-Forwarded headers from Nginx
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

    # 3) Load all settings from config/config.yaml
    config_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    )
    with open(config_path, 'r') as f:
        cfg = yaml.safe_load(f)
    app.config.update(cfg)

    # 4) Secret key handling
    secret = app.config.get('FLASK_SECRET')
    if not secret or secret == 'fallback-secret-key':
        # Show friendly error if SECRET_KEY is missing or insecure
        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def config_error(path):
            return render_template(
                "config_error.html",
                message="SECRET_KEY is missing or not securely configured. Please fix config.yaml."
            ), 500
        return app  # Return early to avoid session errors
    else:
        app.secret_key = secret

    # 5) Initialize extensions
    mongo.init_app(app, uri=app.config['MONGO_URI'])

    # 6) Register Blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    from app.edit_pages import edit_pages
    app.register_blueprint(edit_pages)

    # 7) Static file routes
    @app.route('/robots.txt')
    def robots_txt():
        return send_from_directory(app.static_folder, 'robots.txt')

    @app.route('/sitemap.xml')
    def sitemap_xml():
        response = send_from_directory(app.static_folder, 'sitemap.xml')
        response.direct_passthrough = False
        response.mimetype = 'application/xml'
        return response

    # 8) Maintenance mode check
    @app.before_request
    def check_maintenance_mode():
        if os.path.exists("MAINTENANCE_MODE"):
            allowed_ip = "192.31.112.152"
            if request.remote_addr != allowed_ip and request.endpoint not in ("static",):
                return render_template("maintenance.html"), 503

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404



    return app


# Instantiate the app using our factory
app = create_app()

if __name__ == '__main__':
    # DEBUG now comes from config.yaml (e.g. DEBUG: true/false)
    app.run(debug=app.config.get('DEBUG', False))
