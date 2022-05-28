import json
from urllib.request import urlopen
from dbservice import dbservice

URL_FOR_USERS = "https://jsonplaceholder.typicode.com/users"
URL_FOR_POSTS = "https://jsonplaceholder.typicode.com/posts"
URL_FOR_COMMENTS = "https://jsonplaceholder.typicode.com/comments"

db = dbservice()

response_users = urlopen(URL_FOR_USERS)
response_posts = urlopen(URL_FOR_POSTS)
response_comments = urlopen(URL_FOR_COMMENTS)

json_data_of_users = json.loads(response_users.read())
json_data_of_posts = json.loads(response_posts.read())
json_data_of_comments = json.loads(response_comments.read())

# adding users fetched from API to database
for user in json_data_of_users:
    db.add_user(user)

# adding posts fetched from API to database
for post in json_data_of_posts:
    db.add_post(post)

# adding comments fetched from API to database
for comment in json_data_of_comments:
    db.add_comment(comment)

