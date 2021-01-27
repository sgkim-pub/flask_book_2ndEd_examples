from flask import render_template, Blueprint, request
from appmain.post.models import Post

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
        page = request.args.get('page', 1, type=int)
        # posts = Post.query.order_by().paginate(page=page, per_page=3)
        posts = Post.query.order_by(Post.datePosted.desc()).paginate(page = page, per_page = 3)
        return render_template("home.html", posts=posts)

@main.route("/about")
def about():
        return render_template("about.html", title='About')
