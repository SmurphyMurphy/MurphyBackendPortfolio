from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# import os
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://xmqergsgeyflvr:711d10d51bdb23c3084a15265c452c01afcbf9094e596bde4a170b808748cb93@ec2-44-215-22-37.compute-1.amazonaws.com:5432/dc276us7n0jcua'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    content = db.Column(db.String(144), unique=False)
    url = db.Column(db.String(100), unique=False)

    def __init__(self, title, content, url):
        self.title = title
        self.content = content
        self.url = url


class ProjectSchema(ma.Schema):
    class Meta:
        fields = ('title', 'content', 'url')


project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

# end point to create a new project
@app.route('/project', methods=["POST"])
def add_project():
    title = request.json['title']
    content = request.json['content']
    url = request.json['url']
    

    new_project = Project(title, content, url)

    db.session.add(new_project)
    db.session.commit()

    project = Project.query.get(new_project.id)

    return project_schema.jsonify(project)


# Endpoint to query all projects
@app.route("/projects", methods=["GET"])
def get_projects():
    all_projects = Project.query.all()
    result = projects_schema.dump(all_projects)
    return jsonify(result)

# Endpoint for querying a single project
@app.route("/project/<id>", methods=["GET"])
def get_project(id):
    project = Project.query.get(id)
    return project_schema.jsonify(project)



# Endpoint for updating a project
@app.route("/project/<id>", methods=["PUT"])
def project_update(id):
    project = Project.query.get(id)
    title = request.json['title']
    content = request.json['content']
    url = request.json['url']

    project.title = title
    project.content = content
    project.url = url

    db.session.commit()
    return project_schema.jsonify(project)


# Endpoint for deleting a record
@app.route("/project/<id>", methods=["DELETE"])
def project_delete(id):
    project = Project.query.get(id)
    db.session.delete(project)
    db.session.commit()

    return "Project was successfully deleted"



# app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "Justin": generate_password_hash("Cosmos98")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/auth')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())


if __name__ == '__main__':
    app.run(debug=True)