-- MiTrip database schema
-- Reconstructed in 2026 from the SQL statements in backend/ (the original 2023 database dump was not kept).
-- Column order of `schedule` and `trip` matters: the backend reads them with SELECT * and positional indexes.

-- The MySQL docker entrypoint does not read init scripts as UTF-8 by default; without this the
-- Chinese column names of userPreferences are stored as mojibake and the questionnaire cannot be saved.
SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS MiTrip CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE MiTrip;

CREATE TABLE IF NOT EXISTS `User` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(64) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL,          -- werkzeug password hash
  `email` VARCHAR(255) NOT NULL,
  `birthDay` DATE NULL
);

CREATE TABLE IF NOT EXISTS `Token` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `token` VARCHAR(64) NOT NULL,
  `expiration_time` DATETIME NOT NULL,
  INDEX (`token`)
);

CREATE TABLE IF NOT EXISTS `RestaurantData` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `place_id` VARCHAR(64) NULL,
  `name` VARCHAR(255) NOT NULL,
  `formatted_address` VARCHAR(1024) NULL,
  `formatted_phone_number` VARCHAR(64) NULL,
  `opening_hours` JSON NULL,                 -- Google Places opening_hours (periods + weekday_text)
  `url` TEXT NULL,
  `website` TEXT NULL,
  `rating` FLOAT NULL,
  `user_ratings_total` INT NULL,
  `price_level` INT NULL,
  `class` JSON NULL,                         -- e.g. ["中式", "日式"]
  `photos` TEXT NULL,                        -- single image URL
  `lat` DOUBLE NOT NULL,
  `lng` DOUBLE NOT NULL,
  `wheelchair_accessible_entrance` VARCHAR(8) NULL,
  `serves_breakfast` VARCHAR(8) NULL,
  `serves_brunch` VARCHAR(8) NULL,
  `serves_lunch` VARCHAR(8) NULL,
  `serves_dinner` VARCHAR(8) NULL,
  `serves_beer` VARCHAR(8) NULL,
  `serves_wine` VARCHAR(8) NULL,
  `serves_vegetarian_food` VARCHAR(8) NULL,
  `curbside_pickup` VARCHAR(8) NULL,
  `takeout` VARCHAR(8) NULL,
  `delivery` VARCHAR(8) NULL,
  `reservable` VARCHAR(8) NULL,
  INDEX (`lat`, `lng`),
  INDEX (`name`)
);

CREATE TABLE IF NOT EXISTS `AttractionData` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `place_id` VARCHAR(64) NULL,
  `name` VARCHAR(255) NOT NULL,
  `formatted_address` VARCHAR(1024) NULL,
  `formatted_phone_number` VARCHAR(64) NULL,
  `opening_hours` JSON NULL,
  `url` TEXT NULL,
  `website` TEXT NULL,
  `rating` FLOAT NULL,
  `user_ratings_total` INT NULL,
  `class` JSON NULL,                         -- e.g. ["文化景點"]
  `photos` TEXT NULL,
  `description` TEXT NULL,
  `lat` DOUBLE NOT NULL,
  `lng` DOUBLE NOT NULL,
  INDEX (`lat`, `lng`),
  INDEX (`name`)
);

CREATE TABLE IF NOT EXISTS `HotelData` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `place_id` VARCHAR(64) NULL,
  `name` VARCHAR(255) NOT NULL,
  `formatted_address` VARCHAR(1024) NULL,
  `description` TEXT NULL,
  `formatted_phone_number` VARCHAR(64) NULL,
  `website` TEXT NULL,
  `opening_hours` JSON NULL,
  `url` TEXT NULL,
  `rating` FLOAT NULL,
  `user_ratings_total` INT NULL,
  `class` JSON NULL,                         -- e.g. {"class": "民宿"}
  `numberofRooms` INT NULL,
  `lowestPrice` INT NULL,
  `ceilingPrice` INT NULL,
  `photos` TEXT NULL,
  `lat` DOUBLE NOT NULL,
  `lng` DOUBLE NOT NULL,
  INDEX (`lat`, `lng`),
  INDEX (`name`)
);

CREATE TABLE IF NOT EXISTS `RestaurantReviews` (
  `textID` INT AUTO_INCREMENT PRIMARY KEY,
  `restaurantID` INT NOT NULL,
  `userID` INT NOT NULL,
  `time` DATE NOT NULL,
  `text` TEXT NULL,
  `userRating` FLOAT NULL,
  INDEX (`restaurantID`), INDEX (`userID`)
);

CREATE TABLE IF NOT EXISTS `AttractionReviews` (
  `textID` INT AUTO_INCREMENT PRIMARY KEY,
  `attractionID` INT NOT NULL,
  `userID` INT NOT NULL,
  `time` DATE NOT NULL,
  `text` TEXT NULL,
  `userRating` FLOAT NULL,
  INDEX (`attractionID`), INDEX (`userID`)
);

CREATE TABLE IF NOT EXISTS `HotelReviews` (
  `textID` INT AUTO_INCREMENT PRIMARY KEY,
  `hotelID` INT NOT NULL,
  `userID` INT NOT NULL,
  `time` DATE NOT NULL,
  `text` TEXT NULL,
  `userRating` FLOAT NULL,
  INDEX (`hotelID`), INDEX (`userID`)
);

CREATE TABLE IF NOT EXISTS `browsingHistory` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `userID` INT NOT NULL,
  `type` VARCHAR(16) NOT NULL,               -- restaurant / attraction / hotel
  `history` INT NOT NULL,                    -- item id
  `time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX (`userID`, `type`), INDEX (`type`, `history`)
);

CREATE TABLE IF NOT EXISTS `likesHistory` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `schedule_id` INT NOT NULL,
  INDEX (`user_id`, `schedule_id`)
);

CREATE TABLE IF NOT EXISTS `schedule` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,       -- [0]
  `name` VARCHAR(255) NOT NULL,              -- [1]
  `sDescribe` TEXT NULL,                     -- [2]
  `startDate` DATETIME NOT NULL,             -- [3]
  `endDate` DATETIME NOT NULL,               -- [4]
  `userID` INT NOT NULL,                     -- [5]
  `privilege` TINYINT NOT NULL DEFAULT 0,    -- 1 = public (shown in Social)
  `numberofLikes` INT NOT NULL DEFAULT 0,
  `timeStamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX (`userID`)
);

CREATE TABLE IF NOT EXISTS `trip` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,       -- [0]
  `scheduleID` INT NOT NULL,                 -- [1]
  `type` VARCHAR(16) NOT NULL,               -- [2] Restaurant / Attraction / Hotel
  `trip` INT NOT NULL,                       -- [3] item id
  `startDate` DATETIME NOT NULL,             -- [4]
  `endDate` DATETIME NOT NULL,               -- [5]
  `userID` INT NOT NULL,                     -- [6]
  `nextHours` INT NULL,                      -- [7] travel time to next stop
  `nextMinutes` INT NULL,                    -- [8]
  INDEX (`scheduleID`), INDEX (`userID`, `type`)
);

-- One row per user: one-hot encoded answers of the travel-preference questionnaire.
CREATE TABLE IF NOT EXISTS `userPreferences` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `userID` INT NOT NULL,
  `18 歲以下` TINYINT NOT NULL DEFAULT 0,
  `18-24 歲` TINYINT NOT NULL DEFAULT 0,
  `25-34 歲` TINYINT NOT NULL DEFAULT 0,
  `35-44 歲` TINYINT NOT NULL DEFAULT 0,
  `45-54 歲` TINYINT NOT NULL DEFAULT 0,
  `55 歲以上` TINYINT NOT NULL DEFAULT 0,
  `其他` TINYINT NOT NULL DEFAULT 0,
  `女` TINYINT NOT NULL DEFAULT 0,
  `男` TINYINT NOT NULL DEFAULT 0,
  `學生` TINYINT NOT NULL DEFAULT 0,
  `家管` TINYINT NOT NULL DEFAULT 0,
  `工商業人員` TINYINT NOT NULL DEFAULT 0,
  `自由業` TINYINT NOT NULL DEFAULT 0,
  `軍/警/公/教/人員` TINYINT NOT NULL DEFAULT 0,
  `醫護人員` TINYINT NOT NULL DEFAULT 0,
  `days` FLOAT NOT NULL DEFAULT 0,
  `budget1Day` FLOAT NOT NULL DEFAULT 0,
  `budget2Day` FLOAT NOT NULL DEFAULT 0,
  `budget3-4Day` FLOAT NOT NULL DEFAULT 0,
  `budget5-6Day` FLOAT NOT NULL DEFAULT 0,
  `budget7Day` FLOAT NOT NULL DEFAULT 0,
  `其他旅遊方式` TINYINT NOT NULL DEFAULT 0,
  `自助旅行` TINYINT NOT NULL DEFAULT 0,
  `跟團旅行` TINYINT NOT NULL DEFAULT 0,
  `都喜歡` TINYINT NOT NULL DEFAULT 0,
  `一個月 ~ 三個月前` TINYINT NOT NULL DEFAULT 0,
  `一周 ~ 一個月前` TINYINT NOT NULL DEFAULT 0,
  `一周前或更短時間` TINYINT NOT NULL DEFAULT 0,
  `三個月 ~ 六個月前` TINYINT NOT NULL DEFAULT 0,
  `1 個人` TINYINT NOT NULL DEFAULT 0,
  `2 個人` TINYINT NOT NULL DEFAULT 0,
  `3~5 人` TINYINT NOT NULL DEFAULT 0,
  `6 人以上` TINYINT NOT NULL DEFAULT 0,
  `旅遊公司官方網站或實體店面` TINYINT NOT NULL DEFAULT 0,
  `旅遊書籍或雜誌` TINYINT NOT NULL DEFAULT 0,
  `旅遊相關網站或APP` TINYINT NOT NULL DEFAULT 0,
  `朋友親戚或同事推薦` TINYINT NOT NULL DEFAULT 0,
  `網路搜尋引擎` TINYINT NOT NULL DEFAULT 0,
  `不用看到討厭的人` TINYINT NOT NULL DEFAULT 0,
  `增長見聞、學習新技能` TINYINT NOT NULL DEFAULT 0,
  `放鬆身心、紓解壓力` TINYINT NOT NULL DEFAULT 0,
  `獨立探險、尋找新鮮感` TINYINT NOT NULL DEFAULT 0,
  `與親友共遊、增進感情` TINYINT NOT NULL DEFAULT 0,
  `體驗當地文化、風俗習慣` TINYINT NOT NULL DEFAULT 0,
  `Google Maps` TINYINT NOT NULL DEFAULT 0,
  `Vlog／部落格` TINYINT NOT NULL DEFAULT 0,
  `其他方式` TINYINT NOT NULL DEFAULT 0,
  `旅遊網站／APP` TINYINT NOT NULL DEFAULT 0,
  `文化景點` TINYINT NOT NULL DEFAULT 0,
  `自然景點` TINYINT NOT NULL DEFAULT 0,
  `期間活動` TINYINT NOT NULL DEFAULT 0,
  `休閒娛樂` TINYINT NOT NULL DEFAULT 0,
  `娛樂演出` TINYINT NOT NULL DEFAULT 0,
  `帳篷` TINYINT NOT NULL DEFAULT 0,
  `度假飯店` TINYINT NOT NULL DEFAULT 0,
  `民宿` TINYINT NOT NULL DEFAULT 0,
  `背包客棧` TINYINT NOT NULL DEFAULT 0,
  `膠囊旅館` TINYINT NOT NULL DEFAULT 0,
  `酒店` TINYINT NOT NULL DEFAULT 0,
  `青年旅館` TINYINT NOT NULL DEFAULT 0,
  `飯店` TINYINT NOT NULL DEFAULT 0,
  `budget1DayH` FLOAT NOT NULL DEFAULT 0,
  `中式料理_fav` TINYINT NOT NULL DEFAULT 0,
  `日式料理_fav` TINYINT NOT NULL DEFAULT 0,
  `法式料理_fav` TINYINT NOT NULL DEFAULT 0,
  `泰式料理_fav` TINYINT NOT NULL DEFAULT 0,
  `港式料理_fav` TINYINT NOT NULL DEFAULT 0,
  `美式料理_fav` TINYINT NOT NULL DEFAULT 0,
  `義式料理_fav` TINYINT NOT NULL DEFAULT 0,
  `越式料理_fav` TINYINT NOT NULL DEFAULT 0,
  `韓式料理_fav` TINYINT NOT NULL DEFAULT 0,
  `大眾運輸2` TINYINT NOT NULL DEFAULT 0,
  `自駕2` TINYINT NOT NULL DEFAULT 0,
  `大眾運輸1` TINYINT NOT NULL DEFAULT 0,
  `自駕1` TINYINT NOT NULL DEFAULT 0,
  `不太購買商品` TINYINT NOT NULL DEFAULT 0,
  `奢侈品等高檔商品` TINYINT NOT NULL DEFAULT 0,
  `當地土產、特產` TINYINT NOT NULL DEFAULT 0,
  `當地手工藝品、文化用品等特色商品` TINYINT NOT NULL DEFAULT 0,
  `博物館、藝術展覽等文化活動` TINYINT NOT NULL DEFAULT 0,
  `戶外探險、徒步旅行、露營等冒險活動` TINYINT NOT NULL DEFAULT 0,
  `瑜珈、SPA等休閒動` TINYINT NOT NULL DEFAULT 0,
  `遊樂場、主題公園等娛樂活動` TINYINT NOT NULL DEFAULT 0,
  `中式料理` TINYINT NOT NULL DEFAULT 0,
  `日式料理` TINYINT NOT NULL DEFAULT 0,
  `法式料理` TINYINT NOT NULL DEFAULT 0,
  `泰式料理` TINYINT NOT NULL DEFAULT 0,
  `港式料理` TINYINT NOT NULL DEFAULT 0,
  `美式料理` TINYINT NOT NULL DEFAULT 0,
  `義式料理` TINYINT NOT NULL DEFAULT 0,
  `越式料理` TINYINT NOT NULL DEFAULT 0,
  `韓式料理` TINYINT NOT NULL DEFAULT 0,
  INDEX (`userID`)
);
