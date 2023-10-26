# md2website: markdown to static website builder

# build demo: python3 build.py demo
# watch demo: python3 watch.py demo __dist

import os
import sys
import re
import shutil
import markdown
import sass
import traceback
from datetime import datetime
# syntax highlight
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

ACCEPTED_FILE_FORMATS = ["md", "py", "c", "cpp", "pas", "rb", "rs", "pl", "scala", "asm", "v", "txt"]

FORMAT_MAP = {
    "py": {
        "name": "python",
        "comment": "#"
    },
    "c": {
        "name": "c",
        "comment": "//"
    },
    "cpp": {
        "name": "cpp",
        "comment": "//"
    },
    "pas": {
        "name": "pascal",
        "comment": "//"
    },
    "rb": {
        "name": "ruby",
        "comment": "#"
    },
    "rs": {
        "name": "rust",
        "comment": "//"
    },
    "pl": {
        "name": "prolog",
        "comment": "%"
    },
    "scala": {
        "name": "scala",
        "comment": "//"
    },
    "asm": {
        "name": "asm",
        "comment": ";"
    },
    "v": {
        "name": "verilog",
        "comment": "//"
    },
    "txt": {
        "name": "txt",
        "comment": None
    }
}

SOURCE_PATH = sys.argv[1] if len(sys.argv) > 1 else False

# use demo if not defined in config file
if not SOURCE_PATH:
    print("No source provided, building demo site.")
    print("Usage: python3 build.py <path/to/source>")
    SOURCE_PATH = "demo"

ASSETS = ["main.scss", "main.js"]
APP_THEME = "#0E1525"

# check if .md2website-config in source folder root
if os.path.exists(f"{SOURCE_PATH}/.md2website-config"):
    # load into project
    with open(f"{SOURCE_PATH}/.md2website-config", "r") as file:
        config_content = file.read()
        # parse config
        for line in config_content.split("\n"):
            CONFIG_NAME = str(line.split("=")[0].strip())
            if CONFIG_NAME == "DIST_PATH": DIST_PATH = str(line.split("DIST_PATH =")[1].strip()[1:-1])
            if CONFIG_NAME == "LOAD_FOLDER": LOAD_FOLDER = str(line.split("LOAD_FOLDER =")[1].strip()[1:-1]) if not False else False
            if CONFIG_NAME == "LOAD_FOLDER_FLAGS": LOAD_FOLDER_FLAGS = str(line.split("LOAD_FOLDER_FLAGS =")[1].strip()[1:-1]) if not False else False
            if CONFIG_NAME == "AUTHOR": AUTHOR = str(line.split("AUTHOR =")[1].strip())[1:-1]
            if CONFIG_NAME == "DESCRIPTION": DESCRIPTION = str(line.split("DESCRIPTION =")[1].strip()[1:-1])
            if CONFIG_NAME == "GOOGLE_TAG": GOOGLE_TAG = str(line.split("GOOGLE_TAG =")[1].strip()[1:-1]) if not False else False
            if CONFIG_NAME == "APP_NAME": APP_NAME = str(line.split("APP_NAME =")[1].strip()[1:-1])
            if CONFIG_NAME == "POSTS_ON_INDEX": POSTS_ON_INDEX = bool(line.split("POSTS_ON_INDEX =")[1].strip())
            if CONFIG_NAME == "STYLING": STYLING = bool(line.split("STYLING =")[1].strip())
            if CONFIG_NAME == "DEFAULT_THEME": DEFAULT_THEME = str(line.split("DEFAULT_THEME =")[1].strip()[1:-1])
            if CONFIG_NAME == "ALLOW_CHANGE_THEME": ALLOW_CHANGE_THEME = bool(line.split("ALLOW_CHANGE_THEME =")[1].strip())
else: from config_demo import *

# for listing all posts on index page
GLOBAL_POSTS = [] # [ { title, date, url } ]

def write_header(file, title="md2website – Markdown to static website builder", root=0):
    file.write("<!DOCTYPE html>\n")
    file.write("""
    <!--
    ████████████████████████████████████████████████████████████████
    █▄─▀█▀─▄█▄─▄▄▀█▀▄▄▀█▄─█▀▀▀█─▄█▄─▄▄─█▄─▄─▀█─▄▄▄▄█▄─▄█─▄─▄─█▄─▄▄─█
    ██─█▄█─███─██─██▀▄███─█─█─█─███─▄█▀██─▄─▀█▄▄▄▄─██─████─████─▄█▀█
    █▄▄▄█▄▄▄█▄▄▄▄██▄▄▄▄██▄▄▄█▄▄▄██▄▄▄▄▄█▄▄▄▄██▄▄▄▄▄█▄▄▄██▄▄▄██▄▄▄▄▄█
    This static website was built by github.com/mxsjoberg/md2website
    -->
    """.replace("    ", ""))
    file.write(f"<html lang='en' class='styling {DEFAULT_THEME}'>")
    file.write("<head>")
    # favicon
    # file.write("<link rel='icon' href='data:,'>")
    file.write("<link rel='icon' href='/favicon.png'>")
    # title
    file.write(f"<title>{title}</title>")
    # meta
    file.write("<meta charset='utf-8'>")
    file.write("<meta name='viewport' content='width=device-width, initial-scale=1'>")
    file.write(f"<meta name='author' content='{AUTHOR}'>")
    file.write(f"<meta name='description' content='{DESCRIPTION}'>")
    file.write(f"<meta name='theme-color' content='{APP_THEME}'>")
    file.write(f"<meta name='application-name' content='{APP_NAME}'>")
    file.write(f"<meta name='apple-mobile-web-app-title' content='{title}'>")
    file.write("<meta name='apple-mobile-web-app-capable' content='yes'>")
    file.write("<meta name='mobile-web-app-capable' content='yes'>")
    file.write(f"<meta name='apple-mobile-web-app-status-bar-style' content='{APP_THEME}'>")
    # css
    # file.write(f"<link rel='stylesheet' href='{'../'*root}main.min.css'>")
    file.write("<style>")
    css_file = open(f"__assets/main.min.css", "r")
    css_content = css_file.read()
    css_file.close()
    file.write(css_content)
    file.write("</style>")
    # js
    # file.write(f"<script src='{'../'*root}main.min.js'></script>")
    file.write("</head>")
    # -------------------------------------------
    file.write("<body>")
    # google tag
    if GOOGLE_TAG and SOURCE_PATH != "demo": file.write(GOOGLE_TAG)
    # page
    file.write("<div class='page'>")
    # nav
    file.write("<div class='nav no-print'>")
    try:
        nav_file = open(f"{SOURCE_PATH}/nav.md", "r")
        nav_content = nav_file.read()
        nav_file.close()
        if nav_content != "": file.write(markdown.markdown(nav_content))
        else: raise
    except: file.write(f"<p><a href='{'../'*root}index.html'>home</a></p>")
    file.write("</div>")

def write_footer(file):
    file.write("<div id='footer' class='no-print'>")
    # page config
    file.write(f"<p class='small' style='display:flex;justify-content:space-between;'>")
    file.write(f"<a id='styling'>[styling: <span id='styling-on'>on</span><span id='styling-off'>off</span>]</a> ")
    file.write(f"<a id='theme'>[theme: <span id='theme-dark'>dark</span><span id='theme-light'>light</span>]</a> ")
    file.write(f"</p>")
    # credits
    file.write(f"<p class='small' style='text-align:justify;'>© {datetime.now().year} {AUTHOR}. DOM loaded in <span id='dom_time'></span> and page loaded in <span id='load_time'></span>. This static website was built by <a href='https://github.com/mxsjoberg/md2website'>md2website</a> on {datetime.now().strftime('%B %d, %Y')}.</p>")
    file.write("</div>")
    file.write("</div>") # ./page
    # js
    file.write("<script>")
    js_file = open(f"__assets/main.min.js", "r")
    js_content = js_file.read()
    js_file.close()
    file.write(js_content)
    file.write("</script>")
    # end of file
    file.write("</body>")
    file.write("</html>")

# helpers
def sort_by_date_and_title(item):
    return (item["date"], item["title"])

def generate_and_inject_index(file_content):
    # generate anchors
    file_content = re.sub(r"## (.*)", r"## <a name='\1' class='anchor'></a> [\1](#\1)", file_content)
    # find anchors and generate index
    index = []
    for line in file_content.split("\n"):
        if line.startswith("## "):
            index.append("- " + line.split("## ")[1].split("</a>")[1].strip())
        if line.startswith("### "):
            index.append("    - " + line.split("### ")[1].split("</a>")[1].strip())
    if len(index) > 0:
        # inject index as list just before first line starting with ##
        file_content = re.sub(r"## (.*)", f"\n".join([f"{item}" for item in index]) + "\n --- \n" + r"\n## \1", file_content, count=1)
    return file_content

def replace_hr_with_border(file_content, toc=False):
    file_content = re.sub(r"<hr />\n<ul>", r"<ul class='border'>\n" + f"<p class='label'>Page index</p>" if toc else "", file_content)
    file_content = re.sub(r"</ul>\n<hr />", r"</ul>", file_content)
    return file_content

def syntax_highlight(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    code_blocks = soup.find_all("code")
    if code_blocks:
        for code_block in code_blocks:
            try:
                code_content = code_block.get_text()
                code_language = code_block.get('class')[0].split("-")[1]
                lexer = get_lexer_by_name(code_language, stripall=True)
                formatter = HtmlFormatter(linenos=False, cssclass="highlight")
                highlighted_code = highlight(code_content, lexer, formatter)
                code_block.parent.unwrap()
                code_block.replace_with(BeautifulSoup(highlighted_code, "html.parser"))
            except:
                pass
        html_content = str(soup)
    return html_content

def parse_flags(line):
    FLAG_TOC, FLAG_TIME, FLAG_COL, FLAG_SORT, FLAG_DESC = None, None, None, None, None
    if line.startswith("-* "):
        flags_raw = line[3:].split(";")
        for flag in flags_raw:
            key, value = flag.split("=")
            if key == "toc": FLAG_TOC = bool(value)
            if key == "time": FLAG_TIME = bool(value)
            if key == "col": FLAG_COL = int(value)
            if key == "sort": FLAG_SORT = "date" if value == "date" else "name"
            if key == "desc": FLAG_DESC = str(value)
    return FLAG_TOC, FLAG_TIME, FLAG_COL, FLAG_SORT, FLAG_DESC

# create dist folder
if os.path.isdir(DIST_PATH): shutil.rmtree(DIST_PATH)
os.mkdir(DIST_PATH)

# minimize css
with open(f"__assets/main.min.css", "w+") as file:
    css_content = ""
    for css in [asset for asset in ASSETS if asset.split(".")[-1] == "scss"]:
        tmp_file = open(f"__assets/{css}", "r")
        css_content += tmp_file.read()
        tmp_file.close()
    css_content = sass.compile(string=css_content, output_style="compressed")
    file.write(css_content)

# minimize js
with open(f"__assets/main.min.js", "w+") as file:
    js_content = ""
    for js in [asset for asset in ASSETS if asset.split(".")[-1] == "js"]:
        tmp_file = open(f"__assets/{js}", "r")
        js_content += tmp_file.read()
        tmp_file.close()
    js_content = js_content.replace("  ", "")
    js_content = "\n".join([line for line in js_content.split("\n") if not line.startswith("//")])
    js_content = js_content.replace("\n", "")
    js_content = js_content.replace("\t", "")
    # write
    file.write(js_content)

# copy fonts in _fonts folder
os.system(f"cp -r __fonts {DIST_PATH}")

# copy other stuff in source folder
for file in os.listdir(SOURCE_PATH):
    if not file.startswith(".") and not file == "nav.md" and not os.path.isdir(f"{SOURCE_PATH}/{file}"):
        os.system(f"cp {SOURCE_PATH}/{file} {DIST_PATH}/{file}")

# copy load folders into source
if LOAD_FOLDER != False:
    os.system(f"rsync -av --progress {LOAD_FOLDER} {SOURCE_PATH} --exclude .git --exclude='_*'")
    # create file in source folder with flags for loaded folder
    with open(f"{SOURCE_PATH}/{LOAD_FOLDER.split('/')[-1]}/__flags", "w+") as file: file.write(LOAD_FOLDER_FLAGS)

# create list page for each folder in root dir
for dir_ in os.listdir(SOURCE_PATH):
    if "." not in dir_ and dir_ != "pages" and not dir_.startswith("__"):
        FLAG_TOC, FLAG_TIME, FLAG_COL, FLAG_SORT, FLAG_DESC = None, None, None, None, None
        # check if __flags file in dir_
        if os.path.exists(os.path.join(f"{SOURCE_PATH}/{dir_}", "__flags")):
            flag_content = open(f"{SOURCE_PATH}/{dir_}/__flags").read()
            # parse flags
            FLAG_TOC, FLAG_TIME, FLAG_COL, FLAG_SORT, FLAG_DESC = parse_flags(flag_content)
        # create page for folder
        with open(f"{DIST_PATH}/{dir_}.html", "w+") as dir_page:
            write_header(dir_page, title=dir_.title())
            # TODO: refactor this to single data structure and use flags to set ordering? (by date, category, etc)
            posts_lst = [] # [ { title, date, url } ]
            posts_dict = {} # { category: { subcategory: [ { title, date, url } ] } }
            # for each md file in dir_, create html page and append to posts_lst or posts_dict
            for root, dirs, posts in os.walk(f"{SOURCE_PATH}/{dir_}"):
                root = root.replace(f"{SOURCE_PATH}/", "")
                if ".git" not in root and "/_" not in root: os.mkdir(f"{DIST_PATH}/{root}")
                for post in posts if ".git" not in root and "/_" not in root else []:
                    try:
                        if post != "__flags" and post != "README.md" and not post.startswith("_") and post.split(".")[1] in ACCEPTED_FILE_FORMATS:
                            post_file = open(f"{SOURCE_PATH}/{root}/{post}")
                            post_name = post.split(".")[0]
                            post_format = post.split(".")[1]
                            category, subcategory = None, None
                            date = False
                            # title from file name
                            post_title = post_name.replace("-", " ").capitalize()
                            # TODO: refactor this as helper function?
                            # embed file content in markdown code block
                            if post_format in FORMAT_MAP.keys():
                                key = post.split(".")[1]
                                file_content = post_file.read()
                                post_content = f"# {post_title}\n"
                                try:
                                    date = datetime.strptime(file_content.split('\n')[0].split(FORMAT_MAP[key]["comment"])[1].strip(), "%Y-%m")
                                    post_content += f"*{date.strftime('%B %Y')}*\n"
                                    file_content = "\n".join(file_content.split('\n')[1:])
                                except:
                                    pass
                                post_content += f"```{FORMAT_MAP[key]['name']}\n{file_content}\n```\n"
                            else:
                                post_content = post_file.read()
                            # TODO: refactor this as helper function?
                            # create page
                            with open(f"{DIST_PATH}/{root}/{post_name}.html", "w+") as tmp_file:
                                # title
                                try: post_title = post_content.split("\n")[0].split("# ")[1]
                                except: pass
                                # date
                                if not date:
                                    try: date = post_content.split("\n")[2].split("<mark>")[1].split("</mark>")[0]
                                    except:
                                        try: date = post_content.split("\n")[2].split("*")[1]
                                        except: pass
                                # check if date is older than 2 years
                                if date:
                                    try: date_is_outdated = True if datetime.strptime(date, "%B %d, %Y").year + 2 < datetime.now().year else False
                                    except: date_is_outdated = False
                                # categories
                                try: category, subcategory = root.split("/")[1], root.split("/")[2]
                                except:
                                    try: category = root.split("/")[1]
                                    except: pass
                                # category and subcategory
                                if category and subcategory:
                                    try:
                                        if type(date) == type(""): date = datetime.strptime(date, "%B %Y")
                                    except: date = False
                                    if not category in posts_dict: posts_dict[category] = {}
                                    if not subcategory in posts_dict[category]: posts_dict[category][subcategory] = []
                                    # append
                                    posts_dict[category][subcategory].append({ "title": post_title, "date": date, "url": f"{root}/{post_name}" })
                                # category
                                elif category:
                                    try:
                                        if type(date) == type(""): date = datetime.strptime(date, "%B %Y")
                                    except: date = False
                                    if not category in posts_dict: posts_dict[category] = { "_root": [] }
                                    # append
                                    posts_dict[category]["_root"].append({ "title": post_title, "date": date, "url": f"{root}/{post_name}" })
                                else:
                                    try:
                                        if type(date) == type(""): date = datetime.strptime(date, "%B %d, %Y")
                                    except: date = False
                                    # append to posts_lst
                                    posts_lst.append({ "title": post_title, "date": date, "url": f"{root}/{post_name}" })
                                    GLOBAL_POSTS.append({ "title": post_title, "date": date, "url": f"{root}/{post_name}" })
                                # generate anchors and inject index
                                post_content = generate_and_inject_index(post_content)
                                # write
                                write_header(tmp_file, title=post_title)
                                # write outdated notice
                                if date_is_outdated: tmp_file.write(f"<p style='margin-top:0;'><em>This post is more than two years old and may contain outdated information.</em></p>")
                                html_content = markdown.markdown(post_content, extensions=["fenced_code", "tables"])
                                # replace hr with border (for table of contents)
                                html_content = replace_hr_with_border(html_content, toc=True)
                                # syntax highlight
                                html_content = syntax_highlight(html_content)
                                # write to file
                                tmp_file.write(html_content)
                                write_footer(tmp_file)
                                post_file.close()
                    except Exception as error:
                        # print(traceback.format_exc())
                        pass
            # write page title
            dir_page.write(f"<h1>{dir_.title()}</h1>")
            if FLAG_DESC:
                dir_page.write(f"<p>{FLAG_DESC}</p>")
                dir_page.write("<hr>")
            # sort posts_lst by date then by name
            if FLAG_SORT == "date":
                sorted_posts_lst = sorted(posts_lst, key=sort_by_date_and_title, reverse=True)
            else:
                sorted_posts_lst = sorted(posts_lst, key=lambda item: item["title"])
            # write posts_lst (list by date)
            current_date = None
            for post in sorted_posts_lst:
                if post['date'] and current_date != post['date'].year:
                    if current_date != None:
                        dir_page.write("</dl>")
                    dir_page.write(f"<p><em>{post['date'].year}</em></p>")
                    current_date = post['date'].year
                    # columns
                    if FLAG_COL:
                        dir_page.write(f"<ul class='columns' style='column-count:{FLAG_COL};'>")
                    else:
                        dir_page.write("<dl>")
                dir_page.write(f"<li><a href='{post['url']}.html'>{post['title']}</a></li>")
            dir_page.write("</ul>")
            # create list with categories for ordering
            category_list = sorted(posts_dict.keys())
            # write posts in posts_dict (list by category and subcategory)
            for category in category_list:
                # write category
                dir_page.write(f"<h2 id='{category}'>{category.title()}</h2>")
                # if isinstance(posts_dict[category], dict):
                for subcategory in posts_dict[category]:
                    if FLAG_SORT == "date": sorted_posts_dict = sorted(posts_dict[category][subcategory], key=sort_by_date_and_title, reverse=True)
                    else: sorted_posts_dict = sorted(posts_dict[category][subcategory], key=lambda item: item["title"])
                    # subcategory name
                    if subcategory != "_root":
                        dir_page.write(f"<p id='{category.lower()}-{subcategory.replace(' ', '-').lower()}'>{subcategory.replace('-', ' ')}</p>")
                    if FLAG_COL: dir_page.write(f"<ul class='columns' style='column-count:{FLAG_COL};'>")
                    else: dir_page.write("<ul>")
                    for post in sorted_posts_dict:
                        # if date is current or last month
                        if post['date'] and (post['date'].year == datetime.now().year and post['date'].month == datetime.now().month or post['date'].year == datetime.now().year and post['date'].month == datetime.now().month - 1):
                            dir_page.write(f"<li><mark>new</mark> <a href='{post['url']}.html'>{post['title']}</a></li>")
                        else:    
                            dir_page.write(f"<li><a href='{post['url']}.html'>{post['title']}</a></li>")
                    dir_page.write("</ul>")
                # else:
                #     if FLAG_SORT == "date":
                #         sorted_posts_dict = sorted(posts_dict[category], key=sort_by_date_and_title, reverse=True)
                #     else:
                #         sorted_posts_dict = sorted(posts_dict[category], key=lambda item: item["title"])
                #     if FLAG_COL:
                #         dir_page.write(f"<ul class='columns' style='column-count:{FLAG_COL};'>")
                #     else:
                #         dir_page.write("<ul>")
                #     for post in sorted_posts_dict:
                #         # if date is current or last month
                #         if post['date'] and (post['date'].year == datetime.now().year and post['date'].month == datetime.now().month or post['date'].year == datetime.now().year and post['date'].month == datetime.now().month - 1):
                #             dir_page.write(f"<li><mark>new</mark> <a href='{post['url']}.html'>{post['title']}</a></li>")
                #         else:    
                #             dir_page.write(f"<li><a href='{post['url']}.html'>{post['title']}</a></li>")
                #     dir_page.write("</ul>")
            write_footer(dir_page)

# create html page for each md file in pages folder
for root, dirs, files in os.walk(f"{SOURCE_PATH}/pages"):
    for file in files:
        FLAG_TOC, FLAG_TIME, FLAG_COL, FLAG_SORT, FLAG_DESC = None, None, None, None, None
        if file.split(".")[1] == "md":
            file_name = file.split(".")[0]
            # create page
            with open(f"{DIST_PATH}/{file_name}.html", "w+") as tmp_file:
                file = open(f"{root}/{file}", "r")
                file_content = file.read()
                file_content = file_content.split("\n")
                # flags
                if (file_content[0].startswith("-* ")):
                    FLAG_TOC, FLAG_TIME, FLAG_COL, FLAG_SORT, FLAG_DESC = parse_flags(file_content[0])
                    # skip empty line following flags (if any)
                    if (len(file_content[1]) == 0):
                        file_content = file_content[2:]
                    else:
                        file_content = file_content[1:]
                title = file_content[0].split("# ")[1]
                # join 
                file_content = "\n".join(file_content)
                # add updated time
                if FLAG_TIME: file_content = re.sub(r"# (.*)", r"#\1" + f"\n*Updated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*", file_content, count=1)
                # generate anchors and inject index
                if FLAG_TOC: file_content = generate_and_inject_index(file_content)
                # write header
                write_header(tmp_file, title)
                # TODO: move this into formatting helper
                # replace -- with &mdash;
                file_content = re.sub(r" -- (.*)", r" &mdash; \1", file_content)
                # convert markdown to html
                file_content = markdown.markdown(file_content, extensions=["fenced_code", "tables"])
                # replace hr with border (for table of contents)
                file_content = replace_hr_with_border(file_content, toc=True)
                # syntax highlight
                file_content = syntax_highlight(file_content)
                # write to file
                tmp_file.write(file_content)
                # list recent posts on index
                if POSTS_ON_INDEX and file_name == "index":
                    tmp_file.write("<hr>")
                    # list posts
                    if FLAG_SORT == "date":
                        sorted_global_posts = sorted(GLOBAL_POSTS, key=sort_by_date_and_title, reverse=True)
                    else:
                        sorted_global_posts = sorted(GLOBAL_POSTS, key=lambda item: item["title"])
                    tmp_file.write("<dl>")
                    for post in sorted_global_posts: tmp_file.write(f"<li>{datetime.date(post['date'])} &#8212; <a href='posts/{post['url']}.html'>{post['title']}</a></li>")
                    tmp_file.write("</dl>")
                if FLAG_COL: tmp_file.write("</div>")
                write_footer(tmp_file)
                file.close()
