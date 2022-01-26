# flashcat

CLI tool which turns a wikipedia category into anki flash cards.

## usage

```sh
# one-time setup
direnv allow
pip install -r requirements.txt

# create an anki deck
UNIQUE_ID=12345678
TITLE=anntypes
./flashcat.py Artificial_neural_networks $UNIQUE_ID $TITLE
# anki output will be anntypes.apk

# get help
./flashcat.py --help
```

## features and wishlist

- [x] for every page in a wikipedia category, capture the first paragraph to an anki card
- [x] caching to disk so you can rerun queries while tinkering
- [ ] capture template boxes to do things like date of birth or 'preceded / followed by', country demonym, a million things
- [ ] capture wikipedia props to anki tags so you can filter in the anki app (supreme court cases by year, for example)
- [ ] do something useful with images
- [ ] fix html entities
- [ ] unbreak mathjax
