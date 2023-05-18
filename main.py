from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', current='index')


@app.route('/urls', methods=['GET'])
def urls():
    return render_template('urls.html', current='news')


@app.route('/<string:short>', methods=['GET'])
def url_redirect(short):
    pass


if __name__ == '__main__':
    app.run(debug=True)
