from flask import Flask, render_template, request, redirect
from repo_students import Link, repository
import hashlib
from datetime import datetime

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    short_url = None
    if request.method == "POST":
        url = request.form["url"]
        hash_id = hashlib.md5(url.encode()).hexdigest()[:10]
        link = Link(url=url, hash_id=hash_id, created_at=datetime.now())
        repository.create(link)
        short_url = request.url_root + hash_id
    return render_template("index.html", short_url=short_url)


@app.route("/urls")
def urls():
    all_links = repository.get()
    return render_template("urls.html", links=all_links)


@app.route("/<hash_id>")
def redirect_url(hash_id):
    try:
        link = repository.get(hash_id)
        repository.update(link)
        return redirect(link.url)
    except KeyError:
        return "URL not found", 404


if __name__ == "__main__":
    app.run(debug=True)
