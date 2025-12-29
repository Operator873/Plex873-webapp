-- 1. Create the Parent Table (movies)
CREATE TABLE IF NOT EXISTS movies (
    tmdbid INT NOT NULL,
    title VARCHAR(255),
    year INT,
    owner VARCHAR(255),
    PRIMARY KEY (tmdbid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Create the Child Table (movie_metadata)
-- Includes a foreign key constraint to ensure metadata cannot exist without a parent movie.
-- ON DELETE CASCADE ensures if you delete a movie, its cached metadata is also removed.
CREATE TABLE IF NOT EXISTS movie_metadata (
    tmdbid INT NOT NULL,
    poster_path VARCHAR(255),
    backdrop_path VARCHAR(255),
    overview TEXT,
    vote_average FLOAT,
    release_date DATE,
    PRIMARY KEY (tmdbid),
    CONSTRAINT fk_movie_metadata_movies 
        FOREIGN KEY (tmdbid) 
        REFERENCES movies (tmdbid) 
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;