CREATE TABLE IF NOT EXISTS music_genre (
id SERIAL PRIMARY KEY,
genre VARCHAR(40) UNIQUE NOT NULL
);
									  
CREATE TABLE IF NOT EXISTS musician ( 
id SERIAL PRIMARY KEY,
musician_name VARCHAR(40) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Album ( 
id SERIAL PRIMARY KEY,
album_name VARCHAR(40) UNIQUE NOT NULL,
date_release date
);

CREATE TABLE IF NOT EXISTS genre_musician ( 
genre_id INTEGER REFERENCES music_genre(id),
musician_id INTEGER REFERENCES musician(id),
CONSTRAINT pk PRIMARY KEY (genre_id,musician_id) -- составной первичный ключ
);

CREATE TABLE IF NOT EXISTS album_musician ( 
album_id INTEGER REFERENCES Album(id),
musician_id INTEGER REFERENCES musician(id),
CONSTRAINT anotherpk PRIMARY KEY (album_id,musician_id)
);

CREATE TABLE if not exists track ( 
id SERIAL PRIMARY KEY,
id_album INTEGER REFERENCES Album(id),
track_name VARCHAR(40) UNIQUE NOT NULL,
track_duration NUMERIC(8,2) CHECK
	(track_duration > 1.0 and track_duration < 10.0)
);

CREATE TABLE IF NOT EXISTS collection ( 
id SERIAL primary key,
collection_name VARCHAR(40) UNIQUE NOT NULL,
release_date DATE CHECK
	(release_date > '1950-01-01' AND release_date < '2030-01-01')
);

CREATE TABLE IF NOT EXISTS collection_track ( 
collection_id INTEGER REFERENCES collection(id),
track_id INTEGER REFERENCES track(id),
CONSTRAINT elsepk PRIMARY KEY (collection_id, track_id) 
);



