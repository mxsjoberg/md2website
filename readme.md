# md2website: markdown to static website builder

[Example website (my personal)](https://michaelsjoberg.com/)

## Usage

Running `build.py` in root turns `.md` files in pages-folder into `.html` pages and any other folders into collections of pages (e.g. posts). Page navigation is generated based on `nav.md`. Page anchors are automatically generated from `##` and `###` tags if `toc`-flag is set to `true`. Page index is injected right before the first `##` tag.

## Configuration

- `DIST_PATH = "dist"` - set output folder

- `ASSETS = ["main.css", "main.js", "fav.png"]` - define assets to copy to output folder (css and js-files are minimized)

- `AUTHOR = "Michael Sjöberg"` - set author name for meta tags

- `DESCRIPTION = "My projects, posts, and programming notes."` - set description for meta tags

- `APP_NAME = "Michael's Page"` - set app name for meta tags

- `APP_THEME = "#161716"` - set app theme for meta tags

- `POSTS_ON_INDEX = True` - set to `False` to remove posts from index page

## Flags

Folder can have a `__flags` file to further customize generated pages. I.e. flag file with content `-* col=3,desc=My notes` would split files in folder into three columns and add text "My notes" under title.

Flags can also placed as first line in `.md` files. Currently only used to generate anchors and index on regular pages with `-* toc=true`.

## Watcher

Run `watch.py` to automatically rebuild on `DIR_TO_WATCH` changes.
