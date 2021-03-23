DROP TABLE IF EXISTS Coordinates;
DROP TABLE IF EXISTS User;
Create Table Coordinates (
	x1 VARCHAR(100),
    y1 VARCHAR(100),
    x2 VARCHAR(100),
    y2 VARCHAR(100),
    id INT NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

Create Table User (
	id INT NOT NULL,
    PRIMARY KEY (id)
);