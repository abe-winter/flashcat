#!/usr/bin/env python3
"entrypoint"

import argparse, logging, html
import genanki
from wiki import cache_or_fetch, list_cat
from version import VERSION

def main():
    p = argparse.ArgumentParser(description=f"flashcat {VERSION} - make anki decks from wikipedia categories")
    p.add_argument('cat', help='wikipedia category name. for example, Artificial_neural_networks')
    p.add_argument('deck_id', type=int, help="unique anki deck ID")
    p.add_argument('deck_title', help="deck title")
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
    deck = genanki.Deck(args.deck_id, args.deck_title)
    for page in pages.values():
        deck.add_note(genanki.Note(
            model=genanki.builtin_models.BASIC_MODEL,
            fields=list(map(html.escape, [page['title'], page['extract']])),
        ))
    genanki.Package(deck).write_to_file(f"{''.join(char for char in args.deck_title if char.isalpha() and char.isascii())}.apkg")

if __name__ == '__main__': main()
