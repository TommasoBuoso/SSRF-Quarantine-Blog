from flask import Flask, render_template, url_for, request
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
	return urllib.request.urlopen(url).read()

# Route for handeling the rendering of the page of the post of the blog
@app.route('/post1')
def get_post1():
	return render_template('post1.html', title='Post 1')

# Route for handeling the rendering of the page of the post of the blog
@app.route('/post2')
def get_post2():
	f1 = url_for('static', filename='images/funny/f1.jpeg')
	f2 = url_for('static', filename='images/funny/f2.jpeg')
	f3 = url_for('static', filename='images/funny/f3.jpeg')
	f4 = url_for('static', filename='images/funny/f4.jpeg')
	f5 = url_for('static', filename='images/funny/f5.jpeg')
	f6 = url_for('static', filename='images/funny/f6.jpeg')
	f7 = url_for('static', filename='images/funny/f7.jpeg')
	return render_template('post2.html', title='Post 2', f1=f1,f2=f2,f3=f3,f4=f4,f5=f5,f6=f6,f7=f7)

# Route for handeling the rendering of the page of the post of the blog
@app.route('/post3')
def get_post3():
	return render_template('post3.html', title='Post 3')

# Route for handeling the rendering of the page of the post of the blog
@app.route('/post4')
def get_post4():
	return render_template('post4.html', title='Post 4')

# start server
if __name__ == '__main__':
	app.run(host = "0.0.0.0", port = 80)