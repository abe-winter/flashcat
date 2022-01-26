#!/usr/bin/env python3
"entrypoint"

import argparse, json, logging, os
import requests

VERSION = '0.0.1'

class TooManyPages(Exception):
    "you exceeded maxpages"

def list_cat(args, session):
    args.endpoint
    params = {
        'action': 'query',
        'generator': 'categorymembers',
        'gcmtitle': f'Category:{args.cat}',
        'gcmtype': 'page',
        'gcmlimit': 20,
        'format': 'json',
        'prop': 'extracts',
        'exintro': '',
        'explaintext': '',
        'redirects': 1,
    }
    pages = {}
    for _ in range(args.maxpages):
        res = session.get(args.endpoint, params=params).json()
        pages.update(res['query']['pages'])
        if 'continue' not in res:
            break
        params['gcmcontinue'] = res['continue']['gcmcontinue']
    else:
        raise TooManyPages
    return pages

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

    user_agent = f"flashcat/{VERSION} {args.contact} python-requests/{requests.__version__}"
    logging.debug('user-agent %s', user_agent)
    # creds = json.load(open(args.creds))

    if not os.path.exists(args.cache):
        logging.info('creating cache folder %s', args.cache)
        os.mkdir(args.cache)

    cache_path = os.path.join(args.cache, f'{args.cat}.json')
    if os.path.exists(cache_path):
        pages = json.load(open(cache_path))
        logging.info('loaded %d pages from cache', len(pages))
    else:
        session = requests.Session()
        session.headers = {'User-Agent': user_agent}
        pages = list_cat(args, session)
        logging.info('fetched %d pages', len(pages))
        json.dump(pages, open(cache_path, 'w'))

    raise NotImplementedError

if __name__ == '__main__': main()
