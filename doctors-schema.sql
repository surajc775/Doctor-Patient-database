drop database if exists doctors;
create database doctors;
use doctors;

create table doctor (
	doctor_id int NOT NULL primary key auto_increment,
	first_name varchar(64) not null unique,
	last_name varchar(64) not null unique,
	specialty varchar(64)
);

create table patient (
	patient_id int NOT NULL primary key auto_increment,
	first_name varchar(64) not null unique,
	last_name varchar(64) not null unique,
	doctor_id int,
	
	foreign key (doctor_id) references doctor(doctor_id)
		on update cascade
		on delete cascade
);

create table visit (
	doctor_id int,
	patient_id int,
	visit_date Date,

	primary key (doctor_id, patient_id, visit_date),
	foreign key (patient_id) references patient(patient_id)
		on update cascade
		on delete cascade,
	foreign key (doctor_id) references doctor(doctor_id)
		on update cascade
		on delete cascade
);
