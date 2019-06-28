from flask import Flask, render_template, url_for, current_app, abort
import cf
from flaskext.markdown import Markdown
from flask_caching import Cache


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
Markdown(app)

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)


@app.route("/")
@cache.cached(timeout=60*60*24)
def index():
    posts = cf.client.entries({ 'content_type': 'blogPost', 'order': '-sys.createdAt' })
    return render_template("index.html",posts=posts)
    
@app.route("/test/")
def index_grid():
    return render_template("layout.grid.html")    

@app.route("/<path:path>/")
@cache.cached(timeout=60*60*24)
def post(path):
    
    if path in cf.get_post_urls():
        posts = cf.client.entries({ 'fields.url' : (path or request.path), 'content_type': 'blogPost', 'limit' : 1})
        
        if len(posts) == 0:
            abort(404)
        else:  
            content = render_template("post.html",post=posts[0])    
            content =  content.replace("<p><img",'<p class="wide"><img')
            content = content.replace('src="//images','src="data:image/gif;base64,R0lGODdhAQABAPAAAMPDwwAAACwAAAAAAQABAAACAkQBADs=" class="lazyload" data-src="//images')
            return content
    else:
        abort(404)
        
@app.route("/admin/clear")
def clear_urls():
    
    cf.clear_post_urls()
    return "OK"
    

@app.context_processor
def utility_processor():
    def static(filename):
        return url_for("static", filename=filename)
    return dict(static=static)    
