
from flask import Flask
from flask_restx import Api, Resource, fields
from dbservice import dbservice

app = Flask(__name__)
api = Api(app, title='Jorden & Sky API',
    description='A simple API service',
)

ns = api.namespace('UserData', description='CRUD Operations on User Data')

# model for address of user
address_dict = {}
address_dict['street'] = fields.String()
address_dict['suite'] = fields.String()
address_dict['city'] = fields.String()
address_dict['zipcode'] = fields.String()
address_dict['geo'] = fields.Nested(
    api.model('geo', {'lat': fields.String, 'lng': fields.String})
)
address_dict_payload = api.model('address', address_dict)

# model for company related data of user
company_dict = {}
company_dict['name'] = fields.String()
company_dict['catchPhrase'] = fields.String()
company_dict['bs'] = fields.String()
company_dict_payload = api.model('company', company_dict)

# model for User
user = api.model('User', {
    'id': fields.Integer(),
    'name': fields.String(),
    'username': fields.String(),
    'email': fields.String(),
    'address': fields.Nested(address_dict_payload),
    'phone': fields.String(),
    'website': fields.String(),
    'company': fields.Nested(company_dict_payload)
})

# model for Post
post = api.model('Post', {
    'userId': fields.Integer(),
    'id': fields.Integer(),
    'title': fields.String(),
    'body': fields.String()
})

# model for Comment
comment = api.model('Comment', {
    'postId': fields.Integer(),
    'id': fields.Integer(),
    'name': fields.String(),
    'email': fields.String(),
    'body': fields.String()
})


class userDAO(object):
    '''Data Access Object Class for User'''

    def __init__(self) -> None:
        self.db = dbservice()
        self.users = []
        records = self.db.read_users()
        header = ['id', 'name', 'username', 'email', 'phone', 'website']
        for record in records:
            self.users.append(dict(zip(header, record[0:6])))
        for i, record in enumerate(records):
            self.users[i]['company'] = dict(zip(['name', 'catchPhrase', 'bs'], record[12:]))
            self.users[i]['address'] = dict(zip(['street', 'suite', 'city', 'zipcode'], record[6:10]))
        for i, record in enumerate(records):
            self.users[i]['address']['geo'] = dict(zip(['lat', 'lng'], record[10:12]))
 
    def get(self, id):
        for user in self.users:
            if user['id'] == id:
                return user
        api.abort(404, f"User with id {id} not Found!")
    
    def create(self, data):
        user = data
        self.db.add_user(data)
        return user
    
    def delete(self, id):
        self.db.delete_record('USER', id)


class PostDAO(object):
    '''Data Access Object Class for Post'''

    def __init__(self) -> None:
        self.db = dbservice()
        self.posts = []
        records = self.db.read_posts()
        header = ["userId", "id", "title", "body"]
        for record in records:
            self.posts.append(dict(zip(header, record)))
    
    def get(self, id):
        for post in self.posts:
            if post['id'] == id:
                return post
        api.abort(404, f"Post with id {id} not Found!")
    
    def create(self, data):
        post = data
        self.db.add_post(data)
        return post
    
    def delete(self, id):
        self.db.delete_record('POST', id)


class commentDAO(object):
    '''Data Access Object Class for Comment'''

    def __init__(self) -> None:
        self.db = dbservice()
        self.comments = []
        records = self.db.read_comments()
        header = ["postId", "id", "name", "email", "body"]
        for record in records:
            self.comments.append(dict(zip(header, record)))
    
    def get(self, id):
        for comment in self.comments:
            if comment['id'] == id:
                return comment
        api.abort(404, f"Comment with id {id} not Found!")
    
    def create(self, data):
        comment = data
        self.db.add_comment(data)
        return comment
    
    def delete(self, id):
        self.db.delete_record('COMMENT', id)


# Data Access Object instances for User, Post and Comment
DAO_user = userDAO()
DAO_post = PostDAO()
DAO_comment = commentDAO()


@ns.route('/users')
class CommentList(Resource):
    '''Shows a list of all users, and lets you make POST request to add new user'''

    @ns.doc('list_users')
    @ns.marshal_list_with(user)
    def get(self):
        '''List all users'''
        return DAO_user.users

    @ns.doc('create_user')
    @ns.expect(user)
    @ns.marshal_with(user, code=201)
    def post(self):
        '''Create a new user'''
        return DAO_user.create(api.payload), 201


@ns.route('/users/<int:id>')
@ns.response(404, 'User not found')
@ns.param('id', 'The user identifier')
class Comment(Resource):
    '''Shows a single user and lets you delete them'''

    @ns.doc('get_user')
    @ns.marshal_with(user)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO_user.get(id)

    @ns.doc('delete_user')
    @ns.response(204, 'user deleted')
    def delete(self, id):
        '''Delete a user given its identifier'''
        DAO_user.delete(id)
        return '', 204


@ns.route('/posts')
class PostList(Resource):
    '''Shows a list of all posts, and lets you make a POST request to add new post'''

    @ns.doc('list_posts')
    @ns.marshal_list_with(post)
    def get(self):
        '''List all posts'''
        return DAO_post.posts

    @ns.doc('create_post')
    @ns.expect(post)
    @ns.marshal_with(post, code=201)
    def post(self):
        '''Create a new post'''
        return DAO_post.create(api.payload), 201


@ns.route('/posts/<int:id>')
@ns.response(404, 'Post not found')
@ns.param('id', 'The post identifier')
class Post(Resource):
    '''Shows a single post and lets you delete it'''
    @ns.doc('get_post')
    @ns.marshal_with(post)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO_post.get(id)

    @ns.doc('delete_post')
    @ns.response(204, 'post deleted')
    def delete(self, id):
        '''Delete a post given its identifier'''
        DAO_post.delete(id)
        return '', 204


@ns.route('/comments')
class CommentList(Resource):
    '''Shows a list of all comments, and lets you make POST request to add new comment'''

    @ns.doc('list_comments')
    @ns.marshal_list_with(comment)
    def get(self):
        '''List all comments'''
        return DAO_comment.comments

    @ns.doc('create_comment')
    @ns.expect(comment)
    @ns.marshal_with(comment, code=201)
    def post(self):
        '''Create a new comment'''
        return DAO_comment.create(api.payload), 201


@ns.route('/comments/<int:id>')
@ns.response(404, 'Comment not found')
@ns.param('id', 'The comment identifier')
class Comment(Resource):
    '''Show a single comment and lets you delete it'''

    @ns.doc('get_comment')
    @ns.marshal_with(comment)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO_comment.get(id)

    @ns.doc('delete_comment')
    @ns.response(204, 'comment deleted')
    def delete(self, id):
        '''Delete a comment given its identifier'''
        DAO_comment.delete(id)
        return '', 204


if __name__ == '__main__':
    app.run(debug=True)
