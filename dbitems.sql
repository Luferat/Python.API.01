DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS owner;

CREATE TABLE owner (
    owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    owner_name TEXT,
    owner_email TEXT,
    owner_password TEXT,
    owner_status TEXT DEFAULT 'on'
);

CREATE TABLE item (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    item_name TEXT,
    item_description TEXT,
    item_location TEXT,
    item_owner INTEGER,
    item_status TEXT DEFAULT 'on',
    FOREIGN KEY (item_owner) REFERENCES owner(owner_id)
);

INSERT INTO owner VALUES
('1', '2023-09-14 12:13:14', 'Joca da Silva', 'joca@silva.com', '123', 'on'),
('2', '2023-10-22 21:31:41', 'Setembrino Trocatapas', 'set@brino.com', '123', 'on');

INSERT INTO item VALUES
('1', '2023-09-14 12:31:22', 'Coisa', 'Apenas uma coisa', 'Sob a escada', '1', 'on'),
('2', '2023-10-19 21:22:23', 'Treco', 'Apenas um treco', 'Na caixa azul', '1', 'on'),
('3', '2023-10-23 17:118:!9', 'Bagulho', 'Apenas um bagulho', 'Na mesa de jantar', '2', 'on');