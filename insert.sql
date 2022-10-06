-- ������� musician
INSERT INTO musician(musician_name) 
VALUES ('Metallica ');
INSERT INTO musician(musician_name) 
VALUES ('������ ');
INSERT INTO musician(musician_name) 
VALUES ('���� ��������');
INSERT INTO musician(musician_name) 
VALUES ('���� ');
INSERT INTO musician(musician_name) 
VALUES ('��-2 ');
INSERT INTO musician(musician_name) 
VALUES ('���������� ');
INSERT INTO musician(musician_name) 
VALUES ('Bob Marley');
INSERT INTO musician(musician_name) 
VALUES ('Larry Goldings');

-- ������� music_genre
INSERT INTO music_genre(id, genre) 
VALUES (1,'���');
INSERT INTO music_genre(id, genre) 
VALUES (2,'���-������');
INSERT INTO music_genre(id, genre)
VALUES (3,'������');
INSERT INTO music_genre(id, genre) 
VALUES (4,'�����');
INSERT INTO music_genre(id, genre) 
VALUES (5,'����');

-- ������� genre_musician
INSERT INTO genre_musician
VALUES (1,4);
INSERT INTO genre_musician 
VALUES (1,5);
INSERT INTO genre_musician 
VALUES (1,6);
INSERT INTO genre_musician 
VALUES (2,2);
INSERT INTO genre_musician 
VALUES (2,3);
INSERT INTO genre_musician 
VALUES (3,1);
INSERT INTO genre_musician
VALUES (4,7);
INSERT INTO genre_musician 
VALUES (5,8);

-- ������� album
INSERT INTO album(id, album_name, date_release) 
VALUES (1, 'Load', '1996-01-01');
INSERT INTO album(id, album_name, date_release) 
VALUES (2, '���� �����', '2007-01-01');
INSERT INTO album(id, album_name, date_release) 
VALUES (3, '��� ��� ����', '2007-01-01');
INSERT INTO album(id, album_name, date_release) 
VALUES (4, '��������� �����', '2018-01-01');
INSERT INTO album(id, album_name, date_release) 
VALUES (5, '�������� �������', '2017-01-01');
INSERT INTO album(id, album_name, date_release) 
VALUES (6, '������', '2016-01-01');
INSERT INTO album(id, album_name, date_release) 
VALUES (7, 'Legend', '2019-01-01');
INSERT INTO album(id, album_name, date_release) 
VALUES (8, 'Big Staff', '1996-01-01');

-- ������� track
INSERT INTO track (id, id_album, track_name,track_duration) 
VALUES (1, 1, '2x4', 5.28);
INSERT INTO track (id, id_album, track_name,track_duration) 
VALUES (2, 1, 'Cure', 4.54);
INSERT INTO track (id, id_album, track_name,track_duration) 
VALUES (3, 2, '��� �������', 3.32);
INSERT INTO track (id, id_album, track_name,track_duration) 
VALUES (4, 2, '������', 3.38);
INSERT INTO track (id, id_album, track_name,track_duration) 
VALUES (5, 3, '�������', 3.23);
INSERT INTO track (id, id_album, track_name,track_duration) 
VALUES (6, 3, '� ���� ��������', 6.57);
INSERT INTO track (id, id_album, track_name,track_duration) 
VALUES (7, 4, '����� �� ������', 4.54);
INSERT INTO track (id, id_album, track_name,track_duration) 
VALUES (8, 4, '�����', 6.39);
INSERT INTO track (id, id_album, track_name,track_duration) 
VALUES (9, 5, '������ ������', 5.13);
INSERT INTO track (id, id_album, track_name,track_duration) 
VALUES (10, 6, '�����', 4.02);
INSERT INTO track (id, id_album, track_name,track_duration) 
VALUES (11, 6, '����', 4.34);
INSERT INTO track (id, id_album, track_name,track_duration) 
VALUES (12, 7, 'My love', 3.52);
INSERT INTO track (id, id_album, track_name,track_duration) 
VALUES (13, 7, 'Stir it up', 3.38);
INSERT INTO track (id, id_album, track_name,track_duration) 
VALUES (14, 8, 'Jim jam', 6.46);
INSERT INTO track (id, id_album, track_name,track_duration) 
VALUES (15, 8, 'IdeLupino', 3.32);


--������� Collection
INSERT INTO  collection (id, collection_name, release_date) 
VALUES (1, '����� ���������', '1998-01-02'); 
INSERT INTO  collection (id, collection_name, release_date) 
VALUES (2, '��� ���������', '2001-01-04');
INSERT INTO  collection (id, collection_name, release_date) 
VALUES (3, '��� ������', '2015-03-04');
INSERT INTO  collection (id, collection_name, release_date) 
VALUES (4, '��� ���', '2018-08-25');
INSERT INTO  collection (id, collection_name, release_date) 
VALUES (5, '��� �����������', '2003-11-11');
INSERT INTO  collection (id, collection_name, release_date) 
VALUES (6, '����������', '2019-12-31');
INSERT INTO  collection (id, collection_name, release_date) 
VALUES (7, '�����������', '1967-02-07');
INSERT INTO  collection (id, collection_name, release_date) 
VALUES (8, '�������', '1999-06-22');


--������� Collection_track
INSERT INTO  collection_track  (collection_id,track_id) 
VALUES (1,3);
INSERT INTO  collection_track  (collection_id,track_id) 
VALUES (1,2);
INSERT INTO  collection_track  (collection_id,track_id) 
VALUES (1,6);
INSERT INTO  collection_track  (collection_id,track_id) 
VALUES (1,7);
INSERT INTO  collection_track  (collection_id,track_id) 
VALUES (3,2);
INSERT INTO  collection_track  (collection_id,track_id) 
VALUES (3,1);
INSERT INTO  collection_track  (collection_id,track_id) 
VALUES (4,3);
INSERT INTO  collection_track  (collection_id,track_id) 
VALUES (4,11);
INSERT INTO  collection_track  (collection_id,track_id) 
VALUES (5,6);
INSERT INTO  collection_track  (collection_id,track_id) 
VALUES (6,1);
INSERT INTO  collection_track  (collection_id,track_id) 
VALUES (7,2);
INSERT INTO  collection_track  (collection_id,track_id) 
VALUES (7,3);
INSERT INTO  collection_track  (collection_id,track_id) 
VALUES (7,14);
INSERT INTO  collection_track  (collection_id,track_id) 
VALUES (8,3);
INSERT INTO  collection_track  (collection_id,track_id) 
VALUES (8,2);
INSERT INTO  collection_track  (collection_id,track_id) 
VALUES (8,11);

--������� album_musician
INSERT INTO  album_musician  (album_id, musician_id) 
VALUES (1,1);
INSERT INTO  album_musician  (album_id, musician_id) 
VALUES (2,2);
INSERT INTO  album_musician  (album_id, musician_id) 
VALUES (3,3);
INSERT INTO  album_musician  (album_id, musician_id) 
VALUES (4,4);
INSERT INTO  album_musician  (album_id, musician_id) 
VALUES (5,5);
INSERT INTO  album_musician  (album_id, musician_id) 
VALUES (6,6);
INSERT INTO  album_musician  (album_id, musician_id) 
VALUES (7,7);
INSERT INTO  album_musician  (album_id, musician_id) 
VALUES (8,8);