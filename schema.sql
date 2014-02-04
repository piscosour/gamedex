drop table if exists games;
create table games (
	id integer primary key autoincrement,
	title string not null,
	developer string,
	publisher string,
	release_date string,
	platforms string,
	technologies string,
	genre string,
	dev_time string,
	distribution string,
	game_category string,
	url string
);
drop table if exists orgs;
create table orgs (
	id integer primary key autoincrement,
	name string not null,
	start_date string,
	end_date string,
	size integer,
	location string,
	url string,
	email string,
	status string
);
drop table if exists notes;
create table notes (
	id integer primary key autoincrement,
	title string,
	body string not null,
	tstamp string,
	private bit not null,
	ref_type integer not null,
	ref_id integer not null
);
drop table if exists events;
create table events (
	id integer primary key autoincrement,
	title string,
	body string not null,
	event_date string,
	category string,
	private bit not null,
	ref_type integer not null,
	ref_id integer not null
);