
from app import app, db
from models import User, Post, Comment,UserProfile
from flask import render_template, jsonify, request, redirect, url_for, flash
from flask import flask_login, login_user, current_user, login_required
from flask_mail import Message


@app.route('/')
def index():
    return render_template('landing.html')

if __name__ == '__main__':
    app.run()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()

    # Check if the username is already in use
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({'message': 'Username already in use'}), 400

    # Create a new user with the provided username and password
    new_user = User(username=username)

    # Set the password securely, e.g., using a hashing library like Werkzeug
    new_user.set_password(password)

    new_profile = UserProfile(user=new_user)
    db.session.add(new_profile)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api.login', methiods=['POST'])
def login():
    # Get user login data from the request JSON
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if the user exists in the database
    user = User.query.filter_by(username=username).first()

    if user is None or not user.check_password(password):
        return jsonify({'message': 'Invalid username or password'}), 401

    # If the user exists and the password is correct, create a session (login)
    login_user(user)

    return jsonify({'message': 'Login successful'}), 200

@app.route('/create_post', method=['GET','POST'])
@login_required #requires the user to be logged in

def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title or not content:
            flash('Title and conntent are required','error')

        else:
            new_post = Post(title=title, content=content, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Post created successfully', 'success')
            return redirect(url_for('index'))

    return render_template('create_post.html')

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get(post_id)
    if not post or post.user_id != current_user.id:
        flash('Post not found or unauthorized to edit', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        flash('Post edited successfully', 'success')
        return redirect(url_for('index'))

    return render_template('edit_post.html', post=post)

@app.route('/post/<int:post_id>/comments', methods=['POST'])
@login_required
def create_comment(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post not found'}), 404

    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'message': 'Text is required'}), 400

    new_comment = Comment(text=text, post_id=post_id, user_id=current_user.id)
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({'message': 'Comment posted successfully'}), 201

@app.route('/post/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post not found'}), 404

    comments = Comment.query.filter_by(post_id=post_id).all()
    return jsonify({'comments': [comment.text for comment in comments]})

@app.route('/posts/<int:page>', methods=['GET'])
def list_posts(page=1):
    per_page = 10  # Adjust the number of posts per page as needed
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page, per_page, error_out=False)
    return render_template('posts.html', posts=posts)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        posts = Post.query.filter(Post.title.ilike(f'%{search_query}%') | Post.content.ilike(f'%{search_query}%')).all()
        users = User.query.filter(User.username.ilike(f'%{search_query}%')).all()
        return render_template('search_results.html', posts=posts, users=users)
    return render_template('search.html')

@app.route('/post/<int:post_id>/comments', methods=['POST'])
@login_required
def create_comment(post_id):
    # Existing comment creation code

    # Send email notification to post author
    post_author = post.author
    send_email_notification(post_author.email, 'New Comment Notification', 'A new comment has been posted on your post.')

    return jsonify({'message': 'Comment posted successfully'}), 201

def send_email_notification(to, subject, body):
    msg = Message(subject, recipients=[to], body=body)
    mail.send(msg)