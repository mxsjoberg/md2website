# md2html: static website builder

[Example website built with md2html (my personal)](https://michaelsjoberg.com/)

## Usage

Running `build.py` in root turns `.md` files in pages-folder into `.html` pages and any other folders into collections of pages (e.g. posts, articles, links).

Page navigation is generated based on `nav.md`.

## Configuration

- `DIST_PATH = "dist"` to set output folder

- `ASSETS = ["main.css", "main.js", "highlight.min.js", "fav.png"]` to define assets to copy to output folder (css and js-files are minimized)

- `AUTHOR = "Michael Sjöberg"` to set author name for meta tags

- `DESCRIPTION = "My projects, posts, and programming notes."` to set description for meta tags

- `APP_NAME = "Michael Sjöberg"` to set app name for meta tags

- `APP_THEME = "#161716"` to set app theme for meta tags

## Watcher

Run `watch.py` to automatically rebuild on `.md`-file changes.
