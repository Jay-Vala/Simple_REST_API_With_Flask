from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from  flask_restful import Resource, Api, reqparse, fields, marshal_with, abort


# Initializing flask App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    # Adding representation of the User Model
    def __repr__(self):
        return f"username = {self.name}, email = {self.email}"
        
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="email cannot be blank")

UserFields={
    'id':fields.Integer,
    'name':fields.String,
    'email':fields.String
}

class Users(Resource):
    
    @marshal_with(UserFields) # Specifying the structure/shape of the returned data
    def get(self):
        users = UserModel.query.all()
        return users

    @marshal_with(UserFields)
    def post(self):
        args = user_args.parse_args()
        name = args['name']
        email = args['email']
        user = UserModel(name=name, email=email)    #Creating User Model
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201

class User(Resource):

    @marshal_with(UserFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User Not Found")
        else:
            return user, 200
        
    @marshal_with(UserFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User Not Found")
        else:
            user.email = args['email']
            user.name = args['name']
            db.session.commit()
            return user, 200
        
    @marshal_with(UserFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User Not Found")
        else:
            users = UserModel.query.all()
            db.session.delete(user)
            db.session.commit()
            return users, 200


#Attaching an Endpoint to users class
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')

@app.route('/')
def home():
    return "<h1>Flask REST</h1>"

if __name__=='__main__':
    app.run(debug=True)

