-- Drop table if exists
DROP TABLE twitter_tweets;

--create table in Twitter_DB
CREATE TABLE twitter_tweets(
    index INTEGER,
    monday_tweets VARCHAR NOT NULL,
    friday_tweets VARCHAR NOT NULL,
    april_tweets VARCHAR NOT NULL,
    -- date DATE,
    -- source VARCHAR NOT NULL,
    -- likes INTEGER,
    -- retweets INTEGER,
    PRIMARY KEY (index)
);

-- --create table in Twitter_DB
-- CREATE TABLE twitter_friday(
--     friday_tweets VARCHAR NOT NULL
--     -- friday_tweets VARCHAR NOT NULL,
--     -- april_tweets VARCHAR NOT NULL
--     -- date DATE,
--     -- source VARCHAR NOT NULL,
--     -- likes INTEGER,
--     -- retweets INTEGER,
--     -- PRIMARY KEY (index)
-- );

-- --create table in Twitter_DB
-- CREATE TABLE twitter_april(
--     april_tweets VARCHAR NOT NULL
--     -- friday_tweets VARCHAR NOT NULL,
--     -- april_tweets VARCHAR NOT NULL
--     -- date DATE,
--     -- source VARCHAR NOT NULL,
--     -- likes INTEGER,
--     -- retweets INTEGER,
--     -- PRIMARY KEY (index)
-- );