DROP TABLE IF EXISTS questions;

CREATE TABLE questions(
    /* Problem Number */
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    /* solved, unsolved, stuck, marked */
    status TEXT NOT NULL
)
