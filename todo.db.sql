BEGIN TRANSACTION;
DROP TABLE IF EXISTS "history";
CREATE TABLE IF NOT EXISTS "history" (
	"id"	INTEGER,
	"task_id"	INTEGER NOT NULL,
	"entry_date"	TEXT,
	"ledger"	TEXT,
	PRIMARY KEY("id")
);
DROP TABLE IF EXISTS "todo";
CREATE TABLE IF NOT EXISTS "todo" (
	"id"	INTEGER,
	"task"	char(100) NOT NULL,
	"status"	bool NOT NULL,
	"project"	TEXT,
	"tag"	TEXT,
	"state"	TEXT,
	"date_due"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "projects";
CREATE TABLE IF NOT EXISTS "projects" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT,
	"comment"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "notes";
CREATE TABLE IF NOT EXISTS "notes" (
	"id"	INTEGER,
	"task_id"	INTEGER NOT NULL,
	"entry_date"	TEXT,
	"ledger"	TEXT,
	PRIMARY KEY("id")
);
DROP TABLE IF EXISTS "states";
CREATE TABLE IF NOT EXISTS "states" (
	"id"	INTEGER,
	"name"	TEXT,
	"color"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "attach";
CREATE TABLE IF NOT EXISTS "attach" (
	"id"	INTEGER NOT NULL UNIQUE,
	"task_id"	INTEGER NOT NULL,
	"entry_date"	TEXT NOT NULL,
	"filename"	TEXT NOT NULL,
	"description"	TEXT,
	"filesize"	INTEGER NOT NULL,
	"filetype"	TEXT NOT NULL,
	"isoname"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
COMMIT;
