DROP TABLE IF EXISTS reimbursement CASCADE;
DROP TABLE IF EXISTS approval CASCADE;
DROP TABLE IF EXISTS approval_type CASCADE;
DROP TABLE IF EXISTS reimbursement_request CASCADE;
DROP TABLE IF EXISTS justification_type CASCADE;
DROP TABLE IF EXISTS grading_type CASCADE;
DROP TABLE IF EXISTS event_type CASCADE;
DROP TABLE IF EXISTS employee_rank CASCADE;
DROP TABLE IF EXISTS ranks CASCADE;
DROP TABLE IF EXISTS contact_info_type CASCADE;
DROP TABLE IF EXISTS contact_info CASCADE;
DROP TABLE IF EXISTS supervisor CASCADE;
DROP TABLE IF EXISTS department CASCADE;
DROP TABLE IF EXISTS employee CASCADE;

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
  "employee_id" int,
  "event_start_date" int,
  "event_end_date" int,
  "street" varchar,
  "city" varchar,
  "state" varchar,
  "zip" varchar,
  "event_name" varchar,
  "event_description" varchar,
  "event_cost" decimal,
  "event_type_id" int,
  "missed_work_start" int,
  "missed_work_end" int,
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
