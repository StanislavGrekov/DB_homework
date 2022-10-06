
SELECT album_name, date_release FROM album
where date_release = '2018-01-01';

SELECT track_name, track_duration FROM track
WHERE track_duration = (SELECT MAX(track_duration) FROM track);

SELECT track_name, track_duration FROM track
WHERE track_duration >= '3.5';

SELECT collection_name, release_date FROM collection
WHERE release_date >='2018-01-01' AND release_date <='2020-01-01';

SELECT musician_name from musician
WHERE musician_name LIKE '% ';

SELECT track_name FROM track
WHERE track_name LIKE 'My%';



