DROP TABLE IF EXISTS department CASCADE;
DROP TABLE IF EXISTS employee CASCADE;
DROP TABLE IF EXISTS supervisor CASCADE;
DROP TABLE IF EXISTS contact_info CASCADE;
DROP TABLE IF EXISTS contact_info_type CASCADE;
DROP TABLE IF EXISTS event_type CASCADE;
DROP TABLE IF EXISTS reimbursement_request CASCADE;
DROP TABLE IF EXISTS approval_type CASCADE;
DROP TABLE IF EXISTS approval CASCADE;

CREATE TABLE "department" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "employee" (
  "id" SERIAL PRIMARY KEY,
  "first_name" varchar,
  "last_name" varchar,
  "dept_id" int,
  "username" varchar UNIQUE,
  "password" varchar,
  "is_dept_head" boolean,
  "is_benco" boolean
);

CREATE TABLE "supervisor" (
  "supervisor_id" int,
  "subordinate_id" int,
  PRIMARY KEY ("supervisor_id", "subordinate_id")
);

CREATE TABLE "contact_info" (
  "id" SERIAL PRIMARY KEY,
  "contact_info" varchar,
  "type_id" int,
  "employee_id" int
);

CREATE TABLE "contact_info_type" (
  "id" SERIAL PRIMARY KEY,
  "info_type" varchar
);

CREATE TABLE "event_type" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar,
  "coverage" decimal
);

CREATE TABLE "reimbursement_request" (
  "id" SERIAL PRIMARY KEY,
  "employee_id" INT,
  "event_start_date" BIGINT,
  "event_end_date" BIGINT,
  "street" varchar,
  "city" varchar,
  "state" varchar,
  "zip" varchar,
  "event_name" varchar,
  "event_description" varchar,
  "event_cost" decimal,
  "event_type_id" int,
  "missed_work_start" BIGINT,
  "missed_work_end" BIGINT,
  "grade_type" varchar,
  "justification" varchar,
  "amount" decimal
);

CREATE TABLE "approval_type" (
  "id" SERIAL PRIMARY KEY,
  "appr_type" varchar
);

CREATE TABLE "approval" (
  "id" SERIAL PRIMARY KEY,
  "appr_type" int,
  "req_id" int,
  "approved" boolean,
  "approver_id" int,
  "reason" varchar NOT NULL
);

CREATE INDEX "sup_sub" ON "supervisor" ("supervisor_id", "subordinate_id");

ALTER TABLE "employee" ADD FOREIGN KEY ("dept_id") REFERENCES "department" ("id");

ALTER TABLE "supervisor" ADD FOREIGN KEY ("supervisor_id") REFERENCES "employee" ("id");

ALTER TABLE "supervisor" ADD FOREIGN KEY ("subordinate_id") REFERENCES "employee" ("id");

ALTER TABLE "contact_info" ADD FOREIGN KEY ("type_id") REFERENCES "contact_info_type" ("id");

ALTER TABLE "contact_info" ADD FOREIGN KEY ("employee_id") REFERENCES "employee" ("id");

ALTER TABLE "reimbursement_request" ADD FOREIGN KEY ("employee_id") REFERENCES "employee" ("id");

ALTER TABLE "reimbursement_request" ADD FOREIGN KEY ("event_type_id") REFERENCES "event_type" ("id");

ALTER TABLE "approval" ADD FOREIGN KEY ("req_id") REFERENCES "reimbursement_request" ("id");

ALTER TABLE "approval" ADD FOREIGN KEY ("appr_type") REFERENCES "approval_type" ("id");

INSERT INTO contact_info_type VALUES 
(DEFAULT, 'Work Phone'),
(DEFAULT, 'Work Email'),
(DEFAULT, 'Fax');

INSERT INTO department VALUES
(DEFAULT, 'Web Site Development'),
(DEFAULT, 'Human Resources');

INSERT INTO employee VALUES 
(DEFAULT, 'Alexander', 'Ottosson', 1, 'aottosson', 'password', TRUE, FALSE),
(DEFAULT, 'Benni', 'Fittz', 2, 'bfittz', 'password', TRUE, TRUE),
(DEFAULT, 'John', 'Doe', 1, 'jodoe', 'password', FALSE, FALSE),
(DEFAULT, 'Jane', 'Doe', 1, 'jadoe', 'password', FALSE, FALSE),
(DEFAULT, 'Tavish', 'DeGroot', 1, 'tdgroot', 'password', FALSE, FALSE);

INSERT INTO contact_info VALUES
(DEFAULT, 'aottosson@workplace.org', 2, 1),
(DEFAULT, 'bfittz@workplace.org', 2, 2),
(DEFAULT, '555-555-5555', 1, 2),
(DEFAULT, 'jodoe@workplace.org', 2, 3),
(DEFAULT, 'jadoe@workplace.org', 2, 4),
(DEFAULT, 'tdgroot@workplace.org', 2, 5),
(DEFAULT, '666-666-6666', 3, 5);

INSERT INTO supervisor VALUES
(1, 3),
(3, 4),
(3, 5);

INSERT INTO event_type VALUES
(DEFAULT, 'University Course', 0.8),
(DEFAULT, 'Seminar', 0.6),
(DEFAULT, 'Certification Preperation Class', 0.75),
(DEFAULT, 'Certification', 1),
(DEFAULT, 'Technical Training', 0.9),
(DEFAULT, 'Other', 0.3);

INSERT INTO reimbursement_request VALUES
(
	DEFAULT,
	3,
	1652313600000,
	1652313600000,
	'2222, Strt CC',
	'NormalCity',
	'FL',
	'55555',
	'CSS Grid and You',
	'A Seminar if innovative ways of using CSS grid for UI design',
	100,
	2,
	1652313600000,
	1652313600000,
	'Presentation',
	'I think it is good to keep up with current web design trends',
	60.00
);

INSERT INTO reimbursement_request VALUES
(
	DEFAULT,
	4,
	1652659200000,
	1652659200000,
	'2222, Strt CC',
	'NormalCity',
	'FL',
	'55555',
	'CSS Grid and You',
	'A Seminar if innovative ways of using CSS grid for UI design',
	100.00,
	2,
	1652659200000,
	1652659200000,
	'Presentation',
	'I think it is good to keep up with current web design trends',
	60.00
);

INSERT INTO reimbursement_request VALUES
(
	DEFAULT,
	5,
	1653868800000,
	1653955199000,
	'2222, Strt CC',
	'NormalCity',
	'FL',
	'55555',
	'CSS Grid and You',
	'A Seminar if innovative ways of using CSS grid for UI design',
	100.00,
	2,
	1653868800000,
	1653955199000,
	'Presentation',
	'I think it is good to keep up with current web design trends',
	60.00
);

INSERT INTO approval_type VALUES
(DEFAULT, 'Supervisor Approval'),
(DEFAULT, 'Department Head Approval'),
(DEFAULT, 'Benefits Coordinator Approval');

INSERT INTO approval VALUES
(DEFAULT, 1, 2, TRUE, 3, ''),
(DEFAULT, 2, 2, TRUE, 1, ''),
(DEFAULT, 3, 2, TRUE, 2, '');
