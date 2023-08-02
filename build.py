# html static webpage builder
import os
import markdown

def write_header(file, title="Built with Static Webpage Builder", root=0):
	file.write("<html lang='en'>")
	file.write("<head>")
	file.write(f"<title>{title}</title>")
	file.write(f"<link rel='stylesheet' href='{'../'*root}main.css'>")
	file.write("</head>")
	file.write("<body>")
	file.write(f"<a href='{'../'*root}index.html'>Go back</a>")
	file.write("<div class='page'>")

def write_footer(file):
	file.write("</div>")
	file.write("</body>")
	file.write("</html>")

with open("index.html", "w+") as file:
	# header
	write_header(file, title="Michael Sjöberg")

	# index
	index_file = open("index.md")
	index_content = index_file.read()
	# write
	file.write(markdown.markdown(index_content))
	index_file.close()

	# intro
	# file.write("<h1>Michael Sjöberg</h1>")
	# posts
	with open("posts.html", "w+") as html_posts:
		write_header(html_posts, title="Posts")
		for root, dirs, posts in os.walk("posts"):
			for post in posts:
				if post.split(".")[1] == "md":
					post_name = post.split(".")[0]
					html_posts.write("<p><a href='" + root + "/" + post_name + ".html'>" + post_name + "</a></p>")
					# create page
					with open(f"{root}/{post_name}.html", "w+") as tmp_file:
						post_file = open(f"{root}/{post}")
						post_content = post_file.read()
						title = post_content.split("\n")[0].split("# ")[1]
						# write
						write_header(tmp_file, title=title, root=1)
						tmp_file.write(markdown.markdown(post_content))
						write_footer(tmp_file)
						post_file.close()
		write_footer(html_posts)

	# footer
	write_footer(file)
