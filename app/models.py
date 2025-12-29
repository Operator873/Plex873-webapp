from app import db


class Movie(db.Model):
    __tablename__ = "movies"

    tmdbid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    year = db.Column(db.Integer)
    owner = db.Column(db.String(255))

    # 'uselist=False' makes it a 1-to-1 relationship
    metadata_cache = db.relationship(
        "MovieMetadata", backref="movie", uselist=False, lazy="joined"
    )


class MovieMetadata(db.Model):
    __tablename__ = "movie_metadata"
    tmdbid = db.Column(db.Integer, db.ForeignKey("movies.tmdbid"), primary_key=True)
    poster_path = db.Column(db.String(255))
    backdrop_path = db.Column(db.String(255))
    overview = db.Column(db.Text)
    vote_average = db.Column(db.Float)
    release_date = db.Column(db.Date)

    @property
    def poster_url(self):
        """Helper to return full TMDB URL"""
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return "https://via.placeholder.com/500x750?text=No+Poster"
