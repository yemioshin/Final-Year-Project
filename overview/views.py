from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, abort
from flask_login import login_required, current_user
from .models import User, Project, Task
from . import db
from .forms import (
    ProjectForm, TaskForm,
    TaskCompleteForm,)
import json

views = Blueprint('views', __name__)


error_msg_403 = 'Access denied: You do not have access to this project'



@views.route('/')
@login_required
def home():
    return render_template("dashboard.html", user=current_user)

@views.route('/projects')
@login_required
def view_projects():
    jobs = Project.query.filter_by(user_id=current_user.id)
    return render_template('projects.html', jobs=jobs)



# ------------------------------------------------------- NEW PROJECT
@views.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            number=form.number.data,
            name=form.name.data.lower(),
            value=form.value.data,
            subject=form.subject.data,
            user=current_user)
        db.session.add(project)
        db.session.commit()
        flash('Congratulations, you created a Project')
        return redirect(url_for('views.view_projects'))
    return render_template(
        'forms/add_project.html', title="Create Project", form=form)


# ------------------------------------------------------- SINGLE PROJECTS
@views.route('/project/<projectno>')
@login_required
def view_project_tasks(projectno):
    form = TaskCompleteForm()
    tasks = Task.query.filter_by(project_id=projectno)
    job = Project.query.filter_by(id=projectno).first_or_404()
    if job.user_id == current_user.id:
        return render_template(
            'projects_tasks.html', tasks=tasks, job=job, form=form)
    else:
        flash(error_msg_403)
        abort(403)


@views.route('/project/<int:projectno>/edit_project', methods=['GET', 'POST'])
@login_required
def edit_project(projectno):
    job = Project.query.filter_by(id=projectno).first_or_404()
    if job.user_id != current_user.id:
        flash(error_msg_403)
        abort(403)
    form = ProjectForm()
    if form.validate_on_submit():
        job.number = form.number.data
        job.name = form.name.data.lower()
        job.value = form.value.data
        job.subject = form.subject.data
        db.session.commit()
        flash('Your project has been updated!')
        return redirect(url_for('views.view_project_tasks', projectno=projectno))
    elif request.method == 'GET':
        form.number.data = job.number
        form.name.data = job.name
        form.value.data = job.value
        form.subject.data = job.subject
    return render_template(
        'forms/add_project.html', title="Edit Project", form=form)


@views.route('/project/<int:projectno>/delete_project', methods=['GET', 'POST'])
@login_required
def delete_project(projectno):
    job = Project.query.filter_by(id=projectno).first_or_404()
    if job.user_id != current_user.id:
        flash(error_msg_403)
        abort(403)
    db.session.delete(job)
    db.session.commit()
    flash('Project successfully deleted')
    return redirect(url_for('views.view_projects'))


@views.route('/project/<int:projectno>/add_task', methods=['GET', 'POST'])
@login_required
def add_task(projectno):
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            genre=form.genre.data,
            project_id=projectno)
        # If all task are complete,
        # when new task added mark project as not complete
        are_all_tasks_complete = len(
            {task.completed for task in Task.query.filter_by(
                project_id=projectno)})
        if are_all_tasks_complete == 1:
            project = Project.query.filter_by(id=projectno).first_or_404()
            project.completed = False
        db.session.add(task)
        db.session.commit()
        flash('Congratulations, you created a Task')
        return redirect(url_for('views.view_project_tasks', projectno=projectno))

    elif request.method == "GET":
        job = Project.query.get(projectno)

        # join the Project table and the Task table on project id
        project_tasks_table_join = Project.query.join(
            Task,
            (Task.project_id == Project.id)).all()

        # get all task genres previously used by a user
        list_of_genres = [
            project.tasks.all() for project
            in project_tasks_table_join
            if project.user_id == current_user.id
            ]
        genres = sorted(
            {item.genre for sublist in list_of_genres for item in sublist})

        if job.user_id == current_user.id:
            return render_template(
                'forms/add_task.html',
                title='Create Task', form=form, genres=genres)
        else:
            flash(error_msg_403)
            abort(403)



@views.route('/project/<projectno>/delete_task/<int:task_id>')
def delete_task(task_id, projectno):
    job = Project.query.filter_by(id=projectno).first_or_404()

    if job.user_id == current_user.id:
        task = Task.query.filter_by(id=task_id).first_or_404()
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('views.view_project_tasks', projectno=projectno))
    else:
        flash(error_msg_403)
        abort(403)


@views.route(
    '/project/<int:projectno>/edit_task/<int:task_id>',
    methods=['GET', 'POST'])
def edit_task(task_id, projectno):
    job = Project.query.filter_by(id=projectno).first_or_404()
    task = Task.query.get_or_404(task_id)

    # join the Project table and the Task table on project id
    project_tasks_table_join = Project.query.join(
        Task,
        (Task.project_id == Project.id)).all()

    # get all task genres previously used by a user
    list_of_genres = [
        project.tasks.all() for project
        in project_tasks_table_join
        if project.user_id == current_user.id
        ]

    genres = sorted(
        {item.genre for sublist in list_of_genres for item in sublist})

    if job.user_id != current_user.id:
        flash(error_msg_403)
        abort(403)
    form = TaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.genre = form.genre.data
        db.session.commit()
        flash('Your task has been updated!')
        return redirect(url_for('views.view_project_tasks', projectno=projectno))
    elif request.method == 'GET':
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
        # Complete Task
        task = Task.query.filter_by(id=task_id).first_or_404()
        task.duration = form.duration.data
        task.completed = True
        db.session.commit()

        # Complete project if all task are complete
        are_all_tasks_complete = len(
            {task.completed for task in Task.query.filter_by(
                project_id=projectno)})
        if are_all_tasks_complete == 1:
            project = Project.query.filter_by(id=projectno).first_or_404()
            project.completed = True
            db.session.commit()

        return redirect(url_for('views.view_project_tasks', projectno=projectno))

    elif request.method == "GET":
        job = Project.query.filter_by(id=projectno).first_or_404()
        if job.user_id == current_user.id:
            return redirect(url_for('views.view_project_tasks', projectno=projectno))
        else:
            flash(error_msg_403)
            abort(403)


@views.route('/<int:projectno>/task_not_complete/<int:task_id>')
def task_not_complete(task_id, projectno):
    job = Project.query.filter_by(id=projectno).first_or_404()
    if job.user_id == current_user.id:
        are_all_tasks_complete = len(
            {task.completed for task in Task.query.filter_by(
                project_id=projectno)})
        if are_all_tasks_complete == 1:
            project = Project.query.filter_by(id=projectno).first_or_404()
            project.completed = False
        task = Task.query.filter_by(id=task_id).first_or_404()
        task.completed = False
        db.session.commit()
        return redirect(url_for('views.view_project_tasks', projectno=projectno))
    else:
        flash(error_msg_403)
        abort(403)


@views.route('/data')
@login_required
def user_data():
    user_projects = Project.query.join(
        User, (User.id == Project.user_id)).filter(
            User.id == current_user.id)

    data = [
        {
            'user': job.user.username,
            'project_title': job.name,
            'project_id': job.id,
            'project_value': job.value,
            'project_subject': job.subject,
            'project_completed': sum([job.completed]),
            'project_recieved': job.timestamp,
            'project_tasks_all': len(job.tasks.all()),
            'project_tasks_completed':
                sum([task.completed for task in job.tasks.all()])
        }
        for job in user_projects]

    return jsonify(data)

@views.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', user=current_user)

@views.route('/calendar')
def calendar():
    return render_template('calendar.html', user=current_user)

@views.route('/habit_tracker')
def habit_tracker():
    return render_template('habit_tracker.html', user=current_user)

@views.route('/profile')
def profile():
    return render_template('profile.html', user=current_user)


