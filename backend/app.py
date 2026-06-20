from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    from routes.store_routes import store_bp
    from routes.project_routes import project_bp
    from routes.employee_routes import employee_bp
    from routes.member_routes import member_bp
    from routes.channel_routes import channel_bp
    from routes.export_routes import export_bp
    from routes.warning_routes import warning_bp
    
    app.register_blueprint(store_bp, url_prefix='/api/v1/stores')
    app.register_blueprint(project_bp, url_prefix='/api/v1/projects')
    app.register_blueprint(employee_bp, url_prefix='/api/v1/employees')
    app.register_blueprint(member_bp, url_prefix='/api/v1/members')
    app.register_blueprint(channel_bp, url_prefix='/api/v1/channels')
    app.register_blueprint(export_bp, url_prefix='/api/v1/export')
    app.register_blueprint(warning_bp, url_prefix='/api/v1/warnings')
    
    @app.route('/api/v1/health')
    def health_check():
        return {'code': 200, 'message': 'success', 'data': {'status': 'ok'}}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
