drop table if exists entries;
create table entries(
  id integer primary key autoincrement,
  title text not null,
  'text' text not NULL
);

drop table if exists resource;
create table resource(
  id integer primary key autoincrement,
  'json' varchar not null
);