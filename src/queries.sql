CREATE TABLE IF NOT EXISTS employers
(
    employer_id serial,
    name varchar(255) NOT NULL,
    type varchar(100) NOT NULL,
    area varchar(100) NOT NULL,
    description text,
    employer_url text NOT NULL,
    site_url text,
    open_vacancies int NOT NULL,

    CONSTRAINT pk_employer_employer_id PRIMARY KEY(employer_id)
);

CREATE TABLE IF NOT EXISTS vacancies
(
    vacancy_id serial,
    name varchar(255) NOT NULL,
    employer_id smallint,
    description text,
    area varchar(100) NOT NULL,
    salary_from int NOT NULL,
    salary_to int NOT NULL,
    salary int,
    currency varchar(3) NOT NULL,
    experience varchar (25) NOT NULL,
    employment varchar (50) NOT NULL,
    address text,
    url text NOT NULL,

    CONSTRAINT pk_vacancy_vacancy_id PRIMARY KEY(vacancy_id),
    CONSTRAINT fk_vacancy_employer_id FOREIGN KEY(employer_id) REFERENCES employers(employer_id)
);

