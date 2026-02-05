import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from cgs.db import query_all, query_one, execute
from cgs.askLLM import llm


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        regno = request.form['regno']
        name = request.form['name']
        email = request.form['email']
        skills = request.form['skills']
        target_jobs = request.form['target_jobs']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        error = None

        if password != confirm_password:
            error = "Passwords do not match."
        elif query_one('SELECT regno FROM users WHERE regno = %s', (regno,)) is not None:
            error = f"User with Registration Number: {regno} is already registered."

        if error is None:
            llm_output = llm(skills, target_jobs)
            execute(
                'INSERT INTO users (regno, name, email, password, skills, target_jobs, eligible, skills_to_learn, courses, bonus_skills, bonus_skills_courses, roadmap) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (regno, name, email, generate_password_hash(password), skills, target_jobs, ','.join(llm_output[0]), ','.join(llm_output[1]), ','.join(llm_output[2]), ','.join(llm_output[3]), ','.join(llm_output[4]), llm_output[5])
            )

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        regno = request.form['regno']
        password = request.form['password']
        error = None
        user = query_one(
            'SELECT * FROM users WHERE regno = %s', (regno,)
        )

        if user is None:
            error = 'Incorrect Registration Number.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['regno'] = user['regno']
            return redirect(url_for('guidance.dashboard'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    regno = session.get('regno')

    if regno is None:
        g.user = None
    
    else:
        g.user = query_one('SELECT * FROM users WHERE regno = %s', (regno,))
        g.user['skills'] = g.user['skills'].split(',')
        g.user['target_jobs'] = g.user['target_jobs'].split(',')
        g.user['eligible'] = g.user['eligible'].split(',')
        g.user['skills_to_learn'] = g.user['skills_to_learn'].split(',')
        g.user['courses'] = g.user['courses'].split(',')
        g.user['bonus_skills'] = g.user['bonus_skills'].split(',')
        g.user['bonus_skills_courses'] = g.user['bonus_skills_courses'].split(',')
        g.user['roadmap'] = g.user['roadmap'].split('.')
    

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view