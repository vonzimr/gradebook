from flask_jwt_extended import (JWTManager, get_jwt_identity,
                                jwt_required,
                               create_access_token, get_jwt_claims)
jwt = JWTManager()

@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'roles' : user.get_roles()}

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username
