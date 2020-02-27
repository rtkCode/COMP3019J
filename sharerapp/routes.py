from flask import render_template, flash, redirect, url_for, session, request, jsonify
from sharerapp import app, db
from sharerapp.models import User, Feed
from sharerapp.form import RssForm, LoginForm, SignupForm, HomeForm, LogoutForm
from werkzeug.security import generate_password_hash, check_password_hash
from sharerapp.rss_analyzer import RSSAnalyzer


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = RssForm()
	logout_form = LogoutForm()
	show_list = False
	rss=""
	count=0
	is_login=False
	user=""

	if session.get("USERNAME"):
		is_login=True
		user=session.get("USERNAME")

	# submit
	if form.submit.data and form.validate_on_submit():
		# print(form.link.data) # test
		show_list=True # if submit show list
		rss = RSSAnalyzer.analyze(form.link.data) # rss json
		count=0
		if rss!={}:
			count = rss["count"] # number of rss passages

	# logout
	if logout_form.logout.data and logout_form.validate_on_submit():
		session.pop("USERNAME")
		return redirect(url_for('index'))

	return render_template('index.html', form=form, show_list=show_list, list=rss, count=count, title="F-RSSReader: a flask based web RSS reader", is_login=is_login, user=user, logout_form=logout_form)


# this login route is learned from class code
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user_in_db = User.query.filter(User.username == form.username.data).first()

		# if no user in database
		if not user_in_db:
			flash('No user found: {}'.format(form.username.data))
			return redirect(url_for('login'))

		# check password
		if (check_password_hash(user_in_db.password_hash, form.password.data)):
			session["USERNAME"] = user_in_db.username
			return redirect(url_for('home'))

		flash('Incorrect Password')
		return redirect(url_for('login'))
	return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
	form = SignupForm()
	if form.validate_on_submit():
		# query database
		email_in_db = User.query.filter(User.email == form.email.data).first()
		user_in_db = User.query.filter(User.username == form.username.data).first() # learned from class code

		# check email in database
		if email_in_db:
			flash('Email {} already exist'.format(form.email.data))
			return redirect(url_for('register'))

		# check username in database
		if user_in_db:
			flash('User {} already exist'.format(form.username.data))
			return redirect(url_for('register'))

		# check two passwords match
		if form.password.data != form.password2.data:
			flash('Passwords do not match!')
			return redirect(url_for('register'))

		# add into database
		passw_hash = generate_password_hash(form.password.data)
		user = User(username=form.username.data, email=form.email.data, password_hash=passw_hash)
		db.session.add(user)
		db.session.commit()

		flash('User registered with username:{}'.format(form.username.data))
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)


@app.route('/home', methods=['GET', 'POST'])
def home():
	if not session.get("USERNAME") is None:

		# logout form & add rss form
		logout_form = LogoutForm()
		form = HomeForm()

		# query user
		user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()

		# logout
		if logout_form.logout.data and logout_form.validate_on_submit():
			session.pop("USERNAME")
			return redirect(url_for('index'))

		# add rss
		if form.add.data and form.validate_on_submit():
			# print(form.add_link.data)
			rss=RSSAnalyzer.analyze(form.add_link.data)

			# add into database
			if rss!={}:
				feed=Feed(title=rss["title"], subtitle=rss["subtitle"], link=rss["link"], feed_link=form.add_link.data, update_time=rss["update"], user_id=user_in_db.id)
				db.session.add(feed)
				db.session.commit()
			return redirect(url_for("home"))

		# read feed list from database
		feeds = Feed.query.filter(Feed.user_id == user_in_db.id).all()
		user = session["USERNAME"]

		return render_template('home.html', title='Home', user=user, form=form, logout_form=logout_form, feed=feeds, feed_count=len(feeds))
	else:
		flash("You needs to login first")
		return redirect(url_for('login'))


@app.route('/checkavailable', methods=['POST'])
def checkavailable():
	# print(request.form)
	# check username
	if request.form["username"]:
		username = request.form["username"]
		user_in_db = User.query.filter(User.username == username).first() # learned from class code
		if not user_in_db:
			return jsonify({"ucode": 0})
		else:
			return jsonify({"ucode": 1})

	# check username
	if request.form["email"]:
		email = request.form["email"]
		email_in_db = User.query.filter(User.email == email).first()
		if not email_in_db:
			return jsonify({"ecode": 0})
		else:
			return jsonify({"ecode": 1})
	else:
		return jsonify({"code": -1})


@app.route('/deletefeed', methods=['POST'])
def deletefeed():
	if request.form["id"]:
		feed_id = request.form["id"]

		# find feed by Id
		the_feed = Feed.query.filter(Feed.id == feed_id).all()

		# delete from database
		db.session.delete(the_feed[0])
		db.session.commit()

		return jsonify({"code": 1})
	else:
		return jsonify({"code": 0})


@app.route('/feeddetail', methods=['POST'])
def feeddetail():
	if request.form["feed_link"]:
		# get link
		feed_link = request.form["feed_link"]
		# analysis link and return data
		data=RSSAnalyzer.analyze(feed_link)
		return jsonify({"code": 1, "data": data})
	else:
		return jsonify({"code": 0})