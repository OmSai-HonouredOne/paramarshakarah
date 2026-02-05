import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from cgs.db import query_all, query_one, execute
from cgs.auth import login_required
from cgs.askLLM import llm

bp = Blueprint('guidance', __name__)

@bp.route('/')
def index():
    return render_template('guidance/index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    print(g.user['roadmap'])
    return render_template('guidance/dashboard.html', user=g.user)

@bp.route('/dashboard/edit', methods=('GET', 'POST'))
@login_required
def edit_profile():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        skills = request.form['skills']
        target_jobs = request.form['target_jobs']
        error = None

        if error is None:
            if target_jobs==','.join(g.user['target_jobs']) and skills==','.join(g.user['skills']):
                execute(
                    'UPDATE users SET name = %s, email = %s WHERE regno = %s',
                    (name, email, g.user['regno'])
                )
            else:
                llm_output = llm(skills, target_jobs)
                execute(
                    'UPDATE users SET name = %s, email = %s, skills = %s, target_jobs = %s, eligible = %s, skills_to_learn = %s, courses = %s, bonus_skills = %s, bonus_skills_courses = %s, roadmap = %s WHERE regno = %s',
                    (name, email, skills, target_jobs, ','.join(llm_output[0]), ','.join(llm_output[1]), ','.join(llm_output[2]), ','.join(llm_output[3]), ','.join(llm_output[4]), llm_output[5], g.user['regno'])
                )
            return redirect(url_for('guidance.dashboard'))

        flash(error)


    return render_template('guidance/edit.html', user=g.user)


@bp.route('/coverletter')
def coverletter():
    return render_template('guidance/coverletter.html',user=g.user)
