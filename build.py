# md2website: markdown to static website builder

import os
import re
import shutil
import markdown
from datetime import datetime
# syntax highlight
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

DIST_PATH = "../michaelsjoberg.com/dist"
ASSETS = ["main.css", "main.js", "Hack-Bold.ttf", "Hack-Regular.ttf", "resume.pdf"]
AUTHOR = "Michael Sjöberg"
DESCRIPTION = "I write about programming, projects, and finance."
APP_NAME = "Michael's Page"
APP_THEME = "#161716"
POSTS_ON_INDEX = False
NO_JS = False

# for listing all posts on index page
GLOBAL_POSTS = [] # [ { title, date, url } ]

def sort_by_date_and_title(item):
    return (item["date"], item["title"])

def write_header(file, title="This static website was built using md2website", root=0):
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
    file.write("<html lang='en'>")
    file.write("<head>")
    # favicon
    file.write("<link rel='icon' href='data:,'>")
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
    css_file = open(f"{DIST_PATH}/main.min.css", "r")
    css_content = css_file.read()
    css_file.close()
    file.write(css_content)
    file.write("</style>")
    # js
    # file.write(f"<script src='{'../'*root}main.min.js'></script>")
    file.write("</head>")
    # -------------------------------------------
    file.write("<body>")
    file.write("<div class='page'>")
    # nav
    file.write("<div class='nav no-print'>")
    try:
        nav_file = open("nav.md", "r")
        nav_content = nav_file.read()
        nav_file.close()
        if nav_content != "":
            file.write(markdown.markdown(nav_content))
        else:
            raise
    except:
        file.write(f"<p><a href='{'../'*root}index.html'>home</a></p>")
    file.write("</div>")

def write_footer(file):
    file.write("<div id='footer' class='no-print'>")
    file.write(f"<p class='small'>Page config: <a id='theme'>dark</a> <a id='styling'>styling</a>. This static website was built using <a href='https://github.com/mxsjoberg/md2website'>md2website</a> on {datetime.now().strftime('%B %d, %Y')}. DOM loaded in <span id='dom_time'></span> and page loaded in <span id='load_time'></span>.</p>")
    file.write("</div>")
    file.write("</div>") # ./page
    # is NO_JS useful at all?
    if not NO_JS:
        file.write("<script>")
        js_file = open(f"{DIST_PATH}/main.min.js", "r")
        js_content = js_file.read()
        js_file.close()
        file.write(js_content)
        file.write("</script>")
    file.write("</body>")
    file.write("</html>")

# helpers
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
        file_content = re.sub(r"## (.*)", f"<span class='no-print'>\n".join([f"{item}" for item in index]) + "\n --- \n</span>" + r"\n## \1", file_content, count=1)
    return file_content

def parse_flags(line):
    FLAG_TOC = None
    FLAG_TIME = None
    FLAG_COL = None
    FLAG_DESC = None
    if line.startswith("-* "):
        flags_raw = line[3:].split(";")
        for flag in flags_raw:
            key, value = flag.split("=")
            if key == "toc": FLAG_TOC = bool(value)
            if key == "time": FLAG_TIME = bool(value)
            if key == "col": FLAG_COL = int(value)
            if key == "desc": FLAG_DESC = str(value)
    return FLAG_TOC, FLAG_TIME, FLAG_COL, FLAG_DESC

# create dist folder
if os.path.isdir(DIST_PATH): shutil.rmtree(DIST_PATH)
os.mkdir(DIST_PATH)

# minimize css
with open(f"{DIST_PATH}/main.min.css", "w+") as file:
    css_content = ""
    for css in [asset for asset in ASSETS if asset.split(".")[-1] == "css"]:
        tmp_file = open(css, "r")
        css_content += tmp_file.read()
        tmp_file.close()
    css_content = css_content.replace("\n", "")
    css_content = css_content.replace("\t", "")
    css_content = css_content.replace("  ", "")
    file.write(css_content)

# minimize js
with open(f"{DIST_PATH}/main.min.js", "w+") as file:
    js_content = ""
    for js in [asset for asset in ASSETS if asset.split(".")[-1] == "js"]:
        tmp_file = open(js, "r")
        js_content += tmp_file.read()
        tmp_file.close()
    js_content = js_content.replace("  ", "")
    js_content = "\n".join([line for line in js_content.split("\n") if not line.startswith("//")])
    js_content = js_content.replace("\n", "")
    js_content = js_content.replace("\t", "")
    # write
    file.write(js_content)

# copy non-css and non-js assets
for asset in [asset for asset in ASSETS if asset.split(".")[-1] not in ["css", "js"]]:
    os.system(f"cp {asset} {DIST_PATH}/{asset}")

# create list page for each folder in root dir
for dir_ in os.listdir("."):
    if "." not in dir_ and dir_ != "pages":
        FLAG_TOC = None
        FLAG_TIME = None
        FLAG_COL = None
        FLAG_DESC = None
        # check if __flags file in dir_
        if os.path.exists(os.path.join(dir_, "__flags")):
            flag_content = open(f"{dir_}/__flags").read()
            # parse flags
            FLAG_TOC, FLAG_TIME, FLAG_COL, FLAG_DESC = parse_flags(flag_content)
        # create page for folder
        with open(f"{DIST_PATH}/{dir_}.html", "w+") as dir_page:
            write_header(dir_page, title=dir_.title())
            posts_lst = [] # [ { title, date, url } ]
            posts_dict = {} # { category: { subcategory: [ { title, date, url } ] } }
            # for each md file in dir_, create html page and append to posts_lst or posts_dict
            for root, dirs, posts in os.walk(dir_):
                os.mkdir(f"{DIST_PATH}/{root}")
                for post in posts:
                    if post != "__flags" and post.split(".")[1] == "md":
                        post_name = post.split(".")[0]
                        # create page
                        with open(f"{DIST_PATH}/{root}/{post_name}.html", "w+") as tmp_file:
                            post_file = open(f"{root}/{post}")
                            post_content = post_file.read()
                            # title
                            title = post_content.split("\n")[0].split("# ")[1]
                            # date
                            try:
                                date = post_content.split("\n")[2].split("<mark>")[1].split("</mark>")[0]
                            except:
                                date = post_content.split("\n")[2].split("*")[1]
                            # check if date is older than 2 years
                            try:
                                date_is_outdated = True if datetime.strptime(date, "%B %d, %Y").year + 2 < datetime.now().year else False
                            except:
                                date_is_outdated = False
                            # categories
                            category, subcategory = None, None
                            try:
                                category, subcategory = root.split("/")[1], root.split("/")[2]
                            except:
                                try: category = root.split("/")[1]
                                except: pass
                            # category and subcategory
                            if category and subcategory:
                                if not category in posts_dict: posts_dict[category] = {}
                                if not subcategory in posts_dict[category]: posts_dict[category][subcategory] = []
                                # append
                                posts_dict[category][subcategory].append({ "title": title, "date": datetime.strptime(date, "%B %Y"), "url": post_name })
                            # category
                            elif category:
                                if not category in posts_dict: posts_dict[category] = []
                                # append
                                posts_dict[category].append({ "title": title, "date": datetime.strptime(date, "%B %Y"), "url": post_name })
                            else:
                                # append to posts_lst
                                posts_lst.append({ "title": title, "date": datetime.strptime(date, "%B %d, %Y"), "url": post_name })
                                GLOBAL_POSTS.append({ "title": title, "date": datetime.strptime(date, "%B %d, %Y"), "url": post_name })
                            # generate anchors and inject index
                            post_content = generate_and_inject_index(post_content)
                            # write
                            write_header(tmp_file, title=title)
                            # write outdated notice
                            if date_is_outdated: tmp_file.write(f"*This post is more than two years old and may contain outdated information*")
                            html_content = markdown.markdown(post_content, extensions=["fenced_code", "tables"])
                            # syntax highlight
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
                            tmp_file.write(html_content)
                            write_footer(tmp_file)
                            post_file.close()            
            # write page title
            dir_page.write(f"<h1>{dir_.title()}</h1>")
            if FLAG_DESC:
                dir_page.write(f"<p>{FLAG_DESC}</p>")
                dir_page.write("<hr>")
            # sort posts_lst by date then by name
            sorted_posts_lst = sorted(posts_lst, key=sort_by_date_and_title, reverse=True)
            # write posts_lst (list by date)
            current_date = None
            for post in sorted_posts_lst:
                if current_date != post['date'].year:
                    if current_date != None:
                        dir_page.write("</dl>")
                    dir_page.write(f"<p><em>{post['date'].year}</em></p>")
                    current_date = post['date'].year
                    # columns
                    if FLAG_COL:
                        dir_page.write(f"<ul style='column-count:{FLAG_COL};'>")
                    else:
                        dir_page.write("<dl>")
                # dir_page.write(f"<li>{datetime.date(post['date'])} &#8212; <a href='posts/{post['url']}.html'>{post['title']}</a></li>")
                dir_page.write(f"<li><a href='posts/{post['url']}.html'>{post['title']}</a></li>")
                # tmp_file.write("<dl>")
                # for post in sorted_global_posts:
                #     # TODO: posts/ hardcoded is ugly hack, fix later
                #     tmp_file.write(f"<li>{datetime.date(post['date'])} &#8212; <a href='posts/{post['url']}.html'>{post['title']}</a></li>")
                # tmp_file.write("</dl>")
            dir_page.write("</ul>")
            # create list with categories for ordering
            category_list = sorted(posts_dict.keys())
            # write posts in posts_dict (list by category and subcategory)
            for category in category_list:
                # write category
                dir_page.write(f"<h2 id='{category}'>{category.title()}</h2>")
                if isinstance(posts_dict[category], dict):
                    for subcategory in posts_dict[category]:
                        sorted_posts_dict = sorted(posts_dict[category][subcategory], key=sort_by_date_and_title, reverse=True)
                        # subcategory name
                        if len(posts_dict[category].keys()) > 1:
                            dir_page.write(f"<p id='{category}-{subcategory.replace(' ', '-')}'>{subcategory.title() if not subcategory == subcategory.upper() else subcategory}</p>")
                        if FLAG_COL:
                            dir_page.write(f"<ul style='column-count:{FLAG_COL};column-gap:2rem;'>")
                        else:
                            dir_page.write("<ul>")
                        for post in sorted_posts_dict:
                            # if date is current or last month
                            if post['date'].year == datetime.now().year and post['date'].month == datetime.now().month or post['date'].year == datetime.now().year and post['date'].month == datetime.now().month - 1:
                                dir_page.write(f"<li><mark>new</mark> <a href='{dir_}/{category}/{subcategory}/{post['url']}.html'>{post['title']}</a></li>")
                            else:    
                                dir_page.write(f"<li><a href='{dir_}/{category}/{subcategory}/{post['url']}.html'>{post['title']}</a></li>")
                        dir_page.write("</ul>")
                else:
                    sorted_posts_dict = sorted(posts_dict[category], key=sort_by_date_and_title, reverse=True)
                    if FLAG_COL:
                        dir_page.write(f"<ul style='column-count:{FLAG_COL};'>")
                    else:
                        dir_page.write("<ul>")
                    for post in sorted_posts_dict:
                        # if date is current or last month
                        if post['date'].year == datetime.now().year and post['date'].month == datetime.now().month or post['date'].year == datetime.now().year and post['date'].month == datetime.now().month - 1:
                            dir_page.write(f"<li><mark>new</mark> <a href='{dir_}/{category}/{post['url']}.html'>{post['title']}</a></li>")
                        else:    
                            dir_page.write(f"<li><a href='{dir_}/{category}/{post['url']}.html'>{post['title']}</a></li>")
                    dir_page.write("</ul>")
            write_footer(dir_page)

# create html page for each md file in pages folder
for root, dirs, files in os.walk("pages"):
    for file in files:
        FLAG_TOC = None
        FLAG_TIME = None
        FLAG_COL = None
        FLAG_DESC = None
        if file.split(".")[1] == "md":
            file_name = file.split(".")[0]
            # create page
            with open(f"{DIST_PATH}/{file_name}.html", "w+") as tmp_file:
                file = open(f"{root}/{file}", "r")
                file_content = file.read()
                file_content = file_content.split("\n")
                # flags
                if (file_content[0].startswith("-* ")):
                    # parse flags
                    FLAG_TOC, FLAG_TIME, FLAG_COL, FLAG_DESC = parse_flags(file_content[0])
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
                # TODO: fix for multi columns on regular pages? below title
                # columns
                # if FLAG_COL:
                #     tmp_file.write(f"<div style='column-count:{FLAG_COL};'>")
                # if FLAG_COL:
                #     print(file_name, "OK")
                #     file_content = re.sub(r"---", f"\n<div style='column-count:{FLAG_COL};'>" + r"\n", file_content, count=1)
                # replace -- with &mdash;
                file_content = re.sub(r" -- (.*)", r" &mdash; \1", file_content)
                tmp_file.write(markdown.markdown(file_content, extensions=["fenced_code", "tables"]))
                # list recent posts on index
                if POSTS_ON_INDEX and file_name == "index":
                    tmp_file.write("<hr>")
                    # list posts
                    sorted_global_posts = sorted(GLOBAL_POSTS, key=sort_by_date_and_title, reverse=True)
                    tmp_file.write("<dl>")
                    for post in sorted_global_posts:
                        # TODO: posts/ hardcoded is ugly hack, fix later
                        tmp_file.write(f"<li>{datetime.date(post['date'])} &#8212; <a href='posts/{post['url']}.html'>{post['title']}</a></li>")
                    tmp_file.write("</dl>")
                if FLAG_COL: tmp_file.write("</div>")
                write_footer(tmp_file)
                file.close()


