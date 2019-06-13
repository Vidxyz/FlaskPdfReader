DROP TABLE IF EXISTS PDF;
DROP TABLE IF EXISTS PDFSTATS;

CREATE TABLE PDF (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  filename TEXT UNIQUE NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE PDFSTATS (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pdf_id INTEGER NOT NULL,
  rank INTEGER NOT NULL,
  word TEXT NOT NULL,
  FOREIGN KEY (pdf_id) REFERENCES pdf (id)
);