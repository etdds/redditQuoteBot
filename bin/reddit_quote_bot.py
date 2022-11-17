#!/usr/bin/env python3

import sys
import datetime
import argparse
import os
import logging
import importlib.resources as pkg_resources

import redditquotebot.data
from redditquotebot import BotBuilder
from redditquotebot.quotes import QuoteLoader
from redditquotebot.nlp import QuoteCommentNLPMatcher, QuoteNLPDetector
from redditquotebot.utilities import CredentialGenerator, ConfigurationGenerator, setup_logger

conifguration_file_name = "configuration.json"
credentials_file_name = "credentials.json"
scrape_state_file_name = "scrape_state.json"
records_file_name = "records.json"


def generate_configuration(path: str):
    full_path = os.path.join(os.getcwd(), path)
    if os.path.exists(full_path):
        print(f"The path {full_path} already exists. Delete this file to replace it if this is what was really intended.")
        return
    with open(full_path, "w") as handler:
        ConfigurationGenerator.to_json(handler)


def generate_credentials(path: str):
    full_path = os.path.join(os.getcwd(), path)
    if os.path.exists(full_path):
        print(f"The path {full_path} already exists. Delete this file to replace it if this is what was really intended.")
        return
    with open(full_path, "w") as handler:
        CredentialGenerator.to_json(handler)


parser = argparse.ArgumentParser()

parser.add_argument(
    '-v', '--version',
    action='version', version="version"
)
parser.add_argument(
    '-g', '--generate-config',
    action='store_true',
    help="Generate the required credential and configuration files needed.",
    default=False
)

args = parser.parse_args()
if args.generate_config:
    generate_configuration(conifguration_file_name)
    generate_credentials(credentials_file_name)
    sys.exit()

timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
builder = BotBuilder()

try:
    builder.configuration(os.path.join(os.getcwd(), conifguration_file_name))
    builder.credentials(os.path.join(os.getcwd(), credentials_file_name))
except FileNotFoundError:
    generate_configuration(conifguration_file_name)
    generate_credentials(credentials_file_name)
    print("Modify and populate credential files in order to configure bot.")
    sys.exit()

builder.recored_keeper(os.path.join(os.getcwd(), records_file_name))
builder.scrape_state(os.path.join(os.getcwd(), scrape_state_file_name))
quote_handler = pkg_resources.open_text(redditquotebot.data, "quotes.csv")
quotes = QuoteLoader.from_csv(quote_handler)

config = builder.loaded_configuration()
builder.quotes(quotes)
builder.quote_matcher(
    QuoteCommentNLPMatcher(
        quote_comment_delta=config.nlp.quote_comment_length_delta,
        minimum_sentence_word_length=config.nlp.minimum_comment_sentence_word_length,
        bonus_coeff=config.nlp.quote_length_bonus_coefficient,
        bonus_start=config.nlp.quote_length_bonus_start,
        bonus_end=config.nlp.quote_length_bonus_end,
        match_sentence_coeff=config.nlp.matched_sentence_coefficient
    ),
    config.nlp.match_store_threshold
)
builder.quote_detector(QuoteNLPDetector)

setup_logger(logging.INFO, f"run_log_{timestamp}.log")
bot = builder.bot()
bot.connect()
bot.start()
