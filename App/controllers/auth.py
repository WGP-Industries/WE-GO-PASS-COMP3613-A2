from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request, get_jwt
from App.models import User, Student, Employer, Staff
from App.database import db

def login(username, password, user_type):
    try:
        model_map = {
            'student': Student,
            'employer': Employer,
            'staff': Staff
        }
        model = model_map.get(user_type)
        if not model:
            return None
        
        user = db.session.execute(db.select(model).filter_by(username=username)).scalar_one_or_none()
        if user and user.check_password(password):
            return create_access_token(
                identity=str(user.id),
                additional_claims={"type": user_type}
            )
        return None
    except Exception as e:
        print("Login error:", e)
        return None

def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        user_id = getattr(identity, "id", identity)
        return str(user_id) if user_id is not None else None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        user_type = jwt_data.get("type")
        model_map = {
            "student": Student,
            "employer": Employer,
            "staff": Staff
        }
        model = model_map.get(user_type, User)
        try:
            return db.session.get(model, int(identity))
        except Exception as e:
            print("Lookup error:", e)
            return None

    return jwt

def add_auth_context(app):
    @app.context_processor
    def inject_user():
        try:
            verify_jwt_in_request()
            identity = get_jwt_identity()
            jwt_data = get_jwt()
            user_type = jwt_data.get("type") if jwt_data else None
            user_id = int(identity) if identity is not None else None
            model_map = {
                "student": Student,
                "employer": Employer,
                "staff": Staff
            }
            model = model_map.get(user_type, User)
            current_user = db.session.get(model, user_id) if user_id is not None else None
            is_authenticated = current_user is not None
        except Exception as e:
            print(e)
            is_authenticated = False
            current_user = None
        return dict(is_authenticated=is_authenticated, current_user=current_user)
