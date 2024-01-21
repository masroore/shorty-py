/*
 Navicat Premium Data Transfer

 Source Server         : pg
 Source Server Type    : PostgreSQL
 Source Server Version : 150005 (150005)
 Source Host           : localhost:5432
 Source Catalog        : shorty
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 150005 (150005)
 File Encoding         : 65001

 Date: 21/01/2024 17:13:40
*/


-- ----------------------------
-- Sequence structure for browsers_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."browsers_id_seq";
CREATE SEQUENCE "public"."browsers_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for clicks_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."clicks_id_seq";
CREATE SEQUENCE "public"."clicks_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for links_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."links_id_seq";
CREATE SEQUENCE "public"."links_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for users_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."users_id_seq";
CREATE SEQUENCE "public"."users_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Table structure for browsers
-- ----------------------------
DROP TABLE IF EXISTS "public"."browsers";
CREATE TABLE "public"."browsers" (
  "id" int4 NOT NULL DEFAULT nextval('browsers_id_seq'::regclass),
  "user_agent" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "os" varchar COLLATE "pg_catalog"."default",
  "device" varchar COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Table structure for clicks
-- ----------------------------
DROP TABLE IF EXISTS "public"."clicks";
CREATE TABLE "public"."clicks" (
  "id" int8 NOT NULL DEFAULT nextval('clicks_id_seq'::regclass),
  "link_id" int8 NOT NULL,
  "browser_id" int4,
  "ip_addr" inet,
  "created_on" timestamp(6) NOT NULL DEFAULT (now() AT TIME ZONE 'utc'::text)
)
;

-- ----------------------------
-- Table structure for links
-- ----------------------------
DROP TABLE IF EXISTS "public"."links";
CREATE TABLE "public"."links" (
  "id" int8 NOT NULL DEFAULT nextval('links_id_seq'::regclass),
  "url" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "short_code" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "owner_id" int2,
  "secret_key" varchar COLLATE "pg_catalog"."default",
  "is_protected" bool NOT NULL DEFAULT false,
  "is_custom" bool NOT NULL DEFAULT false,
  "expires_at" timestamp(6),
  "created_at" timestamp(6) NOT NULL DEFAULT (now() AT TIME ZONE 'utc'::text),
  "updated_at" timestamp(6)
)
;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "public"."users";
CREATE TABLE "public"."users" (
  "id" int4 NOT NULL DEFAULT nextval('users_id_seq'::regclass),
  "name" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "email" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "password" varchar COLLATE "pg_catalog"."default",
  "is_active" bool NOT NULL DEFAULT true,
  "created_at" timestamp(6) NOT NULL DEFAULT (now() AT TIME ZONE 'utc'::text),
  "updated_at" timestamp(6)
)
;

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."browsers_id_seq"
OWNED BY "public"."browsers"."id";
SELECT setval('"public"."browsers_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."clicks_id_seq"
OWNED BY "public"."clicks"."id";
SELECT setval('"public"."clicks_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."links_id_seq"
OWNED BY "public"."links"."id";
SELECT setval('"public"."links_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."users_id_seq"
OWNED BY "public"."users"."id";
SELECT setval('"public"."users_id_seq"', 1, false);

-- ----------------------------
-- Uniques structure for table browsers
-- ----------------------------
ALTER TABLE "public"."browsers" ADD CONSTRAINT "AK_browsers" UNIQUE ("user_agent");

-- ----------------------------
-- Primary Key structure for table browsers
-- ----------------------------
ALTER TABLE "public"."browsers" ADD CONSTRAINT "PK_browsers" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table clicks
-- ----------------------------
ALTER TABLE "public"."clicks" ADD CONSTRAINT "PK_clicks" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table links
-- ----------------------------
CREATE INDEX "IX_links_expiry" ON "public"."links" USING btree (
  "expires_at" "pg_catalog"."timestamp_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table links
-- ----------------------------
ALTER TABLE "public"."links" ADD CONSTRAINT "AK_links" UNIQUE ("short_code");

-- ----------------------------
-- Primary Key structure for table links
-- ----------------------------
ALTER TABLE "public"."links" ADD CONSTRAINT "PK_links" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table users
-- ----------------------------
ALTER TABLE "public"."users" ADD CONSTRAINT "AK_users" UNIQUE ("email");

-- ----------------------------
-- Primary Key structure for table users
-- ----------------------------
ALTER TABLE "public"."users" ADD CONSTRAINT "PK_users" PRIMARY KEY ("id");
