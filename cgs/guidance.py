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
    return render_template('guidance/dashboard.html', user=g.user)