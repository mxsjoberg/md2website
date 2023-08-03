# html static webpage builder

import os
import markdown
from datetime import datetime

ROOT_DIR = "dist"

def sort_by_date_and_title(item):
    return (item["date"], item["title"])

def write_header(file, title="Built with Static Webpage Builder", root=0):
    file.write("<html lang='en'>")
    file.write("<head>")
    # favicon
    file.write("<link rel='icon' href='fav.png'>")
    # title
    file.write(f"<title>{title}</title>")
    # meta
    file.write("<meta charset='utf-8'>")
    file.write("<meta name='viewport' content='width=device-width, initial-scale=1'>")
    file.write("<meta name='author' content='Michael Sjöberg'>")
    file.write("<meta name='description' content='My projects, posts, and programming notes.'>")
    file.write("<meta name='theme-color' content='#161716'>")
    file.write("<meta name='application-name' content='Michael Sjöberg'>")
    file.write("<meta name='apple-mobile-web-app-title' content='Michael Sjöberg'>")
    file.write("<meta name='apple-mobile-web-app-capable' content='yes'>")
    file.write("<meta name='mobile-web-app-capable' content='yes'>")
    file.write("<meta name='apple-mobile-web-app-status-bar-style' content='#161716'>")
    # css
    file.write(f"<link rel='stylesheet' href='{'../'*root}main.min.css'>")
    # js
    file.write(f"<script src='{'../'*root}main.min.js'></script>")
    file.write("</head>")
    file.write("<body>")
    # fixed nav
    file.write("<nav>")
    try:
        nav_file = open("nav.md")
        nav_content = nav_file.read()
        if nav_content != "":
            file.write(markdown.markdown(nav_content))
        else:
            raise
    except:
        file.write(f"<p><a href='{'../'*root}index.html'>Home</a> [<a id='invert'>invert</a>]</p>")
    file.write("</nav>")
    file.write("<div class='page'>")

def write_footer(file):
    file.write("</div>")
    file.write("<div id='footer'>")
    file.write("<p>[<a id='invert'>light|dark</a>] [<a href='https://github.com/mixmaester/html_builder'>source</a>]</p>")
    file.write(f"<p><span class='small'>DOM loaded in <span id='dom_time'></span>, page loaded in <span id='load_time'></span></span></p>")
    file.write("</div>")
    file.write("</body>")
    file.write("</html>")

# create or clear dist folder
if os.path.isdir(ROOT_DIR):
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            os.remove(f"{root}/{file}")
        for dir in dirs:
            os.rmdir(f"{root}/{dir}")
else:
    os.mkdir(ROOT_DIR)

# index
with open(f"{ROOT_DIR}/index.html", "w+") as file:
    index_file = open("index.md")
    index_content = index_file.read()
    title = index_content.split("\n")[0].split("# ")[1]
    write_header(file, title)
    file.write(markdown.markdown(index_content))
    index_file.close()
    write_footer(file)

# courses
with open(f"{ROOT_DIR}/courses.html", "w+") as file:
    courses_file = open("courses.md")
    courses_content = courses_file.read()
    title = courses_content.split("\n")[0].split("# ")[1]
    write_header(file, title)
    file.write(markdown.markdown(courses_content))
    courses_file.close()
    write_footer(file)

# projects
with open(f"{ROOT_DIR}/projects.html", "w+") as file:
    projects_file = open("projects.md")
    projects_content = projects_file.read()
    title = projects_content.split("\n")[0].split("# ")[1]
    write_header(file, title)
    file.write(markdown.markdown(projects_content))
    projects_file.close()
    write_footer(file)

# posts
with open(f"{ROOT_DIR}/posts.html", "w+") as html_posts:
    write_header(html_posts, title="Posts")
    posts_lst = []
    for root, dirs, posts in os.walk("posts"):
        for post in posts:
            if post.split(".")[1] == "md":
                post_name = post.split(".")[0]
                # create page
                with open(f"{ROOT_DIR}/{post_name}.html", "w+") as tmp_file:
                    post_file = open(f"{root}/{post}")
                    post_content = post_file.read()
                    # title (first line)
                    title = post_content.split("\n")[0].split("# ")[1]
                    # date (third line)
                    date = post_content.split("\n")[2].split("*")[1]
                    # append to posts_lst
                    posts_lst.append({ "title": title, "date": datetime.strptime(date, "%B %Y"), "url": post_name })
                    # write
                    write_header(tmp_file, title=title)
                    tmp_file.write(markdown.markdown(post_content, extensions=["fenced_code", "tables"]))
                    write_footer(tmp_file)
                    post_file.close()
    # sort posts_lst by date then by name
    sorted_posts_lst = sorted(posts_lst, key=sort_by_date_and_title, reverse=True)
    # write posts
    current_date = None
    for post in sorted_posts_lst:
        if current_date != post['date'].year:
            if current_date != None:
                html_posts.write("</ul>")
            html_posts.write(f"<h1>{post['date'].year}</h1>")
            current_date = post['date'].year
            html_posts.write("<ul>")
        html_posts.write(f"<li><a href='{post['url']}.html'>{post['title']}</a></li>")
    write_footer(html_posts)

# programming
with open(f"{ROOT_DIR}/programming.html", "w+") as html_programming:
    write_header(html_programming, title="Programming")
    programming_dict = {}
    for root, dirs, posts in os.walk("programming"):
        for post in posts:
            if post.split(".")[1] == "md":
                post_name = post.split(".")[0]
                # create page
                with open(f"{ROOT_DIR}/{post_name}.html", "w+") as tmp_file:
                    post_file = open(f"{root}/{post}")
                    post_content = post_file.read()
                    # title (first line)
                    title = post_content.split("\n")[0].split("# ")[1]
                    # date (third line)
                    date = post_content.split("\n")[2].split("*")[1]
                    # meta
                    language = None
                    category = None
                    try:
                        language = post_content.split("\n")[2].split("*")[2].strip().split(" ", 1)[0].split("]")[0][1:].lower()
                        category = post_content.split("\n")[2].split("*")[2].strip().split(" ", 1)[1].split("]")[0][1:].lower()
                    except:
                        pass
                    if language and category:
                        if not language in programming_dict:
                            programming_dict[language] = {}
                        if not category in programming_dict[language]:
                            programming_dict[language][category] = []
                        programming_dict[language][category].append({ "title": title, "date": datetime.strptime(date, "%B %Y"), "url": post_name })
                    else:
                        pass
                    # write
                    write_header(tmp_file, title=title)
                    tmp_file.write(markdown.markdown(post_content, extensions=["fenced_code", "tables"]))
                    write_footer(tmp_file)
                    post_file.close()

    # write programming
    for language in programming_dict:
        html_programming.write(f"<h1 id='{language}'>{language.title()}</h1>")
        for category in programming_dict[language]:
            html_programming.write(f"<p id='{category}'>{category.title()}</p>")
            sorted_posts_lst = sorted(programming_dict[language][category], key=sort_by_date_and_title, reverse=True)
            html_programming.write("<ul>")
            for post in sorted_posts_lst:
                html_programming.write(f"<li><a href='{post['url']}.html'>{post['title']}</a></li>")
            html_programming.write("</ul>")
    write_footer(html_programming)

# minimize css
with open(f"{ROOT_DIR}/main.min.css", "w+") as file:
    css_file = open("main.css")
    css_content = css_file.read()
    css_content = css_content.replace("\n", "")
    css_content = css_content.replace("\t", "")
    css_content = css_content.replace("  ", "")
    file.write(css_content)
    css_file.close()

# minimize js
with open(f"{ROOT_DIR}/main.min.js", "w+") as file:
    js_file = open("main.js")
    js_content = js_file.read()
    # remove line comments
    js_content = js_content.replace("  ", "")
    js_content = "\n".join([line for line in js_content.split("\n") if not line.startswith("//")])
    js_content = js_content.replace("\n", "")
    js_content = js_content.replace("\t", "")
    file.write(js_content)
    js_file.close()

# copy fav.png to dist/fav.png
os.system("cp fav.png dist/fav.png")
