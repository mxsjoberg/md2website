# md2website: markdown to static website builder

Example websites:

- [DEMO](https://md2website.pages.dev/)
- [My personal](https://michaelsjoberg.com/)
- [My notes](https://notes.michaelsjoberg.com/)

## Usage

Running `python3 build.py <path/to/source>` turns `.md` files in pages-folder (see demo folder structure) into `.html` pages and any other folders into list pages (e.g., blog posts, articles, files). Files are embedded into `.html` pages and code is highlighted.

Page navigation is generated based on `nav.md`, which should be in root folder of source.

Page anchors and table of contents are automatically generated from `##` and `###` tags if `toc`-flag is set to `true`. Table of contents is injected right before the first `##` tag.

## Configuration

Create a `.md2website-configure` file in root of source with following contents:

```
DIST_PATH = "../dist"
LOAD_FOLDER = "../../files"
LOAD_FOLDER_FLAGS = "-* col=2;sort=name;desc=My code"
AUTHOR = "Your Name"
DESCRIPTION = "A description for your website."
GOOGLE_TAG = "<your google analytics tag>"
APP_NAME = "My Website"
POSTS_ON_INDEX = False
STYLING = True
DEFAULT_THEME = "dark"
ALLOW_CHANGE_THEME = True
```

Set `LOAD_FOLDER` and `LOAD_FOLDER_FLAGS` to `False` if not loading external folders into source folder.

Set `GOOGLE_TAG` to `False` if no analytics.

Set `POSTS_ON_INDEX` to `True` if you want to show posts on index page.

Set `STYLING` to `False` to disable default styling (not implemented yet).

There are two themes for `DEFAULT_THEME`: `dark` and `light`.

Set `ALLOW_CHANGE_THEME` to `False` to remove toggle theme button.


## Flags

Folder can have a `__flags` file to customize list pages, e.g., a flag file with content `-* col=3;desc=My notes` would split listed content into three columns and add the intro text "My notes" under title.

Experimental feature (not fully implemented yet): Flags can also placed as first line in `.md` files to customize individual pages (such as `-* toc=true` to include table of content on page).

## Watcher

Run `python3 watch.py <path/to/source> <path/to/dist>` to watch for changes in source, rebuild, and serve dist on localhost.
