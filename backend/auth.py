from flask import jsonify, request, make_response # Flask
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

authNS = Namespace('auth', description="A namespace for authentication")

# Register Model Serializer
registerModel = authNS.model("Register", {
    "username": fields.String(),
    "email": fields.String(),
    "password": fields.String()
})

# Login Model Serializer
loginModel = authNS.model("Login", {
    "username": fields.String(),
    "password": fields.String()
})

@authNS.route('/register')
class Register(Resource):
    @authNS.expect(registerModel)
    def post(self):
        data = request.get_json()

        username = data.get('username')

        dbUser = User.query.filter_by(username=username).first()
        if dbUser is not None:
            return jsonify({"message":f"User with username {username} already exists."})
        
        newUser = User(
            username = data.get('username'),
            email = data.get('email'),
            password = generate_password_hash(data.get('password'))
        )

        newUser.save()

        return make_response(jsonify({"message": "User created successfully!"}), 201) # Generates a JSON message along with a status code for unit testing

@authNS.route('/login')
class Login(Resource):
    @authNS.expect(loginModel)
    def post(self):
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        dbUser = User.query.filter_by(username=username).first()

        if dbUser and check_password_hash(dbUser.password, password):
            accessToken = create_access_token(identity=dbUser.username)
            refreshToken = create_refresh_token(identity=dbUser.username)

            return make_response(jsonify({
                "accessToken": accessToken, "refreshToken": refreshToken
                }), 200)
        
@authNS.route('/refresh')
class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        currentUser = get_jwt_identity()
        newAccessToken = create_access_token(identity=currentUser)

        return make_response(jsonify({"accessToken" : newAccessToken}), 200)