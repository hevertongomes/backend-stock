set -e

psql -v ON_ERROR_STOP=1 --username "$DB_USER" --dbname "$DB_NAME" <<-EOSQL
    CREATE SCHEMA items;
    CREATE SCHEMA stock;
    DROP SCHEMA public;
EOSQL
