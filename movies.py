# -*- coding: utf-8 -*-
import requests
from cgi import escape
from flask import Flask
from flask import render_template, redirect
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import Required

app = Flask(__name__)

api_key = "Your api key"


def search_movie_list(keyword):
    url = 'http://api.themoviedb.org/3/search/movie?api_key=%s&query=%s' % (api_key, escape(keyword))
    res = requests.get(url)
    # convert json response in to python dict
    return res.json()


def get_movie_detail(movie_id):
    url = 'https://api.themoviedb.org/3/movie/%s?api_key=%s' % (movie_id, api_key)
    res = requests.get(url)
    # convert json response in to python dict
    import json
    return json.loads(res.content)


class SearchForm(Form):
    name = StringField('Movie Name', validators=[Required()])


@app.route('/', methods=('GET', 'POST'))
def home():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect('/list/%s' % (escape(form.name.data)))
    return render_template('home.html', form=form)


@app.route('/list/<keyword>', methods=('GET', 'POST'))
def movie_list(keyword):
    form = SearchForm()
    result = search_movie_list(keyword)
    # import pprint
    # pprint.pprint(result)
    return render_template('list.html', result=result, form=form, keyword=keyword)


@app.route('/movie_detail/<movie_id>')
def movie_detail(movie_id):
    result = get_movie_detail(movie_id)
    # import pprint
    # pprint.pprint(result)
    return render_template('details.html', result=result)


if __name__ == '__main__':
    app.secret_key = 's3cr3t'
    app.run(debug=True)
