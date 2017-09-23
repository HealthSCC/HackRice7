drop table if exists entries;
drop table if exists patient;
create table patient (
  id integer primary key not null,
  useremail varchar not null,
  password varchar(20) not null,
  firstname varchar(20),
  lastname varchar(20)
);