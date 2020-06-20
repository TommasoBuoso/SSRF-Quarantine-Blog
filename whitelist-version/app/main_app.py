from flask import Flask, render_template, url_for, request, redirect
import urllib.request
from urllib.parse import urlparse

# config
app = Flask(__name__)

# Route for handling the index page
@app.route('/')
@app.route('/home')
def home():
	image_file = url_for('static', filename='images/home.jpg')
	return render_template('index.html', title='Home', image_file=image_file)

# Route for handeling POST request that display the vulnerability to the user
@app.route('/', methods=['POST'])
@app.route('/home', methods=['POST'])
def go_to():
	url = request.form.get('text')		
	parsed_url = urlparse(url)							#create a 6-item named tuple that contains the parse of the url in the form 'scheme://netloc/path;parameters?query#fragment'
	print(parsed_url)
	if 'localhost:80' in parsed_url.netloc:				#whitelist 'localhost:80'
		#if '#' not in parsed_url.netloc:				#blacklist '#'
		return urllib.request.urlopen(url).read()
		#else:
		#	return 'I don\'t like instagram'
	else:
		return '\'My URL is...inevitable\''

# Route for handeling the rendering of the page of the first post of the blog
@app.route('/post1')
def get_post1():
	return render_template('post1.html')

# Route for handeling the rendering of the page of the second post of the blog
@app.route('/post2')
def get_post2():
	return render_template('post2.html')

# start server
if __name__ == '__main__':
	app.run(host = "0.0.0.0", port = 80)