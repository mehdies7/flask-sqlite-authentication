DROP TABLE IF EXISTS users;

create table users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username text not null,
    password text not null);