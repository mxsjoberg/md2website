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
	file.write("<div class='page'>")

def write_footer(file):
	file.write("</div>")
	file.write("</body>")
	file.write("</html>")

with open("index.html", "w+") as file:
	# header
	write_header(file)
	
	# intro
	file.write("<h1>Hello Static Webpage!</h1>")
	# posts
	for root, dirs, posts in os.walk("posts"):
		for post in posts:
			if post.split(".")[1] == "md":
				post_name = post.split(".")[0]
				file.write("<p><a href='" + root + "/" + post_name + ".html'>" + post_name + "</a></p>")
				# create page
				with open(f"{root}/{post_name}.html", "w+") as tmp_file:
					post_file = open(f"{root}/{post}")
					post_content = post_file.read()
					write_header(tmp_file, root=1)
					tmp_file.write(markdown.markdown(post_content))
					write_footer(tmp_file)
					post_file.close()

	# footer
	write_footer(file)
