#!/bin/bash
set -e
echo "~~~~~~~ RUNNING CUSTOM DB INIT SCRIPT!!! ~~~~~~~~"
psql -v ON_ERROR_STOP=1 --username postgres --dbname psql <<-EOSQL
  BEGIN;
  CREATE TABLE hello_table (
      hello_column VARCHAR(255)
  );
  INSERT INTO hello_table(hello_column) VALUES ('Database is reachable and responsive!');
  COMMIT;
EOSQL
