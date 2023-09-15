# md2website: markdown to static website builder

[Example website (my personal)](https://michaelsjoberg.com/)

## Usage

Running `build.py` in root turns `.md` files in pages-folder into `.html` pages and any other folders into collections of pages (e.g. posts). Page navigation is generated based on `nav.md`.

## Configuration

- `DIST_PATH = "dist"` - set output folder

- `ASSETS = ["main.css", "main.js", "highlight.min.js", "fav.png"]` - define assets to copy to output folder (css and js-files are minimized)

- `AUTHOR = "Michael Sjöberg"` - set author name for meta tags

- `DESCRIPTION = "My projects, posts, and programming notes."` - set description for meta tags

- `APP_NAME = "Michael Sjöberg"` - set app name for meta tags

- `APP_THEME = "#161716"` - set app theme for meta tags

- `SHOW_RECENT_POSTS = True` - set to `False` to hide recent posts on index page

## Watcher

Run `watch.py` to automatically rebuild on `DIR_TO_WATCH` changes.
