Consider the design of a database for an online store. Each item is identified by a unique item ID, a
title, a description of the item, the date the item is posted, price, and a list of categories (each category
is a single word in lower cases). Only registered users can post, buy, and review an item. Each registered
user is identified by a user ID or username (or both), a password, a first name, a last name, and an email
address. A user can give at most one review for each item, and on a particular day, the user can post at
most 3 items and 3 reviews. Meanwhile, an item can have no or many reviews. The review given by a
user provides a score of "Excellent, Good, Fair, or Poor" and then a short remark. A user cannot modify
an existing review that she/he gave earlier


CREATE TABLE IF NOT EXISTS items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    price DECIMAL(10, 2)
);

-- SAMPLE INSERT
INSERT INTO Items (title, description, price)
VALUES ('New Item', 'Description of the new item.', 29.99);

-- REMAINS TO CONSIDER for Item table "and a list of categories (each category is a single word in lower cases)"
-- Idea make a categories table, use item_id foreign key to make the one to many sync
CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    item_id INT,
    FOREIGN KEY (item_id) REFERENCES Items(item_id)
);

-- Only registered users can post, buy, and review an item.
-- Already handled by log in

--Each registered user is identified by a user ID or username (or both), a password, a first name, a last name, and an email address
-- Current set up in phase 1
CREATE TABLE IF NOT EXISTS user (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(100) NOT NULL,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE
)

-- We can make the following change if we want to maintain a user_id too
CREATE TABLE IF NOT EXISTS user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(100) NOT NULL,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE
)

-- Review table
CREATE TABLE IF NOT EXISTS Reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    item_id INT NOT NULL,
    score VARCHAR(20) NOT NULL,
    remark TEXT NOT NULL,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES Users(username),
    FOREIGN KEY (item_id) REFERENCES Items(item_id),
    CONSTRAINT no_update_reviews CHECK (1 = 1),
    CONSTRAINT unique_user_item_review UNIQUE (username, item_id),
);

-- Last thing to consider will be these constraints
--  A user can give at most one review for each item (unique_user_item_review), and on a particular day, the user can post atmost 3 items and 3 reviews
CREATE TABLE IF NOT EXISTS UserActivity (
    username VARCHAR(50),
    activity_date DATE DEFAULT CURRENT_DATE,
    items_posted INT DEFAULT 0,
    reviews_posted INT DEFAULT 0,
    PRIMARY KEY (username, activity_date),
    FOREIGN KEY (username) REFERENCES Users(username)
);
-- Use this table before allowing new insert item, insert review


_____________________________ SQL ONLY ___________________________________



-- Drop tables
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS UserActivity;


_______________________________ Phase 3 _____________________________

-- Phase3_1
select max(i.price), c.category_name
from categories c join items i on c.item_id = i.item_id
group by c.category_name

-- Phase3_2
SELECT DISTINCT u1.username, DATE(u1.date_posted)
FROM items u1
JOIN items u2 ON u1.username = u2.username AND DATE(u1.date_posted) = DATE(u2.date_posted)
JOIN categories c1 on c1.item_id = u1.item_id
JOIN categories c2 on c2.item_id = u2.item_id
WHERE c1.category_name = 'Fitness' 
  AND c2.category_name = 'Photography'
  AND c1.category_name <> c2.category_name;

-- Phase3_3
-- Items 6 and 7 from mdhindsa, 6 is expected to return and 7 is not
SELECT I.*
FROM items I
JOIN Reviews R ON I.item_id = R.item_id
WHERE I.username = 'mdhindsa'
GROUP BY I.item_id
HAVING COUNT(R.item_id) = COUNT(CASE WHEN R.score IN ('Excellent', 'Good') THEN 1 END);

-- Phase3_4
SELECT UA.USERNAME, UA.ACTIVITY_DATE
FROM USERACTIVITY UA
WHERE DATE(UA.ACTIVITY_DATE) = '2023-07-26'
AND UA.ITEMS_POSTED = (
	SELECT MAX(UA1.ITEMS_POSTED)
	FROM USERACTIVITY UA1
	WHERE DATE(UA1.ACTIVITY_DATE) = '2023-07-26'
)

-- Phase3_5
SELECT R.USERNAME
FROM REVIEWS R
GROUP BY R.USERNAME
HAVING COUNT(R.USERNAME) = COUNT(CASE WHEN R.score = 'Poor' THEN 1 END);

-- Phase3_6
SELECT i.username
FROM items i, Reviews R2
WHERE I.item_id = R2.item_id
group by i.username
having COUNT(R2.item_id) = COUNT(CASE WHEN R2.score Not IN ('Poor') THEN 1 END);
