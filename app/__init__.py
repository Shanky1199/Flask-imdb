def init_app(app, jwt):
    # Import routes after app is created
    from app.routes import user_routes

    # Register routes with the app
    app.register_blueprint(user_routes)

    # Initialize JWTManager in routes
    jwt.init_app(app)
