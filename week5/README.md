## Task 2: Create database and table in your MySQL server
+ Create a new database named website
  ```MySQL
  CREATE DATABASE website;
  ```
  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/8aeb955d-e1fe-4a57-87f4-eb2a2da29352)

  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/8cd87d2b-918b-48ad-95a6-3667f8991de6)

+ Create a new table named member, in the website database, designed as below:
  ```MySQL
  CREATE TABLE member (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT "Unique ID",
    name VARCHAR(255) NOT NULL COMMENT "Name",
    username VARCHAR(255) NOT NULL COMMENT "Username",
    password VARCHAR(255) NOT NULL COMMENT "Password",
    follower_count INT UNSIGNED NOT NULL DEFAULT 0 COMMENT "Follower Count",
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT "Signup Time"
  );
  ```
  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/dfe82e87-8723-4409-8c3a-f9aec63081a4)

  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/a4bf4c67-b204-4a94-a58d-eddeb4c4ebb3)

## Task 3: SQL CRUD
+ INSERT a new row to the member table where name, username and password must be set to test. INSERT additional 4 rows with arbitrary data.
  ```MySQL
  INSERT INTO member (name, username, password, follower_count) VALUES ("test", "test", "test", 5),
  INSERT INTO  member (name, username, password, follower_count)
  VALUES
  ("Rick", "Rick", "80085", 9),
  ("Morty", "Morty", "C137", 7),
  ("Beth", "Beth", "Beth_pw", 4),
  ("Summer", "Summer", "Summer_pw", 8);
  ```
  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/f362652e-60cf-4470-b13d-cd1e5f27abdb)
  
+ SELECT all rows from the member table.
  ```MySQL
  SELECT * FROM member;
  ```
  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/eca727fe-0450-45c4-99e8-02a5e40ae3b4)

+ SELECT all rows from the member table, in descending order of time.
  ```MySQL
  SELECT * FROM member ORDER BY time DESC;
  ```
  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/84e949d7-1f5b-40eb-b72e-dedeaa87bf82)

+ SELECT total 3 rows, second to fourth, from the member table, in descending order of time. Note: it does not mean SELECT rows where id are 2, 3, or 4.
  ```MySQL
  SELECT * FROM member ORDER BY time DESC LIMIT 1,3;
  ```
  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/c020afcf-bbf8-4b98-b0ba-ace31540f5f3)

+ SELECT rows where username equals to test.
  ```MySQL
  SELECT * FROM member WHERE username="test";
  ```
  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/2ab1aee9-7ba1-4285-9986-b8a11980e5b0)

+ SELECT rows where name includes the es keyword.
  ```MySQL
  SELECT * FROM member WHERE name LIKE "%es%";
  ```
  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/fcbc902f-f0ab-4ab5-96fc-a9d7fd60da73)

+ SELECT rows where both username and password equal to test.
  ```MySQL
  SELECT * FROM member WHERE username="test" AND password="test";
  ```
  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/33bee2ab-e2a3-457f-a91c-a5bfefa3b848)

+ UPDATE data in name column to test2 where username equals to test.
  ```MySQL
  UPDATE member SET name="test2" WHERE username="test";
  ```
  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/ef3ea603-cf33-4ab5-be8d-4a9f237c0e4b)


## Task 4: SQL Aggregation Functions
+ SELECT how many rows from the member table.
  ```MySQL
  SELECT COUNT(*) FROM member;
  ```
  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/909a35a6-cdbd-4260-9fb2-e890ef87ad7a)

+ SELECT the sum of follower_count of all the rows from the member table.
  ```MySQL
  SELECT SUM(follower_count) FROM member;
  ```
  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/7e793561-3c7b-42e7-98ad-49a88a28979b)

+ SELECT the average of follower_count of all the rows from the member table.
  ```MySQL
  SELECT AVG(follower_count) FROM member;
  ```
  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/d38e4983-9239-4d0d-8220-eb99192fc9be)

+ SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table.
  ```MySQL
  SELECT AVG(follower_count)
  FROM (
    SELECT follower_count
    FROM member
    ORDER BY follower_count DESC
    LIMIT 0,2
  ) AS subquery;
  ```
  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/88806224-01fc-46fd-a8ff-4ed1609d6633)

## Task 5: SQL JOIN
+ Create a new table named message, in the website database. designed as below:
  ```MySQL
  CREATE TABLE message (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT "Unique ID", 
    member_id BIGINT NOT NULL COMMENT "Member ID for Message Sender", 
    FOREIGN KEY (member_id) REFERENCES member(id), 
    content VARCHAR(255) NOT NULL COMMENT "Content", 
    like_count INT UNSIGNED NOT NULL DEFAULT 0 COMMENT "Like Count", 
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT "Publish Time"
  );
  ```
  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/0b874775-dc30-4df7-b7a7-1a168e7884c0)

+ (addtion) INSERT test data.
  ```MySQL
  INSERT INTO message (member_id, content, like_count)
  VALUES (1, "What is my purpose?", 2),
  (2, "You test my program.", 9),
  (3, "Oh geeeees!!!!", 7),
  (1, "Oh my god", 4),
  (2, "Welcome to the club, pal", 5);
  ```
  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/a2b3474c-f6f7-4ecc-a76c-0692a19b7167)

+ SELECT all messages, including sender names. We have to JOIN the member table to get that.
  ```MySQL
  SELECT * FROM message JOIN member ON message.member_id=member.id;
  ```
  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/35a8c162-2aa3-4c8a-be57-740b9b961ac4)

+ SELECT all messages, including sender names, where sender username equals to test. We have to JOIN the member table to filter and get that.
  ```MySQL
  SELECT * FROM message JOIN member ON message.member_id=member.id WHERE username="test";
  ```
  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/5db75a4a-5bb8-4093-9932-45202d056b4a)

+ Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender username equals to test.
  ```MySQL
  SELECT AVG(like_count) FROM message JOIN member ON message.member_id=member.id WHERE username="test";
  ```
  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/0baf2a33-b3fe-4392-bb93-59c38797f80d)

+ Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender username.
  ```MySQL
  SELECT username, AVG(like_count) FROM message JOIN member ON message.member_id=member.id GROUP BY username;
  ```
  ![image](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/48964990-95db-4d0a-9a45-66df4f445d21)

