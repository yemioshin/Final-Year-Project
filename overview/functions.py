from flask_login import current_user
from .models import User, Project, Task
from . import db

# Current user
def get_current_user():
    return current_user

# Projects
def get_user_projects(user_id):
    return Project.query.filter_by(user_id=user_id)

def add_project_to_db(form):
    project = Project(
        number=form.number.data,
        name=form.name.data.lower(),
        time=form.time.data,
        subject=form.subject.data,
        user=get_current_user()
    )
    db.session.add(project)
    db.session.commit()

def get_project_by_id(projectno):
    return Project.query.filter_by(id=projectno).first_or_404()

def edit_project_in_db(form, projectno):
    job = get_project_by_id(projectno)
    job.number = form.number.data
    job.name = form.name.data.lower()
    job.time = form.time.data
    job.subject = form.subject.data
    db.session.commit()

def delete_project_from_db(projectno):
    job = get_project_by_id(projectno)
    db.session.delete(job)
    db.session.commit()

# Tasks
def get_project_tasks(projectno):
    return Task.query.filter_by(project_id=projectno)

def add_task_to_db(form, projectno):
    task = Task(
        title=form.title.data,
        genre=form.genre.data,
        project_id=projectno
    )
    db.session.add(task)
    db.session.commit()

def delete_task_from_db(task_id):
    task = Task.query.filter_by(id=task_id).first_or_404()
    db.session.delete(task)
    db.session.commit()

def edit_task_in_db(form, task_id):
    task = Task.query.get_or_404(task_id)
    task.title = form.title.data
    task.genre = form.genre.data
    db.session.commit()

def complete_task_in_db(form, task_id, projectno):
    task = Task.query.filter_by(id=task_id).first_or_404()
    task.duration = form.duration.data
    task.completed = True
    db.session.commit()
    project = Project.query.filter_by(id=projectno).first_or_404()
    are_all_tasks_complete = len({task.completed for task in Task.query.filter_by(project_id=projectno)})
    if are_all_tasks_complete == 1 and True in {task.completed for task in Task.query.filter_by(project_id=projectno)}:
        project.completed = True
    db.session.commit()


def incomplete_task_in_db(task_id, projectno):
    task = Task.query.filter_by(id=task_id).first_or_404()
    task.completed = False
    db.session.commit()
    project = Project.query.filter_by(id=projectno).first_or_404()
    are_all_tasks_complete = len({task.completed for task in Task.query.filter_by(project_id=projectno)})
    if are_all_tasks_complete == 1 and False in {task.completed for task in Task.query.filter_by(project_id=projectno)}:
        project.completed = False
    db.session.commit()


        

def get_user_data():
    user_projects = Project.query.join(
        User, (User.id == Project.user_id)).filter(
            User.id == current_user.id
    )

    data = [
        {
            'user': job.user.username,
            'project_title': job.name,
            'project_id': job.id,
            'project_time': job.time,
            'project_subject': job.subject,
            'project_completed': sum([job.completed]),
            'project_recieved': job.timestamp,
            'project_tasks_all': len(job.tasks.all()),
            'project_tasks_completed': sum([task.completed for task in job.tasks.all()])
        }
        for job in user_projects
    ]

    return data
