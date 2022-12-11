# Reddit Quote Bot

Reads all comments in selected subreddits and compares their comments to famous quotes. On a close match, replies with the full quote, crediting the original author.

![Comment Demo](images/comment_demo.png?raw=true "Example reply")

I'm live! Check out what I've been up to on [Reddit](https://www.reddit.com/user/redditQuoteBot/comments/).

## Overview

The bot periodically requests comments from selected subreddits, sorted by newest submissions. Each comment, is compared for similarity to a dataset of [quotes](https://www.kaggle.com/datasets/abireltaief/english-quotes) using [spacy](https://spacy.io/). If a high similarity is detected, a reply is generated and posted as a response to the original comment.


## Running a bot instance

### Using Python

The package is available on [pypi](https://pypi.org/project/redditquotebot/), it can be installed with:

```bash
pip install redditquotebot
```

A Spacy language model is also needed for natural language processing. Testing is conducted with `en-core-web-md`:
```bash
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.4.1/en_core_web_md-3.4.1-py3-none-any.whl
```

Generate the configuration and credential templates in the current directory (see reference below):
```bash
reddit_quote_bot.py -g
```

Start up the bot:
```bash
reddit_quote_bot.py
```

### Using Docker

Currently, the only option is to build the container from source. Eventually, this will be pushed to [Docker Hub](https://hub.docker.com/).

Clone this repository:

```bash
git clone https://github.com/etdds/redditQuoteBot.git
cd redditQuoteBot
```

Build the docker container:
```
make build-image
# or
docker build -t etdds/reddit-quote-bot:latest .
```

Start up the bot. The configuration and credential templates are generated on the first run. Populate these files then restart the container.
```
# Initial run to generate configuration
docker run -v $(pwd):/home/app_user/run etdds/reddit-quote-bot

# Run the container, detached, restarting unless stopped.
docker run --restart unless-stopped -d -v $(pwd):/home/app_user/run etdds/reddit-quote-bot
```

The mounted directory is used to store the configuration files, credentials, comment and reply records and state.

## Runtime file descriptions

The bot uses four files during runtime, these are created and stored in the directory from where the bot is started.

### Configuration

The configuration file `configuration.json` is created the first time is run, and read once on startup. 

```json
{
  "reddit": {
    "subreddits": [
      "test"
    ],
    "new_submissions_per_request": 10,
    "max_comments_per_request": 100,
    "minimum_comment_length": 15
  },
  "bot": {
    "reply_to_comments": true,
    "reply_threshold": 0.99,
    "matched_quotes_to_log": 3,
    "remove_own_comments": true,
    "remove_comment_threshold": -1
  },
  "nlp": {
    "match_store_threshold": 0.97,
    "quote_comment_length_delta": 0.7,
    "minimum_comment_sentence_word_length": 5,
    "quote_length_bonus_coefficient": 0.0008,
    "quote_length_bonus_start": 6,
    "quote_length_bonus_end": 10,
    "matched_sentence_coefficient": 0.5,
    "discard_comments_with_author": true
  },
  "records": {
    "maximum_comment_count": 0,
    "maximum_match_count": 100,
    "maximum_reply_count": null
  }
}
```
| Section       | Subsection                            |    Description                                                                                            |
| ------------- | -------------                         | -------------                                                                                             |
|reddit         | subreddit                             |  List of subreddits from which comments are taken    |
|               | new_submissions_per_request           |  The maximum number of submissions (posts) which are taken    |
|               | max_comments_per_request              |  The maximum number comments which are queried per request.   |
|               | minimum_comment_length                |  The minimum length of a comment which is stored. Shorter comments are discarded. |
|bot            | reply_to_comments                     |  If set to true, replies are posted to reddit. If false, they are only logged in `records.json` |
|               | reply_threshold                       |  The NLP score needed in order for a reply to be sent. Ranging between 0-1 |
|               | matched_quotes_to_log                 |  The number of matches above `match_store_threshold` to log. |
|               | remove_own_comments                   |  Toggle the bot's ability to remove it's own comments |
|               | remove_comment_threshold              |  Toggle the comment score at which a comment is removed. Comments which score equal or below this value are removed. |
|nlp            | match_store_threshold                 |  The NLP score threshold for comments which are stored, under `matches` in `records.json` |
|               | quote_comment_length_delta            |  The maximum difference ratio between the length of a comments sentence and quote sentence to be compared. Quote / comment sentence ratios outside this range are discarded. |
|               | minimum_comment_sentence_word_length  |  The minimum word length a comment needs to be in order to be compared with a quote. |
|               | quote_length_bonus_coefficient        |  The coefficient applied per word to the NLP score for comment quote sentences matches when they longer than `quote_length_bonus_start` |
|               | quote_length_bonus_start              |  The starting quote sentence length needed for the NLP score bonus to be applied. |
|               | quote_length_bonus_end                |  The maximum quote sentence length to which a bonus NLP score is applied. |
|               | discard_comments_with_author          |  Define if comments should be matched to quotes when the body of the comment contains the author of the quote |
|records        | maximum_comment_count                 |  Specify the maximum number of comments to be logged in `records.json` . 0 = None, null = No limit |
|               | maximum_match_count                   |  Specify the maximum number of matches to be logged in `records.json`. 0 = None, null = No limit |
|               | maximum_reply_count                   |  Specify the maximum number of replies to be logged in `records.json`. 0 = None, null = No limit |
|               | maximum_removed_comment_count         |  Specify the maximum number of removed comments to be logged in `records.json`. 0 = None, null = No limit |

### Credentials

The credentials file `credentials.json` is created the first time is run, and read once on startup. Currently, this means the credentials are stored in plain text. This should be changed.

The fields for the `reddit` object are identically named, and passed directly to [Praw](https://praw.readthedocs.io/en/stable/index.html). See Praw's documentation [here](https://praw.readthedocs.io/en/stable/getting_started/authentication.html).

```json
{
  "reddit": {
    "user_agent": "",
    "client_id": "",
    "client_secret": "",
    "username": "",
    "password": ""
  }
}
```

### Records 

The record file, `records.json` is automatically generated and updated during the bots runtime. A minimum example would look like:

#### Comments Section

Contains a log of all comments fetched which meet the minimum length criteria, have not been edited, and are not part of the author blacklist.

#### Matches Section

Contains a log of all comments and quotes which matched with a score above the `match_store_threshold` score.

#### Replies Section

Contains a log of all replies which have been sent (or just logged if `reply_to_comments` is set to false). These are generally matches with a score above `reply_threshold`.

#### Removed Section

Contains a log of all self-posted comments that the bot has removed.

#### Banned Subreddit Section

Contains a list of subreddits which the bot thinks it is banned from. This is determined by receiving a forbidden exception when trying to post a reply.

```json
{
    "records": {
      "comments": [
        {
          "body": "Eight billion people, it is a momentous milestone for humanity\n\nYet, I realise this moment might not be celebrated by all.\n\nInstead of the fear of overpopulation, we should focus on the overconsumption of the planet\u2019s resources by the wealthiest among us.",
          "utc": 1667800195.0,
          "author": "cop3213",
          "url": "https://reddit.com/r/worldnews/comments/yodyyg/planet_earth_8_billion_people_and_dwindling/ivdteb8/",
          "subreddit": "r/worldnews",
          "edited": false,
          "uid": "ivdteb8"
        },
      ],
      "matches": [
        {
          "comment": {
            "body": "The question feels very cryptic. What are you trying to do?",
            "utc": 1667805202.0,
            "author": "dbug89",
            "url": "https://reddit.com/r/AusFinance/comments/yofkj7/salary_sacrificing_super/ivdzyjj/",
            "subreddit": "r/AusFinance",
            "edited": false,
            "uid": "ivdzyjj"
          },
          "quote": {
            "body": "Always do what you are afraid to do.",
            "author": "Ralph Waldo Emerson",
            "category": [
              "'inspirational'"
            ]
          },
          "score": 0.9728559309059505
        }
      ],
      "replies": [
        {
          "quote": {
            "body": "Just because you're paranoid doesn't mean they aren't after you.",
            "author": "Joseph Heller,",
            "category": [
              "'misattributed-kurt-cobain'"
            ]
          },
          "comment": {
            "body": "*just because you're not paranoid doesn't mean they're not after you*",
            "utc": 1667874409.0,
            "author": "peter-doubt",
            "url": "https://reddit.com/r/worldnews/comments/yp7yux/afp_says_it_does_not_believe_china_has_an_active/ivhyeqv/",
            "subreddit": "r/worldnews",
            "edited": false,
            "uid": "ivhyeqv"
          },
          "body": "Hi peter-doubt,\n\nIt looks like your comment closely matches the famous quote:\n\n\"Just because you're paranoid doesn't mean they aren't after you.\"\n\nJoseph Heller,\n\nI'm a bot and this action was automatic. [project source](https://www.google.com)\n        "
        }
      ],
      "removed": [
        {
          "body": "Hi Mikey2bz,\n\nIt looks like your comment closely matches the famous quote:\n\n\"It hurts to let go. Sometimes it seems the harder you try to hold on to something or someone the more it wants to get away. You feel like some kind of criminal for having felt, for having wanted. For having wanted to be wanted. It confuses you, because you think that your feelings were wrong and it makes you feel so small because it's so hard to keep it inside when you let it out and it doesn't coma back. You're left so alone that you can't explain. Damn, there's nothing like that, is there? I've been there and you have too. You're nodding your head.\" - Henry Rollins,\n\n*I'm a bot and this action was automatic [Project source](https://github.com/etdds/redditQuoteBot).*",
          "utc": 1669551675.0,
          "author": "redditQuoteBot",
          "url": "https://reddit.com/r/Futurology/comments/z5mtb3/we_tasted_the_worlds_first_cultivated_steak_no/ixyo0nc/",
          "subreddit": "r/Futurology",
          "edited": false,
          "uid": "ixyo0nc",
          "score": -2
        },
      ],
      "banned_subreddits": [
        "test"
      ]
    }
  }
```

### Bot State

The current state of the bot is stored in an autogenerated file `scrape_state.json`. Currently, this only keeps a log of the latest comment timestamp in UTC for each subreddit queried.

```json
{
  "latest_comments": {
    "worldnews": 1667877818.0,
    "science": 1667877772.0,
    "AusFinance": 1667877814.0,
    "news": 1667877770.0,
    "ShowerThoughts": 1667877860.0,
    "askscience": 1667875135.0,
    "nottheonion": 1667877792.0,
    "space": 1667877875.0,
    "books": 1667877515.0,
    "UpliftingNews": 1667877390.0,
    "test": 1667856381.0
    }
}
```

## Development

The repository is setup to use VSCode with the remote development plugin. Everything should be self-contained within this environment.

Contributions and suggestions welcome. Open and an issue or formulate a pull request.
