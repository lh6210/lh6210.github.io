
import sys 
from datetime import datetime

from flask import Flask, render_template, url_for 
from flask_flatpages import FlatPages
from flask_frozen import Freezer
import markdown
import mkdcomments
import pymdownx.arithmatex as arithmatex

#FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
DEBUG = True
# attr_list: heading anchor
# pymdownx.arithmatex: latex
# tables: table


extension_configs= {
    "pymdownx.highlight": {
        "pygments_style" : "tango",
        "noclasses": True,
        "linenums": True
        }
}

comments = mkdcomments.CommentsExtension()


md = markdown.Markdown(extensions=['tables', 'attr_list', 'pymdownx.highlight', 'pymdownx.inlinehilite', 'pymdownx.arithmatex', comments, 'pymdownx.superfences'], extension_configs=extension_configs)

def my_renderer(text):
    return md.convert(text)

app = Flask(__name__)
app.config.from_object(__name__)
app.config['FLATPAGES_HTML_RENDERER'] = my_renderer

pages = FlatPages(app)

freezer = Freezer(app)

@app.route('/')
def index():
    return render_template('index.html', pages=pages)

@app.route('/cal2')
def cc():
    return render_template('doubleintegral.html')


@app.route('/<path:path>.html')
def page(path):
    print('Page function running')
    page = pages.get_or_404(path)
    print(f'page is {page}')
    return render_template('page.html', page=page)

@freezer.register_generator
def pagelist():
    for page in pages:
        yield url_for('page', path=page.path)



if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', port= 5001)
