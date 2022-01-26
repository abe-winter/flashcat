#!/usr/bin/env python3
"entrypoint"

import argparse, logging
from wiki import cache_or_fetch, list_cat

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--cat', default='Artificial_neural_networks')
    # todo: make creds optional. I think it's optional for real wikipedia
    # p.add_argument('--creds', default='creds.json')
    p.add_argument('--endpoint', default='https://en.wikipedia.org/w/api.php')
    p.add_argument('--contact', default='(https://github.com/abe-winter/flashcat/issues; awinter.public@gmail.com)', help="included in user-agent. replace this with your email if you're doing a lot of requests")
    p.add_argument('--maxpages', default=20, type=int, help='max pages of search results to get for category. protects against accidental infinite loops')
    p.add_argument('--cache', default='.fc-cache')
    # p.add_argument('-f', '--field', n='+', default=[''], help="make cards based on fields, not short desc")
    args = p.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    pages = cache_or_fetch(args, list_cat)

    raise NotImplementedError

if __name__ == '__main__': main()
