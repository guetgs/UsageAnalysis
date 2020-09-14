## Database
### Structure
The database (called zahler) consists of two tables. The first table is called zahler and contains all observed utility meters with properties zahler_id (primary key), zahler_nummer (meter number), zahler_name (name). The second table is called readings and contains all readings with properties reading_id (primary key), zahler_id (foreign key), date (day of reading) and entry (meter count). 

### Requirements
The database is implemented using a MariaDB Community Server on localhost with a user "python" that has at least SELECT privileges. In order to connect to the analysis framework, the MariaDB Connector/Python is required.
