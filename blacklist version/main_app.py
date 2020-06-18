from flask import Flask, render_template, redirect, url_for, request, session, flash
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

@app.route('/', methods=['POST'])
@app.route('/home', methods=['POST'])
def go_to():
	url = request.form.get('text')
	parsed_url = urlparse(url)
	if 'localhost' in parsed_url.netloc or '127.0.0.1' in parsed_url.netloc:
		return 'Eheheh I\'ve learned from my mistake!'
	elif 'admin' in parsed_url.path:
		return 'Uhuh try again ;)'
	#debug
	#print(parsed_url.path)
	#print(parsed_url.netloc)
	else:
		return urllib.request.urlopen(url).read()

@app.route('/post1')
def get_post1():
	return render_template('post1.html')

@app.route('/post2')
def get_post2():
	return render_template('post2.html')

# start server
if __name__ == '__main__':
	app.run(debug=True)