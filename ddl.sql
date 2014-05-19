DROP TABLE aep_sprint;
DROP TABLE aep_user_project;
DROP TABLE aep_session;
DROP TABLE aep_project;
DROP TABLE aep_customer;
DROP TABLE aep_user;
DROP TABLE aep_profile;
--
--
--
CREATE TABLE aep_profile(id serial primary key, name varchar(30));
CREATE TABLE aep_customer(id serial primary key, name varchar(60), country varchar(30), operation_area varchar(60));
CREATE TABLE aep_user(id serial primary key, name varchar(30), username varchar(30), password varchar(32), email varchar(100), id_profile integer);
ALTER TABLE aep_user add constraint fk_user_profile foreign key (id_profile) references aep_profile (id);
CREATE TABLE aep_session(id serial primary key, username varchar(30), login_date date);
CREATE TABLE aep_project(id serial primary key, name varchar(60), id_customer integer);
ALTER TABLE aep_project add constraint fk_project_customer foreign key (id_customer) references aep_customer (id);
CREATE TABLE aep_user_project(id serial primary key, id_user integer, id_project integer);
ALTER TABLE aep_user_project add constraint fk_user_project_user foreign key (id_user) references aep_user (id);
ALTER TABLE aep_user_project add constraint fk_user_project_project foreign key (id_project) references aep_project (id);
CREATE TABLE aep_sprint(id serial primary key, id_project integer, start_date date, end_date date, points_estimated integer, points_delivered integer, number_of_tests integer, date_scanned date, id_user integer);
ALTER TABLE aep_sprint add constraint fk_sprint_project foreign key (id_project) references aep_project (id);
ALTER TABLE aep_sprint add constraint fk_sprint_user foreign key (id_user) references aep_user (id);
--
--
--
INSERT INTO aep_profile (name) values ('Team');
INSERT INTO aep_profile (name) values ('Admin');
INSERT INTO aep_user (name, username, password, id_profile) values ('Marcelo Cure', 'mcure', 't00thbrush', 1);
INSERT INTO aep_user (name, username, password, id_profile) values ('Administrator', 'admin', 't00thbrush', 2);