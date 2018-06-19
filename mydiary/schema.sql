DROP TABLE IF EXISTS mytasks;
DROP TABLE IF EXISTS mystatus;

CREATE TABLE mystatus(
    skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    /* algo, mldl, dtbs, syst, corresponds to stdy directions */
    skill TEXT UNIQUE NOT NULL,
    /* initially zero for all skills */
    level INTEGER NOT NULL,
    /* points in the current level */
    points INTEGER NOT NULL
);

CREATE TABLE mytasks(
    /*  Everything should have a id */
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    /* stdy, work, side, pers */
    category TEXT NOT NULL,
    /* algo, mldl, dtbs, syst */
    direction TEXT NOT NULL,
    /* leetcode, other contest name */
    taskname TEXT NOT NULL,
    /* register time */
    t_register TEXT NOT NULL,
    /* end time */
    t_complete TEXT NOT NULL,
    /* deadline */
    deadline TEXT NOT NULL,
    /* task description */
    description TEXT NOT NULL,
    /* number of steps */
    num_steps INTEGER NOT NULL,
    /* finished steps */
    fin_steps INTEGER NOT NULL,
    /* reward points */
    rewards INTEGER NOT NULL
);
