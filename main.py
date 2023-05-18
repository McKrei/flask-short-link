import datetime
import random
import string

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SECRET_KEY'] = 'SECRET_KEY'

db = SQLAlchemy(app)


class URLmodel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(255))
    short = db.Column(db.String(6), unique=True)
    visits = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)


class URLForm(FlaskForm):
    original_url = StringField('Вставьте ссылку',
                               validators=[DataRequired(message='Ссылка не может быть пустой'),
                                           URL(message='Неверная ссылка')])
    submit = SubmitField('Получить короткую ссылку')


db.create_all()

def generate_random_string(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def get_short():
    while True:
        short = generate_random_string()
        if URLmodel.query.filter(URLmodel.short == short).first():
            continue
        return short


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if form.validate_on_submit():
        url = URLmodel()
        url.original_url = form.original_url.data
        url.short = get_short()
        db.session.add(url)
        db.session.commit()
        return redirect(url_for('urls'))
    return render_template('index.html', form=form)


@app.route('/urls', methods=['GET'])
def urls():
    urls = URLmodel.query.all()
    return render_template('urls.html', urls=urls)


@app.route('/<string:short>', methods=['GET'])
def url_redirect(short):
    pass


if __name__ == '__main__':
    app.run(debug=True)
