from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from instagram import db
from instagram.models import Post, Comment, Like
from instagram.posts.forms import PostForm, CommentForm
from instagram.posts.utils import save_picture_p

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        picture_file = save_picture_p(form.image_file.data)
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id, image_file=picture_file)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post, form=form)

@posts.route('/post/<int:post_id>/update', methods=["POST", "GET"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.image_file = save_picture_p(form.image_file.data)
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
        form.image_file.data = post.image_file
    return render_template("create_post.html", title="Update Post", form=form, legend="Update Post")

@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        abort(403)
    comments = Comment.query.filter_by(post_id=post_id).all()
    likes = Like.query.filter_by(post_id=post.id).all()

    for comment in comments:
        db.session.delete(comment)
    for like in likes:
        db.session.delete(like)

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')

    return redirect(url_for('main.home'))

@posts.route("/create-comment/<post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        post = Post.query.filter_by(id=post_id).first()
        if post:
            comment = Comment(content=form.content.data, user_id=current_user.id, post_id=post_id, user=current_user)
            db.session.add(comment)
            db.session.commit()
            flash('Comment added Successfully.', category='success')
        else:
            flash('Post does not exist.', category='error')
    else:
        flash('Comment cannot be empty.', category='error')
    return redirect(request.referrer)

@posts.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash('comment does not exist.', category='error')
    elif current_user.id != comment.user_id:
        flash('You do not have permission.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
    return redirect(request.referrer)

@posts.route('/like-post/<post_id>', methods=['GET'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if not post:
        flash('Post does not exist.', category='error')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    return redirect(request.referrer)