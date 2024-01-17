# Data Dictionary

## Staging Tables

### `staging_tweets`

- `user_id`: User ID (varchar)
- `name`: User name (varchar)
- `nickname`: User nickname (varchar)
- `description`: User description (varchar)
- `user_location`: User location (varchar)
- `followers_count`: Number of followers (integer)
- `tweets_count`: Number of tweets (integer)
- `user_date`: User creation date (timestamp)
- `verified`: User verification status (boolean)
- `tweet_id`: Tweet ID (varchar)
- `text`: Tweet text (varchar)
- `favs`: Number of favorites (integer)
- `retweets`: Number of retweets (integer)
- `tweet_date`: Tweet creation date (timestamp)
- `tweet_location`: Tweet location (varchar)
- `source`: Source of the tweet (varchar)
- `sentiment`: Sentiment of the tweet (varchar)

### `staging_happiness`

- `country`: Country name (varchar)
- `rank`: Happiness rank (smallint)
- `score`: Happiness score (decimal)
- `confidence_high`: High confidence level (decimal)
- `confidence_low`: Low confidence level (decimal)
- `economy`: Economic factor (decimal)
- `family`: Family factor (decimal)
- `health`: Health factor (decimal)
- `freedom`: Freedom factor (decimal)
- `trust`: Trust factor (decimal)
- `generosity`: Generosity factor (decimal)
- `dystopia`: Dystopia factor (decimal)

### `staging_temperature`

- `date`: Date of temperature record (timestamp)
- `temperature`: Recorded temperature (decimal)
- `uncertainty`: Uncertainty in temperature (decimal)
- `country`: Country name (varchar)

## Dimension Tables

### `users`

- `user_id`: User ID (varchar)
- `name`: User name (varchar)
- `nickname`: User nickname (varchar)
- `description`: User description (varchar)
- `location`: User location (varchar)
- `followers_count`: Number of followers (integer)
- `tweets_count`: Number of tweets (integer)
- `creation_date`: User creation date (timestamp)
- `is_verified`: User verification status (boolean)

### `sources`

- `source_id`: Source ID (bigint)
- `source`: Source name (varchar)
- `is_mobile`: Whether the source is mobile (boolean)
- `is_from_twitter`: Whether the source is from Twitter (boolean)

### `happiness`

- `country`: Country name (varchar)
- `rank`: Happiness rank (smallint)
- `score`: Happiness score (decimal)
- `economy`: Economic factor (decimal)
- `family`: Family factor (decimal)
- `health`: Health factor (decimal)
- `freedom`: Freedom factor (decimal)
- `trust`: Trust factor (decimal)
- `geneorsity`: Generosity factor (decimal)
- `dystopia`: Dystopia factor (decimal)

### `temperature`

- `country`: Country name (varchar)
- `temp_last_20`: Average temperature over the last 20 years (decimal)
- `temp_last_50`: Average temperature over the last 50 years (decimal)
- `temp_last_100`: Average temperature over the last 100 years (decimal)

### `time`

- `date`: Date (timestamp)
- `second`: Second of the date (integer)
- `minute`: Minute of the date (integer)
- `hour`: Hour of the date (integer)
- `week`: Week of the date (integer)
- `month`: Month of the date (varchar)
- `year`: Year of the date (integer)
- `weekday`: Weekday of the date (varchar)

## Fact Table

### `tweets`

- `tweet_id`: Tweet ID (varchar)
- `text`: Tweet text (varchar)
- `favs`: Number of favorites (integer)
- `retweets`: Number of retweets (integer)
- `creation_date`: Tweet creation date (timestamp)
- `location`: Tweet location (varchar)
- `user_id`: User ID (varchar)
- `source`: Source of the tweet (varchar)
- `happy_rank`: Happiness rank (smallint)
- `happy_score`: Happiness score (decimal)
- `temp_last_20`: Average temperature over the last 20 years (decimal)
- `temp_last_50`: Average temperature over the last 50 years (decimal)
- `temp_last_100`: Average temperature over the last 100 years (decimal)

