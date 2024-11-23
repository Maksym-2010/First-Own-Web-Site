import os
from dotenv import load_dotenv
from datetime import datetime
from flask_bootstrap import Bootstrap
from .forms import LoginForm, RegistrationForm, CommentForm
from .models import User, session, Post, Comment, create_db
from flask import render_template, redirect, url_for, flash, request, Flask
from flask_login import current_user, login_user, login_required, logout_user, LoginManager
from werkzeug.security import check_password_hash, generate_password_hash



load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = os.getenv("STM")
Bootstrap(app)


login_manager = LoginManager()
login_manager.init_app(app)

create_db()
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)



@app.context_processor
def injector():
    return {"now": datetime.utcnow()}


@app.route("/")
def home():
    posts = session.query(Post).all()
    return render_template("home.html", posts=posts)






@app.route("/read_post_detail/<int:id>")
def read_post(id):
    post = session.query(Post).get(id)
    return render_template("post_detail.html", post=post)




@app.route("/create_post", methods=["POST", "GET"])
def create_post():
    if request.method == "POST":
        content = request.form["Content"]
        title = request.form["Title"]

        new_post = Post(
            title=title,
            content=content
        )

        try:
            session.add(new_post)
            session.commit()
            return redirect("/index")
        except Exception as exc:
            return f"При збереженні поста виникла помилка: {exc}"
    else:
        return render_template("create_post.html")




@app.route("/update_post/<int:id>", methods=["GET", "POST"])
def update_post(id):
    post = session.query(Post).get(id)
    if request.method == "POST":
        content = request.form["content"]
        title = request.form["title"]
        if title or content:
            try:
                post.title = title
                post.content = content
                session.commit()
                return redirect("/index")
            except Exception as exc:
                return f"При оновленні поста виникла помилка: {exc}"
            finally:
                session.close()
        else:
            return "Оновіть поля, оскільки Ви їх не змінювали."
    else:
        return render_template("update_post.html", post=post)




@app.route("/delete_post/<int:id>")
def delete_post(id):
    try:
        post = session.query(Post).get(id)
   
        if post is None:
            return f"Пост з ID {id} не знайдено.", 404
        session.query(Comment).filter_by(post_id=post.id).delete()
        session.delete(post)
       
        session.commit()
        return redirect("/index")

    except Exception as exc:
        session.rollback()
        return f"При видаленні поста виникла помилка: {exc}", 500

    finally:
        session.close()




@app.route("/index")
def index():
    all_posts = session.query(Post).all()
    posts_with_comments = []
    for post in all_posts:
        comments = session.query(Comment).filter_by(post_id=post.id).all()
        posts_with_comments.append({
            "post": post,
            "comments": comments
        })

    return render_template("index.html", posts_with_comments=posts_with_comments)




@app.route("/register", methods=["POST", "GET"])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        user = session.query(User).filter_by(email=email).first()
        if user:
            flash(f"Юзер з поштою {email} вже існує.<br> <a href={url_for('log_in')}>Log in</a>", "error")
            return redirect(url_for("registration"))
        new_user = User(
            name=form.name.data,
            email=email,
            password=generate_password_hash(form.password.data),
            phone=form.phone.data
        )

        try:
            session.add(new_user)
            session.commit()
            flash("Дякую за реєстрацію! Тепер Ви маєте змогу увійти до свого аккаунту!", "success")
            return redirect(url_for("log_in"))
        except Exception as exc:
            raise exc
        finally:
            session.close()
    return render_template("register.html", form=form)



@app.route("/login", methods=["GET", "POST"])
def log_in():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = session.query(User).filter_by(email=email).first()
        if not user:
            flash(f"Юзера з поштою {email} не існує.<br> <a href={url_for('registration')}>Register</a>", "error")
            return redirect(url_for("log_in"))
        elif check_password_hash(user.password, form.password.data):
            login_user(user=user)
            return redirect(url_for("index"))
        else:
            flash("Пароль, або Email не вірні. ", "error")
            return redirect(url_for("log_in"))
    else:
        return render_template("login.html", form=form)
    



@app.route("/create_comment/<int:id>", methods=["GET", "POST"])
def create_com(id):
    post = session.query(Post).get(id)
    
    if not post:
        return "Пост не знайдено", 404

    comments = session.query(Comment).filter_by(post_id=post.id).all()
    if request.method == "POST":
        content = request.form["content"]

        # Перевірка, чи введено контент
        if not content:
            return "Поле контенту не може бути порожнім", 400

        new_comment = Comment(
            comment=content, 
            post_id=post.id,
            user_id=current_user.id 
        )

        try:
            session.add(new_comment)
            session.commit()
            return redirect(url_for('index'))
        except Exception as exc:
            session.rollback() 
            return f"При збереженні коментаря виникла помилка: {exc}"
        finally:
            session.close() 
    else:
        return render_template("create_comment.html", post=post, comments=comments)
    



@app.route("/logout")
@login_required
def log_out():
    logout_user()
    return redirect(url_for("home"))