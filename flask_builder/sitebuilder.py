import sys
import os

from flask import Flask, render_template, render_template_string, send_from_directory
from flask_flatpages import FlatPages
from flask_flatpages.utils import pygmented_markdown
from flask_frozen import Freezer

# Flask configurations
DEBUG = True

# Flask flat pages configurations
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.html'

# Freezer configurations
FREEZER_DESTINATION = '..\\'
FREEZER_REMOVE_EXTRA_FILES = False


# Utils

def jinja_prerender(text):
    prerendered_body = render_template_string(text)
    print text
    return pygmented_markdown(prerendered_body)

# Set up

app = Flask(__name__)
app.config.from_object(__name__)
# app.config['FLATPAGES_HTML_RENDERER'] = jinja_prerender
pages = FlatPages(app)
freezer = Freezer(app)

# Route methods

@app.route('/')
def index():
    return render_template('index.html', pages=pages,
        page={'title': 'factors'})

@app.route('/projects/<path:path>/')
def project_page(path):
    page = pages.get_or_404('projects/' + path)
    return render_template('project_page.html', page=page)

@app.route('/posts/<path:path>/')
def posts_page(path):
    page = pages.get_or_404('posts/' + path)
    return render_template('post_page.html', page=page)

@app.route('/tag/<string:tag>/')
def tag(tag):
    tagged = [p for p in pages if tag in p.meta.get('tags', [])]
    return render_template('tag.html', pages=tagged,
        tag=tag, page={'title': 'tags'})

@app.route('/img/<path:path>/')
def img(path):
    return send_from_directory('img', path)

@app.route('/js/<path:path>/')
def js(path):
    return send_from_directory('js', path)

@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('project_page.html', page=page)

# freezer URLs

@freezer.register_generator
def product_url_generator():
    # Return a list. (Any iterable type will do.)
    path_to_js  = os.path.join(os.path.dirname(__file__),
                               './js')
    path_to_img = os.path.join(os.path.dirname(__file__),
                              './img')

    js_urls  = map(lambda x: '/js/' + x , os.listdir(path_to_js))
    img_urls = map(lambda x: '/img/' + x, os.listdir(path_to_img))

    return js_urls + img_urls



if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    else:
        app.run(port=8000)
