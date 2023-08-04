# md2html: static website builder

## Usage

Running `build.py` in root folder turns `.md` files in pages-folder into `.html` pages and other folders into collections of pages (i.e. posts, articles, links, etc).

Page navigation is generated from `nav.md`.

## Configuration

- `DIST_PATH = "dist"`, output folder
- `ASSETS = ["main.css", "main.js", "highlight.min.js", "fav.png"]`, assets to copy to output folder (css and js-files are minimized)
- `AUTHOR = "Michael Sjöberg"`, author name for meta tags
- `DESCRIPTION = "My projects, posts, and programming notes."`, description for meta tags
- `APP_NAME = "Michael Sjöberg"`, app name for meta tags
- `APP_THEME = "#161716"`, app theme for meta tags
