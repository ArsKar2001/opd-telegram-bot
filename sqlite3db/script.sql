create table curator
(
    id       integer not null
        constraint curator_pk
            primary key autoincrement,
    name     text    not null,
    link_sdo text
);

create unique index curator_id_uindex
    on curator (id);

create table faculty
(
    id   integer not null
        constraint faculty_pk
            primary key autoincrement,
    name text    not null
);

create unique index faculty_id_uindex
    on faculty (id);

create unique index faculty_name_uindex
    on faculty (name);

create table "group"
(
    id         integer not null
        constraint group_pk
            primary key autoincrement,
    name       text    not null,
    faculty_id integer not null
        references faculty
);

create unique index group_id_uindex
    on "group" (id);

create unique index group_name_uindex
    on "group" (name);

create table student
(
    id        integer not null
        constraint student_pk
            primary key autoincrement,
    group_id  integer not null
        references "group",
    full_name text    not null
);

create unique index student_id_uindex
    on student (id);

create table user
(
    id       integer not null
        constraint user_pk
            primary key autoincrement,
    chat_id  integer not null,
    group_id integer
        references "group"
);

create unique index user_chat_id_uindex
    on user (chat_id);

create unique index user_id_uindex
    on user (id);


