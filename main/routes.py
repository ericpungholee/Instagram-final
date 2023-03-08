from flask import render_template, request, Blueprint
from instagram.models import Post
from instagram.posts.forms import CommentForm
from instagram.users.forms import SearchForm

main = Blueprint('main', __name__)

@main.route("/")
@main.route('/home', methods=['POST', 'GET'])
def home():
    comment = CommentForm()
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, comment=comment, form=form)

@main.route("/about")
def about():
    form = SearchForm()
    return render_template('about.html', title='About', form=form)