from flask import Flask, render_template, redirect, url_for, request, session

# config
app = Flask(__name__)

@app.route('/')
def home():
	return 'Admin backend'

@app.route('/admin')
def get_flag():
	return render_template('admin.html')

# start server
if __name__ == '__main__':
	app.run(host = "0.0.0.0", port = 5001)