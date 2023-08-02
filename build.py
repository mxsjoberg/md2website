# html static webpage builder

# TODO
#
# - define folders in dict or list to use as "pages" (i.e. posts, etc.), ignore other folders

import os
import markdown

ROOT_DIR = "dist"

def write_header(file, title="Built with Static Webpage Builder", root=0):
    file.write("<html lang='en'>")
    file.write("<head>")
    file.write(f"<title>{title}</title>")
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
            # file.seek(file.tell() - 4, os.SEEK_SET)
            # file.write(" [<a id='invert'>invert</a>]")
            # file.write("</p>")
        else:
            raise
    except:
        file.write(f"<p><a href='{'../'*root}index.html'>Home</a> [<a id='invert'>invert</a>]</p>")
    file.write("</nav>")
    file.write("<div class='page'>")

def write_footer(file):
    file.write("</div>")
    file.write("<div id='footer'>")
    file.write("<p>[<a id='invert'>light|dark</a>]</p>")
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

# posts
with open(f"{ROOT_DIR}/posts.html", "w+") as html_posts:
    write_header(html_posts, title="Posts")
    for root, dirs, posts in os.walk("posts"):
        for post in posts:
            if post.split(".")[1] == "md":
                post_name = post.split(".")[0]
                html_posts.write(F"<p><a href='{post_name}.html'>{post_name}</a></p>")
                # create page
                with open(f"{ROOT_DIR}/{post_name}.html", "w+") as tmp_file:
                    post_file = open(f"{root}/{post}")
                    post_content = post_file.read()
                    title = post_content.split("\n")[0].split("# ")[1]
                    # write
                    write_header(tmp_file, title=title)
                    tmp_file.write(markdown.markdown(post_content, extensions=["fenced_code"]))
                    write_footer(tmp_file)
                    post_file.close()
    write_footer(html_posts)

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

