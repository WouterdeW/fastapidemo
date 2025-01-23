CREATE SCHEMA IF NOT EXISTS demo;

CREATE TYPE user_type AS ENUM ('teacher', 'student');

CREATE TABLE IF NOT EXISTS demo.contacts(
    id              INTEGER     NOT NULL GENERATED ALWAYS AS IDENTITY
,   first_name      TEXT        NOT NULL
,   last_name       TEXT        NOT NULL
,   email           TEXT        UNIQUE
,   user_type       user_type
,   CONSTRAINT      pk_contacts PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS demo.teachers(
    id              INTEGER     NOT NULL
,   subject         TEXT
,   CONSTRAINT      pk_teachers PRIMARY KEY (id)
,   CONSTRAINT      fk_teachers FOREIGN KEY (id) REFERENCES demo.contacts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS demo.students(
    id              INTEGER     NOT NULL
,   curriculum      TEXT
,   enrollment_year INTEGER
,   CONSTRAINT      pk_students PRIMARY KEY (id)
,   CONSTRAINT      fk_students FOREIGN KEY (id) REFERENCES demo.contacts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS demo.courses(
    id              INTEGER     NOT NULL GENERATED ALWAYS AS IDENTITY
,   name            TEXT        NOT NULL
,   subject         TEXT
,   start_date      DATE
,   CONSTRAINT      pk_courses PRIMARY KEY  (id)
);

CREATE TABLE IF NOT EXISTS demo.course_registrations(
    id                  INTEGER     NOT NULL GENERATED ALWAYS AS IDENTITY
,   course_id           INTEGER     NOT NULL
,   contact_id          INTEGER     NOT NULL
,   registration_date   DATE        NOT NULL DEFAULT CURRENT_DATE
,   CONSTRAINT          pk_course_registraions PRIMARY KEY (id)
,   CONSTRAINT          fk_course_registrations_courses FOREIGN KEY (course_id) REFERENCES demo.courses(id) ON DELETE CASCADE
,   CONSTRAINT          fk_course_registrations_contacts FOREIGN KEY (contact_id) REFERENCES demo.contacts(id) ON DELETE CASCADE
,   UNIQUE(course_id, contact_id)
);
