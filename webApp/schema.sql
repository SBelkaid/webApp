drop table if exists Entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  price float not null,
  'text' text not null
);

drop table if exists User;
create table user (
  id integer primary key autoincrement,
  username text not null,
  password text not null
);

drop table if exists Role;
create table role (
  id integer primary key autoincrement,
  username text not null,
  role text not null
);