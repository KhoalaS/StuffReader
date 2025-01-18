import sqlite3
from lib.registry import Registry
from lib.gallery_state import DbService
from flask import Flask, g, render_template, request, make_response
from requests import session
from extensions import webtoons

con = sqlite3.connect("./data.db")

registry = Registry()
registry.register(webtoons.Ext(con))
db_service = DbService()

app = Flask(__name__)

proxy_session = session()

# TODO chapter support


@app.get("/@<ext_handle>/g/<id>")
def gallery(ext_handle: str, id: int):
    if registry.getExtension(ext_handle) == None:
        return render_template("error.html")
    else:
        gallery = registry.getExtension(ext_handle).fetchGallery(id)
        state = db_service.getState(ext_handle, id)

        return render_template("gallery.html", gallery=gallery, ext_handle=ext_handle, id=id, state=state)


@app.get("/@<ext_handle>/v/<id>")
def viewer(ext_handle: str, id: str):
    chapter = request.args.get("chapter")

    if registry.getExtension(ext_handle) == None:
        return render_template("error.html")
    else:
        ext = registry.getExtension(ext_handle)
        image_url = "/@{}/i/{}?chapter={}".format(ext_handle, id, chapter)
        return render_template("viewer.html", extension=ext, image_url=image_url)


@app.get("/@<ext_handle>/i/<id>")
def images(ext_handle: str, id: str):
    chapter = request.args.get("chapter")

    if registry.getExtension(ext_handle) == None:
        return render_template("error.html")
    else:
        ext = registry.getExtension(ext_handle)
        return ext.fetchImages(id, chapter)


@app.get("/@<ext_handle>/home")
def home(ext_handle: str):
    if registry.getExtension(ext_handle) == None:
        return render_template("error.html")
    else:
        ext = registry.getExtension(ext_handle)
        return render_template("home.html", quick_filters=ext.quick_filters, handle=ext.handle)


@app.get("/@<ext_handle>/filter/<id>")
def filter(ext_handle: str, id: str):
    if registry.getExtension(ext_handle) == None:
        return render_template("error.html")
    else:
        ext = registry.getExtension(ext_handle)
        filter = ext.quick_filters.get(id)
        if filter == None:
            return render_template("error.html")

        galleries = filter.callback()
        return render_template("content.html", galleries=galleries, handle=ext_handle)


@app.route("/ext/@<ext_handle>")
def extension(ext_handle):
    if registry.getExtension(ext_handle) == None:
        return render_template("error.html")
    else:
        return ext_handle


@app.route("/")
def index():
    return render_template("index.html", extensions=registry.getExtensions())


@app.route("/img/proxy")
def image_proxy():
    # make request

    url = request.args.get("url")
    ext_handle = request.args.get("ext_handle")
    extension = registry.getExtension(ext_handle)
    res = proxy_session.get(url=url, headers=extension.image_proxy_headers)
    response = make_response(res.content)
    response.headers["Cache-Control"] = "max-age=604800"
    return response


@app.get("/ac")
def admin_console():
    return render_template("admin.html")


@app.post("/@<ext_handle>/<id>/bookmark")
def bookmark(ext_handle: str, id: str):
    if registry.getExtension(ext_handle) is None:
        return render_template("error.html")
    else:
        state = db_service.getState(ext_handle, id)
        db_service.setBookmark(
            ext_handle, id, (not state["bookmarked"]))
        return render_template("components/icon_button.html", state=not state["bookmarked"], icon="bookmark")


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
