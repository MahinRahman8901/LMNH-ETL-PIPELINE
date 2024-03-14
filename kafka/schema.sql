DROP DATABASE IF EXISTS museum WITH FORCE;
CREATE DATABASE museum;
\c museum;

CREATE TABLE floor (
    floor_id INT GENERATED ALWAYS AS IDENTITY,
    floor_number VARCHAR(50) NOT NULL,
    PRIMARY KEY (floor_id)
);

CREATE TABLE department (
    department_id INT GENERATED ALWAYS AS IDENTITY,
    dept_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (department_id)
);

CREATE TABLE exhibition (
    exhibition_id INT GENERATED ALWAYS AS IDENTITY,
    exhibition_name VARCHAR(255) UNIQUE NOT NULL,
    exhibition_desc VARCHAR(255) NOT NULL,
    exhibition_code VARCHAR(20) NOT NULL,
    date_started TIMESTAMP NOT NULL,
    floor_id INT,
    department_id INT,
    PRIMARY KEY (exhibition_id),
    FOREIGN KEY (floor_id) REFERENCES floor (floor_id),
    FOREIGN KEY (department_id) REFERENCES department (department_id)
);

CREATE TABLE rating_type (
    rating_type_id INT GENERATED ALWAYS AS IDENTITY,
    rating_integer_value INT NOT NULL,
    rating_desc VARCHAR(255) NOT NULL,
    PRIMARY KEY (rating_type_id)
);

CREATE TABLE rating (
    rating_id INT GENERATED ALWAYS AS IDENTITY,
    rating_value INT NOT NULL,
    rating_timestamp TEXT,
    exhibition_id INT,
    rating_type_id INT,
    PRIMARY KEY (rating_id),
    FOREIGN KEY (exhibition_id) REFERENCES exhibition (exhibition_id),
    FOREIGN KEY (rating_type_id) REFERENCES rating_type (rating_type_id)
);

CREATE TABLE call_assistance (
    call_assistance_id INT GENERATED ALWAYS AS IDENTITY,
    call_assistance_timestamp TIMESTAMP NOT NULL,
    exhibition_id INT,
    PRIMARY KEY (call_assistance_id),
    FOREIGN KEY (exhibition_id) REFERENCES exhibition (exhibition_id)
);

CREATE TABLE call_emergency (
    call_emergency_id INT GENERATED ALWAYS AS IDENTITY,
    call_emergency_timestamp TIMESTAMP NOT NULL,
    exhibition_id INT,
    PRIMARY KEY (call_emergency_id),
    FOREIGN KEY (exhibition_id) REFERENCES exhibition (exhibition_id)
);


--Insert inital data --

INSERT INTO department(dept_name) VALUES
    ('Entomology'),
    ('Geology'),
    ('Paleontology'),
    ('Zoology'),
    ('Ecology'),
    ('test');

INSERT INTO floor(floor_number) VALUES
    ('Vault'),
    ('1'),
    ('2'),
    ('3'),
    ('4');

INSERT INTO rating_type(rating_integer_value, rating_desc) VALUES
    (0, 'Terrible'),
    (1, 'Bad'),
    (2, 'Neutral'),
    (3, 'Good'),
    (4, 'Amazing');

INSERT INTO exhibition (exhibition_code, exhibition_name, exhibition_desc, date_started, department_id, floor_id)
    VALUES
    ('EXH_00','Measureless to Man', 'An immersive 3D experience: delve deep into a previously-inaccessible cave system.', '2021-08-23', 2, 2),
    ('EXH_01','Adaptation','How insect evolution has kept pace with an industrialised world', '2019-07-01',1,1),
    ('EXH_02','The Crenshaw Collection','An exhibition of 18th Century watercolours, mostly focused on South American wildlife.', '2021-03-03',4,3),
    ('EXH_03','Cetacean Sensations','Whales: from ancient myth to critically endangered.','2019-07-01',4,2),
    ('EXH_04','Our Polluted World','A hard-hitting exploration of humanity`s impact on the environment.','2021-05-12',5,4),
    ('EXH_05','Thunder Lizards', 'How new research is making scientists rethink what dinosaurs really looked like.', '2023-02-01',3,2);
