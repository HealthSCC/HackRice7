drop table if exists patient;
drop table if exists event;
drop table if exists doctor;
create table patient (
  pid integer primary key not null,
  useremail varchar not null,
  password varchar(20) not null,
  firstname varchar(20),
  lastname varchar(20)
);

create table doctor(
  did integer primary key not null,
  firstname varchar(20) not null,
  lastname varchar(20) not null
);

create table event(
  pid integer not null,
  did integer,
  startdate date not null,
  enddate date not null,
  category varchar(10) not null,
  time time not null,
  description text,
  foreign key(pid) REFERENCES patient(pid),
  foreign key(did) REFERENCES doctor(did)
);

