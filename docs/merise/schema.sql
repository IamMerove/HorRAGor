CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE source (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nom VARCHAR(80) NOT NULL UNIQUE,
    type VARCHAR(20) NOT NULL CHECK (type IN ('api', 'scraping')),
    url_base TEXT
);

CREATE TABLE auteur (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nom VARCHAR(150) NOT NULL,
    nationalite VARCHAR(80),
    biographie TEXT,
    UNIQUE(nom)
);

CREATE TABLE genre (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nom VARCHAR(80) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE tag (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    libelle VARCHAR(80) NOT NULL UNIQUE,
    categorie VARCHAR(50)
);

CREATE TABLE oeuvre (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titre VARCHAR(255) NOT NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('film', 'livre', 'jeu')),
    synopsis TEXT,
    date_sortie DATE,
    note_moyenne NUMERIC(3,1),
    source_id UUID REFERENCES source(id) ON DELETE SET NULL,
    UNIQUE(titre, type)
);

CREATE TABLE oeuvre_auteur (
    oeuvre_id UUID REFERENCES oeuvre(id) ON DELETE CASCADE,
    auteur_id UUID REFERENCES auteur(id) ON DELETE CASCADE,
    PRIMARY KEY (oeuvre_id, auteur_id)
);

CREATE TABLE oeuvre_genre (
    oeuvre_id UUID REFERENCES oeuvre(id) ON DELETE CASCADE,
    genre_id UUID REFERENCES genre(id) ON DELETE CASCADE,
    PRIMARY KEY (oeuvre_id, genre_id)
);

CREATE TABLE oeuvre_tag (
    oeuvre_id UUID REFERENCES oeuvre(id) ON DELETE CASCADE,
    tag_id UUID REFERENCES tag(id) ON DELETE CASCADE,
    PRIMARY KEY (oeuvre_id, tag_id)
);