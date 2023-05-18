import datetime

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'

db = SQLAlchemy(app)


class URLmodel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(255))
    short = db.Column(db.String(6), unique=True)
    visits = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)


db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET'])
def urls():
    urls = URLmodel.query.all()
    return render_template('urls.html', urls=urls)


@app.route('/<string:short>', methods=['GET'])
def url_redirect(short):
    pass


if __name__ == '__main__':
    app.run(debug=True)
