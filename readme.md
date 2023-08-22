# md2html: static website builder

████████████████████████████████████████████
█▄─▀█▀─▄█▄─▄▄▀█▀▄▄▀█─█─█─▄─▄─█▄─▀█▀─▄█▄─▄███
██─█▄█─███─██─██▀▄██─▄─███─████─█▄█─███─██▀█
▀▄▄▄▀▄▄▄▀▄▄▄▄▀▀▄▄▄▄▀▄▀▄▀▀▄▄▄▀▀▄▄▄▀▄▄▄▀▄▄▄▄▄▀

## Usage

Running `build.py` in root turns `.md` files in pages-folder into `.html` pages and other folders into collections of pages (i.e. posts, articles, links, etc).

Page navigation is generated from `nav.md`.

## Configuration

`DIST_PATH = "dist"`

Output folder.

`ASSETS = ["main.css", "main.js", "highlight.min.js", "fav.png"]`

Assets to copy to output folder (css and js-files are minimized).

`AUTHOR = "Michael Sjöberg"`

Author name for meta tags.

`DESCRIPTION = "My projects, posts, and programming notes."`

Description for meta tags.

`APP_NAME = "Michael Sjöberg"`

App name for meta tags.

`APP_THEME = "#161716"`

App theme for meta tags.

## Watcher

Run `watch.py` to automatically rebuild on file changes.
