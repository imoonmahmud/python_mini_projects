from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from datetime import datetime, timezone

def now_utc():
    return datetime.now(timezone.utc)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

class PostModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    tags = db.Column(db.String(120))
    createdAt = db.Column(db.DateTime, default=now_utc)
    updatedAt = db.Column(db.DateTime, default=now_utc, onupdate=now_utc)

    def __repr__(self):
        return f'Post(title = {self.title}, category = {self.category})'

post_args = reqparse.RequestParser()
post_args.add_argument('title', type=str, required=True, help='Title cannot be blank')
post_args.add_argument('content', type=str, required=True, help='Content cannot be blank')
post_args.add_argument('category', type=str, required=True, help='Category cannot be blank')
post_args.add_argument('tags', type=list, location='json', required=False, help='Tags must be a list of strings')

class TagListField(fields.Raw):
    def format(self, value):
        if not value:
            return []
        return value.split(',')
postFields = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'category': fields.String,
    'tags': TagListField,
    'createdAt': fields.DateTime,
    'updatedAt': fields.DateTime
}

class Posts(Resource):
    @marshal_with(postFields)
    def get(self):
        term = request.args.get('term')

        if term:
            search = f'%{term}%'
            posts = PostModel.query.filter(
                db.or_(
                    PostModel.title.ilike(search),
                    PostModel.content.ilike(search),
                    PostModel.category.ilike(search)
                )
            ).all()
        else:
            posts = PostModel.query.all()
        return posts

    @marshal_with(postFields)
    def post(self):
        args = post_args.parse_args()
        tags_str = ",".join(args['tags']) if args['tags'] else ""
        post = PostModel(
            title=args['title'],
            content=args['content'],
            category=args['category'],
            tags=tags_str
        )
        db.session.add(post)
        db.session.commit()
        posts = PostModel.query.all()
        return posts, 201

class Post(Resource):
    @marshal_with(postFields)
    def get(self, id):
        post = PostModel.query.filter_by(id=id).first()
        if not post:
            abort(404, message='Post not found')
        return post

    @marshal_with(postFields)
    def patch(self, id):
        args = post_args.parse_args()
        post = PostModel.query.filter_by(id=id).first()
        if not post:
            abort(404, message='Post not found')

        if args['title'] is not None:
            post.title = args['title']
        if args['content'] is not None:
            post.content = args['content']
        if args['category'] is not None:
            post.category = args['category']
        if args['tags'] is not None:
            post.tags = ",".join(args['tags'])
        
        db.session.commit()
        return post

    @marshal_with(postFields)
    def delete(self, id):
        post = PostModel.query.filter_by(id=id).first()
        if not post:
            abort(404, message='Post not found')
        db.session.delete(post)
        db.session.commit()
        posts = PostModel.query.all()
        return posts, 204


api.add_resource(Posts, '/posts')
api.add_resource(Post, '/posts/<int:id>')

@app.route('/')
def home():
    return '<h3>Welcome to Blogging Platform API</h3>'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)