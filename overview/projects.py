from flask import Blueprint, abort, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from .models import Project, Task
from . import db

projects = Blueprint('projects', __name__)

@projects.route('/projects', methods=['GET'])
@login_required
def list_projects():
    user_projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('projects.html', projects=user_projects)


@projects.route('/projects/new', methods=['GET', 'POST'])
@login_required
def new_project():
    if request.method == 'POST':
        project_name = request.form['name']
        project_description = request.form['description']
        project_start_date = request.form['start_date']
        project_end_date = request.form['end_date']

        new_project = Project(name=project_name, description=project_description,
                              start_date=project_start_date, end_date=project_end_date,
                              user_id=current_user.id)
        db.session.add(new_project)
        db.session.commit()

        flash('Project created successfully', 'success')
        return redirect(url_for('projects.list_projects'))

    return render_template('new_project.html')

@projects.route('/projects/<int:project_id>/tasks/new', methods=['POST'])
@login_required
def create_task(project_id):
    project = Project.query.get_or_404(project_id)

    if project.user_id != current_user.id:
        abort(403)

    task_name = request.form['task_name']
    new_task = Task(name=task_name, project_id=project_id)
    db.session.add(new_task)
    db.session.commit()

    flash('Task created successfully', 'success')
    return redirect(url_for('projects.list_projects'))



@projects.route('/projects/<int:project_id>/update', methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    project = Project.query.get_or_404(project_id)

    if project.user_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        project.name = request.form['name']
        project.description = request.form['description']
        project.start_date = request.form['start_date']
        project.end_date = request.form['end_date']

        db.session.commit()

        flash('Project updated successfully', 'success')
        return redirect(url_for('projects.list_projects'))

    return render_template('update_project.html', project=project)


@projects.route('/projects/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)

    if project.user_id != current_user.id:
        abort(403)

    db.session.delete(project)
    db.session.commit()

    flash('Project deleted successfully', 'success')
    return redirect(url_for('projects.list_projects'))

