from flask import render_template, url_for, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from appmain import db
from appmain.post.forms import PostForm, DeletePostForm
from appmain.post.models import Post

post = Blueprint('post', __name__)

@post.route("/post/new", methods=['GET', 'POST'])
@login_required
def newPost():
        form = PostForm()
        if form.validate_on_submit():
                content = Post(title = form.title.data, content = form.content.data, author = current_user.username)
                db.session.add(content)
                db.session.commit()
                print('A new post is created: ', form.title.data)
                return redirect(url_for('main.home'))
        return render_template('create_post.html', title='New Post', form=form)

@post.route("/post/<int:postId>")
def displayPost(postId):
        content = Post.query.get_or_404(postId)
        return render_template('post.html', title = content.title, post = content)

@post.route("/post/<int:postId>/update", methods=['GET', 'POST'])
@login_required
def updatePost(postId):
        content = Post.query.get_or_404(postId)
        if content.author != current_user.username:
                abort(403)
        form = PostForm()
        if form.validate_on_submit():
                content.title = form.title.data
                content.content = form.content.data
                db.session.commit()
                print("A post is updated: ", content.title)
                return redirect(url_for('main.home'))
        elif request.method == 'GET':
                form.title.data = content.title
                form.content.data = content.content
        return render_template('create_post.html', title='Update Post', form=form)

@post.route("/post/<int:postId>/delete", methods=['GET', 'POST'])
@login_required
def deletePost(postId):
        content = Post.query.get_or_404(postId)
        form = DeletePostForm()
        if content.author != current_user.username:
                abort(403)
        if form.validate_on_submit():
                # db.session.delete(content)
                # db.session.commit()
                print('Post deleted successfully: ', content.title)
                return redirect(url_for('main.home'))
        elif request.method == 'GET':
                return render_template('delete_post.html', title='Confirm Post Deletion', post=content, form=form)