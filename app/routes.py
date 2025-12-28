from flask import Blueprint, render_template
from app.models import Movie

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # Fetch only movies owned by Operator873, joined with metadata
    # The 'joined' lazy loading in models.py handles the join automatically
    movies = Movie.query\
        .filter(Movie.owner.like('%Operator873%'))\
        .order_by(Movie.title)\
        .all()
        
    return render_template('index.html', movies=movies)
