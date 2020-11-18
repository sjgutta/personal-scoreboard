CREATE TABLE team (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    espn_id INT UNSIGNED NOT NULL,
    sport_type VARCHAR(64) NOT NULL,
    full_name VARCHAR(64) NOT NULL,
    abbreviation VARCHAR(64) NOT NULL,
    logo_url VARCHAR(255) NOT NULL,
    UNIQUE KEY (`espn_id`, `sport_type`)
);