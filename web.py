from flask import Flask, render_template, url_for, current_app, abort
import cf
from flaskext.markdown import Markdown
from flask_caching import Cache
import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
Markdown(app)

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

@app.route("/")
@cache.cached(timeout=0)
def index():
    posts = cf.client.entries({ 'content_type': 'blogPost', 'order': '-sys.createdAt' })
    return render_template("index.html",posts=posts)
    
@app.route("/<path:path>/")
@cache.cached(timeout=0)
def post(path):
    
    posts = cf.client.entries({ 'fields.url' : (path or request.path), 'content_type': 'blogPost', 'limit' : 1})
    
    if len(posts) == 0:
        abort(404)
    else:  
        content = render_template("post.html",post=posts[0])    
        content = content.replace('src="//images','src="data:image/gif;base64,R0lGODdhAQABAPAAAMPDwwAAACwAAAAAAQABAAACAkQBADs=" width="100%" class="lazyload img10" data-src="//images')
        return content
        
@app.route("/clear/")
def claer_cache():
    
    cache.clear()
    
    return "OK"

@app.context_processor
def utility_processor():
    
    def static(filename):
        return url_for("static", filename=filename)
        
    return dict(static=static, now=datetime.datetime.utcnow())
