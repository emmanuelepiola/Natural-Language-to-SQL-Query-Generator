CREATE DATABASE IF NOT EXISTS database;
USE database;

CREATE TABLE IF NOT EXISTS movies (
    titolo VARCHAR(255),
    regista VARCHAR(255),
    eta_autore INT,
    anno INT,
    genere VARCHAR(100),
    piattaforma_1 VARCHAR(100),
    piattaforma_2 VARCHAR(100)
);

INSERT INTO movies (titolo, regista, eta_autore, anno, genere, piattaforma_1, piattaforma_2) VALUES
('Inception', 'Christopher Nolan', 54, 2010, 'Fantascienza', 'Amazon Prime Video', 'NOW'),
('Parasite', 'Bong Joon-ho', 55, 2019, 'Dramma', 'Netflix', NULL),
('Interstellar', 'Christopher Nolan', 54, 2014, 'Fantascienza', 'Paramount+', 'Amazon Prime Video'),
('The Dark Knight', 'Christopher Nolan', 54, 2008, 'Azione', 'Netflix', NULL),
('Fight Club', 'David Fincher', 62, 1999, 'Dramma', NULL, NULL),
('Seven', 'David Fincher', 62, 1995, 'Crime', 'Netflix', NULL),
('Gladiator', 'Ridley Scott', 87, 2000, 'Azione', 'Netflix', 'Paramount+'),
('Shutter Island', 'Martin Scorsese', 82, 2010, 'Thriller', 'Netflix', 'Paramount+'),
('Star Wars: A New Hope', 'George Lucas', 80, 1977, 'Fantascienza', 'Disney+', NULL),
('Pulp Fiction', 'Quentin Tarantino', 62, 1994, 'Crime', 'NOW', 'Paramount+'),
('The Shawshank Redemption', 'Frank Darabont', 66, 1994, 'Dramma', 'NOW', NULL),
('Forrest Gump', 'Robert Zemeckis', 72, 1994, 'Dramma', 'Netflix', 'Paramount+'),
('The Godfather', 'Francis Ford Coppola', 86, 1972, 'Crime', 'Paramount+', 'Netflix'),
('The Matrix', 'Lana Wachowski', 59, 1999, 'Fantascienza', 'Netflix', 'Amazon Prime Video'),
('Goodfellas', 'Martin Scorsese', 82, 1990, 'Crime', 'Netflix', 'NOW'),
('Spirited Away', 'Hayao Miyazaki', 84, 2001, 'Animazione', 'Netflix', NULL),
('Saving Private Ryan', 'Steven Spielberg', 78, 1998, 'Guerra', 'Paramount+', 'NOW'),
('Back to the Future', 'Robert Zemeckis', 72, 1985, 'Fantascienza', 'Netflix', 'Amazon Prime Video'),
('The Lord of the Rings: The Fellowship of the Ring', 'Peter Jackson', 63, 2001, 'Fantasy', 'Amazon Prime Video', 'NOW'),
('The Lord of the Rings: The Return of the King', 'Peter Jackson', 63, 2003, 'Fantasy', 'Amazon Prime Video', 'NOW'),
('Schindler''s List', 'Steven Spielberg', 78, 1993, 'Dramma', 'Amazon Prime Video', 'NOW'),
('Inglourious Basterds', 'Quentin Tarantino', 62, 2009, 'Guerra', 'Amazon Prime Video', 'Netflix'),
('Whiplash', 'Damien Chazelle', 40, 2014, 'Dramma', 'Netflix', NULL),
('Joker', 'Todd Phillips', 54, 2019, 'Dramma', 'Netflix', 'Amazon Prime Video'),
('Mad Max: Fury Road', 'George Miller', 80, 2015, 'Azione', 'Netflix', 'NOW'),
('Blade Runner 2049', 'Denis Villeneuve', 57, 2017, 'Fantascienza', 'Netflix', NULL),
('Arrival', 'Denis Villeneuve', 57, 2016, 'Fantascienza', 'Netflix', 'Paramount+'),
('Django Unchained', 'Quentin Tarantino', 62, 2012, 'Western', 'Netflix', NULL),
('The Wolf of Wall Street', 'Martin Scorsese', 82, 2013, 'Biografico', 'Netflix', 'Amazon Prime Video'),
('Once Upon a Time in Hollywood', 'Quentin Tarantino', 62, 2019, 'Commedia', 'Netflix', NULL);
