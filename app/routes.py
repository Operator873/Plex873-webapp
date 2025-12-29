import requests
from flask import Blueprint, render_template, jsonify, current_app # <--- Add current_app
from app.models import Movie

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    movies = Movie.query\
        .filter(Movie.owner.like('%Operator873%'))\
        .order_by(Movie.title)\
        .all()
    return render_template('index.html', movies=movies)

@bp.route('/details/<int:tmdbid>')
def movie_details(tmdbid):
    api_key = current_app.config.get('TMDB_API_KEY') 

    if not api_key:
        return jsonify({'error': 'Server configuration error: TMDB API Key missing'}), 500

    url = f"https://api.themoviedb.org/3/movie/{tmdbid}?api_key={api_key}&language=en-US"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'TMDB Error'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500