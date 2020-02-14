import sys
import errno
import re
import os
import json

from collections import Counter

import click

@click.command()
@click.option("-i", help="File input.")
@click.option("-t", help="Type of input data. Supports cowrie.")
@click.option("-o", multiple=True, help="Output types. Supports txt, csv, sqlite, and json")
def main(i, t, o):

    if i and o and t:
        input_file = i
        output_file = o
        log_type = t

        wordlist = parse_log(input_file, log_type)
        write_wordlist(wordlist, output_file)

    else:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit()


def write_wordlist_sqlite(wordlist, output_option):
    pass 

def write_wordlist_csv(wordlist, output_option):
    pass 

def write_wordlist_json(wordlist, output_option):
    pass

def write_wordlist(wordlist, output_option):
    pass 

def write_wordlist_plaintext(wordlist, output_option):
    try:
        with open(output_option, "a") as f:
            for word in wordlist:
                f.write(word + "\n")
    except IOError as x:
        print(x)

def write_wordlist(wordlist, output_file):

    file_types = {
        "sql": write_wordlist_sqlite,
        "sqlite": write_wordlist_sqlite,
        "csv": write_wordlist_csv,
        "": write_wordlist_plaintext,
    }

    for output_option in output_file:
        if os.path.exists(output_option):
            sys.exit("{output_option} already exists!".format(output_option=output_option))

    for output_option in output_file:
        file_extension = re.match(r'[a-zA-Z\d]+\.([a-zA-Z\d]+)', output_option)
        file_extension = None if not file_extension else file_extension.groups()[0]
        if file_extension in file_types.keys():
            file_types[file_extension](wordlist, output_option)
        else:
            write_wordlist_plaintext(wordlist, output_option)

def parse_log(input_file, log_type):
    if log_type == "cowrie":
        output = parse_cowrie(input_file)

    return output

def parse_cowrie(input_file):
    wordlist = []

    try:
        with open(input_file, "r") as f:
            log = f.read().splitlines()
            for entry in log:
                entry = json.loads(entry)
                password = entry.get("password")
                if password:
                    wordlist.append(password)
    except IOError as x:
        if x.errno == errno.ENONET:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), input_file)
        elif x.errno == errno.EACCES:
            raise FileNotFoundError(errno.EACCES, os.strerror(errno.EACCES), input_file)

    counted = Counter(wordlist)
    return sorted(counted, key=counted.get, reverse=True)


if __name__ == "__main__":
    main()
