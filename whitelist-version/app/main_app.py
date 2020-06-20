from flask import Flask, render_template, url_for, request, redirect
import urllib.request

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
	if 'localhost:80' in url:				#whitelist 'localhost:80'
		return urllib.request.urlopen(url).read()
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

#http://localhost:5001/admin#localhost:80