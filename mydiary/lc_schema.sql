DROP TABLE IF EXISTS questions;

CREATE TABLE questions(
    /* Problem Number */
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    /* stdy, work, side, pers */
    status TEXT NOT NULL
)
