drop table if exists entries;
create table User (
  id integer primary key autoincrement,
  username text not null,
  password float not null
);

drop table if exists entries;
create table Role (
  id integer primary key autoincrement,
  username text not null,
  role float not null
);