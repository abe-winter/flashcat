"wikipedia harness"

import json, logging, os
from typing import Dict
import requests
from version import VERSION

class TooManyPages(Exception):
    "you exceeded maxpages"

def list_cat(args, session) -> Dict[str, dict]:
    "return dict of {pageid: obj} for pages in category"
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

def cache_or_fetch(args, fetch_fn) -> Dict[str, dict]:
    "fetch from cache if present, else fetch from wikipedia"
    if not os.path.exists(args.cache):
        logging.info('creating cache folder %s', args.cache)
        os.mkdir(args.cache)

    cache_path = os.path.join(args.cache, f'{args.cat}.json')
    if os.path.exists(cache_path):
        pages = json.load(open(cache_path))
        logging.info('loaded %d pages from cache', len(pages))
    else:
        session = requests.Session()
        session.headers = {'User-Agent': f"flashcat/{VERSION} {args.contact} python-requests/{requests.__version__}"}
        pages = fetch_fn(args, session)
        logging.info('fetched %d pages', len(pages))
        json.dump(pages, open(cache_path, 'w'))

    return pages
