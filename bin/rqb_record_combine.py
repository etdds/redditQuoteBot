#!/usr/bin/env python3

from redditquotebot.utilities import RecordLoader, RecordKeeper, RecordStorer
from redditquotebot.backtesting import combine_records
from typing import List
import argparse
import sys
import os

usage = """
Example 1: Combine comments from multiple records into a single file, discarding duplicates.
    rqb_record_combine.py -c comment_record_1.json comment_record_2.json -o all_comments_output.json

Example 1: Combine comments from multiple records into a single file, appending to current comments.
    rqb_record_combine.py -c comment_record_1.json all_comments_output.json -o all_comments_output.json

Example 2: Get comments from matches is multiple record files, combine into a single comment record.
    rqb_record_combine.py -m match_record_1.json match_record_2.json -o all_match_comments_output.json

Example 3: Get comments from matches is multiple record files, combine into a single comment record, append to existing comment record.
    rqb_record_combine.py -m match_records.json -c existing_records.json master_record.json -o master_record.json
    """


def combine_comments(infiles: List[str], outfile: str):
    """Combine comments from a list of files into a single record.

    Args:
        infiles (List[str]): List of input files to source comments
        outfile (str): The name of the output file.
    """
    records_to_combine = []
    for input_file in infiles:
        with open(input_file, "r", encoding="utf-8") as handler:
            records_to_combine.append(RecordLoader.from_json(handler))
            print(f"Load {len(records_to_combine[-1].logged_comments())} comments from {input_file}.")

    # Create a new record and just add the comments.
    combined = RecordKeeper()
    combined.log_comments(combine_records(records_to_combine).logged_comments())

    with open(outfile, "w", encoding="utf-8") as handler:
        RecordStorer.to_json(handler, combined)

    print(f"Total {len(combined.logged_comments())} comments written to {outfile}.")


def combine_matches(infiles: List[str], outfile: str):
    """Get comments from the match section of a list of records and store them in as comments in the output record.

    Args:
        infiles (List[str]): List of input files with source matches
        outfile (str): The output file to store the comments as matches.
    """
    records_to_combine = []
    for input_file in infiles:
        with open(input_file, "r", encoding="utf-8") as handler:
            records_to_combine.append(RecordLoader.from_json(handler))
            print(f"Load {len(records_to_combine[-1].logged_matches())} matches from {input_file}.")

    comments = []
    for record in records_to_combine:
        for match in record.logged_matches():
            comments.append(match.comment)

    comment_record = RecordKeeper()
    comment_record.log_comments(comments)

    with open(outfile, "w", encoding="utf-8") as handler:
        RecordStorer.to_json(handler, comment_record)
    print(f"Write {len(comments)} comments from matches to {outfile}")


parser = argparse.ArgumentParser(description="Reddit quote bot record combiner.", usage=usage)

parser.add_argument(
    '-v', '--version',
    action='version', version="version"
)
parser.add_argument(
    '-o', '--output-file',
    nargs=1,
    help="Specify the output file to store combined records",
    default=None
)
parser.add_argument(
    '-c', '--comment-files',
    nargs="+",
    help="Specify records containing comments to combine.",
    default=None
)
parser.add_argument(
    '-m', '--match-files',
    nargs="+",
    help="Specify records containing matches to combine into comments.",
    default=None
)

args = parser.parse_args()

if args.output_file is None or len(args.output_file) != 1:
    print("Expected exactly one output file to be supplied.")
    sys.exit(1)

if args.match_files is not None:
    match_files = [os.path.join(os.getcwd(), p) for p in args.match_files]
    combine_matches(match_files, args.output_file[0])

if args.comment_files is not None:
    comment_files = [os.path.join(os.getcwd(), p) for p in args.comment_files]
    combine_comments(comment_files, args.output_file[0])
