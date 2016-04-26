import sys
import os
import argparse

# Flask imports
import flask
import flask_flatpages
import flask_flatpages.utils
import flask_frozen

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
    prerendered_body = flask.render_template_string(text)
    print(text)
    return flask_flatpages.utils.pygmented_markdown(prerendered_body)

# Set up

app = flask.Flask(__name__)
app.config.from_object(__name__)
app.config['FLATPAGES_HTML_RENDERER'] = jinja_prerender
pages = flask_flatpages.FlatPages(app)
freezer = flask_frozen.Freezer(app)

# Route methods

@app.route('/')
def index():
    return flask.render_template('index.html', pages=pages,
        page={'title': 'factors'})

@app.route('/projects/<path:path>/')
def project_page(path):
    page = pages.get_or_404('projects/' + path)
    return flask.render_template('project_page.html', page=page)

@app.route('/posts/<path:path>/')
def posts_page(path):
    page = pages.get_or_404('posts/' + path)
    return flask.render_template('post_page.html', page=page)

@app.route('/tag/<string:tag>/')
def tag(tag):
    tagged = [p for p in pages if tag in p.meta.get('tags', [])]
    return flask.render_template('tag.html', pages=tagged,
        tag=tag, page={'title': 'tags'})

@app.route('/img/<path:path>/')
def img(path):
    return flask.send_from_directory('img', path)

@app.route('/js/<path:path>/')
def js(path):
    return flask.send_from_directory('js', path)

@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return flask.render_template('project_page.html', page=page)

# freezer URLs

@freezer.register_generator
def product_url_generator():
    # Return a list. (Any iterable type will do.)
    path_to_js  = os.path.join(os.path.dirname(__file__),
                               './js')
    path_to_img = os.path.join(os.path.dirname(__file__),
                              './img')

    js_urls  = ['/js/' + x for x in os.listdir(path_to_js)]
    img_urls = ['/img/' + x for x in os.listdir(path_to_img)]

    return js_urls + img_urls

# command line functions
def build(args):
    freezer.freeze()
    pass

def run(args):
    app.run(port=args.port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    build_parser = subparsers.add_parser('build')

    run_parser = subparsers.add_parser('run')
    run_parser.add_argumnent('-p', '--port',
                             help='Specify port',
                             nargs=1,
                             type=int,
                             default=8000)

    args = parser.parse_args()
