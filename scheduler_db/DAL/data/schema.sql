DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS actions;
DROP TABLE IF EXISTS tasks;

CREATE TABLE occurrences (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  details TEXT,
  due_time TIMESTAMP
);

CREATE TABLE actions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  location TEXT,
  args TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  occurrence_id INTEGER NOT NULL,
  action_id INTEGER NOT NULL,
  distinction TEXT NOT NULL DEFAULT '(0d)(0h)(0m)(0s)',
  due_time TIMESTAMP NOT NULL,
  status TEXT CHECK( status IN ('PENDING','DONE') )   NOT NULL DEFAULT 'PENDING',
  task_args TEXT NOT NULL DEFAULT '{}',
  FOREIGN KEY (occurrence_id) REFERENCES occurrences (id),
  FOREIGN KEY (action_id) REFERENCES actions (id)
);
