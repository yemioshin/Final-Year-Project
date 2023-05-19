from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, abort
from flask_login import login_required
from .models import User, Project, Task
from .forms import (ProjectForm, TaskForm, TaskCompleteForm,)
from .functions import *
import json

views = Blueprint('views', __name__)

error_msg_403 = 'Access denied: You do not have access to this project'

@views.route('/')
@login_required
def home():
    return render_template("dashboard.html", user=get_current_user())

@views.route('/projects')
@login_required
def view_projects():
    jobs = get_user_projects(get_current_user().id)
    return render_template('projects.html', jobs=jobs)

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=get_current_user())

@views.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        add_project_to_db(form)
        flash('Congratulations, you created a Project')
        return redirect(url_for('views.view_projects'))
    return render_template('forms/add_project.html', title="Create Project", form=form)

@views.route('/project/<projectno>')
@login_required
def view_project_tasks(projectno):
    form = TaskCompleteForm()
    tasks = get_project_tasks(projectno)
    job = get_project_by_id(projectno)
    if job.user_id == get_current_user().id:
        return render_template('project_tasks.html', tasks=tasks, job=job, form=form)
    else:
        flash(error_msg_403)
        abort(403)

@views.route('/project/<int:projectno>/edit_project', methods=['GET', 'POST'])
@login_required
def edit_project(projectno):
    job = get_project_by_id(projectno)
    if job.user_id != get_current_user().id:
        flash(error_msg_403)
        abort(403)
    form = ProjectForm()
    if form.validate_on_submit():
        edit_project_in_db(form, projectno)
        flash('Your project has been updated!')
        return redirect(url_for('views.view_project_tasks', projectno=projectno))
    elif request.method == 'GET':
        form.number.data = job.number
        form.name.data = job.name
        form.time.data = job.time
        form.subject.data = job.subject
    return render_template('forms/add_project.html', title="Edit Project", form=form)

@views.route('/project/<int:projectno>/delete_project', methods=['GET', 'POST'])
@login_required
def delete_project(projectno):
    job = get_project_by_id(projectno)
    if job.user_id != get_current_user().id:
        flash(error_msg_403)
        abort(403)
    delete_project_from_db(projectno)
    flash('Project successfully deleted')
    return redirect(url_for('views.view_projects'))


@views.route('/project/<int:projectno>/add_task', methods=['GET', 'POST'])
@login_required
def add_task(projectno):
    form = TaskForm()
    if form.validate_on_submit():
        add_task_to_db(form, projectno)
        flash('Congratulations, you created a Task')
        return redirect(url_for('views.view_project_tasks', projectno=projectno))

    elif request.method == "GET":
        job = get_project_by_id(projectno)
        if job.user_id == get_current_user().id:
            return render_template(
                'forms/add_task.html',
                title='Create Task', form=form)
        else:
            flash(error_msg_403)
            abort(403)


@views.route('/project/<projectno>/delete_task/<int:task_id>')
def delete_task(task_id, projectno):
    job = get_project_by_id(projectno)
    if job.user_id == get_current_user().id:
        delete_task_from_db(task_id)
        return redirect(url_for('views.view_project_tasks', projectno=projectno))
    else:
        flash(error_msg_403)
        abort(403)


@views.route(
    '/project/<int:projectno>/edit_task/<int:task_id>',
    methods=['GET', 'POST'])
def edit_task(task_id, projectno):
    job = get_project_by_id(projectno)

    if job.user_id != get_current_user().id:
        flash(error_msg_403)
        abort(403)
    form = TaskForm()
    if form.validate_on_submit():
        edit_task_in_db(form, task_id)
        flash('Your task has been updated!')
        return redirect(url_for('views.view_project_tasks', projectno=projectno))
    elif request.method == 'GET':
        task = Task.query.get_or_404(task_id)
        form.title.data = task.title
        form.genre.data = task.genre
    return render_template(
        'forms/add_task.html', title='Edit Task', form=form, genres=genres)


@views.route(
    '/project/<int:projectno>/task_complete/<int:task_id>',
    methods=['GET', 'POST'])
def complete_task(task_id, projectno):
    form = TaskCompleteForm()
    if form.validate_on_submit():
        complete_task_in_db(form, task_id, projectno)
        return redirect(url_for('views.view_project_tasks', projectno=projectno))

    elif request.method == "GET":
        job = get_project_by_id(projectno)
        if job.user_id == get_current_user().id:
            return redirect(url_for('views.view_project_tasks', projectno=projectno))
        else:
            flash(error_msg_403)
            abort(403)


@views.route('/<int:projectno>/task_not_complete/<int:task_id>')
def task_not_complete(task_id, projectno):
    job = get_project_by_id(projectno)
    if job.user_id == get_current_user().id:
        incomplete_task_in_db(task_id, projectno)
        return redirect(url_for('views.view_project_tasks', projectno=projectno))
    else:
        flash(error_msg_403)
        abort(403)



@views.route('/data')
@login_required
def user_data():
    data = get_user_data()
    return jsonify(data)



