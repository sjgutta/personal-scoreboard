CREATE TABLE favorite (
    id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT(11) UNSIGNED NOT NULL,
    team INT UNSIGNED NOT NULL,
    sport_type VARCHAR(64) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    UNIQUE KEY (`user_id`, `team`, `sport_type`)
);