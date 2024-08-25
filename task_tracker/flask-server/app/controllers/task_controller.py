from app import app
from flask import Flask, render_template, redirect, request, flash, session
from app.models.task_model import Task
from app.models.user_model import User



#display
@app.route('/task/<int:task_id>')
def display_task(task_id):
    if 'user_id' not in session:
        return redirect('/')
    
    task = Task.get_one_task(task_id)
    
    if not task:
        flash("Task not found")
        return redirect('/user/dashboard')
    
    user = User.get_one_by_id(session['user_id'])
    return render_template('/task/display_task.html', task = task, user = user)#task = task.get_one_task(task_id)


# display tasks by user
@app.route('/user/tasks')
def user_tasks():
    if 'user_id' not in session:
        return redirect('/')

    user = User.get_one_by_id(session['user_id'])
    tasks = Task.get_tasks_by_user(session['user_id'])
    
    for task in tasks:
        # Check if the user is logged in and is the owner of the Task
        task.can_edit = (task.user_id == session['user_id'])

    return render_template('/user/user_tasks.html', tasks=tasks, user=user)


#report a task
@app.route('/task/add')
def get_add_task_form():
    
    if not 'user_id' in session:
        return redirect('/')
    
    user = User.get_one_by_id(session['user_id'])
    return render_template('/task/post_new_task.html', user = user)


#report a task
@app.route('/task/add', methods=['POST'])
def add_task():
    if not 'user_id' in session:
        return redirect('/')
    
    Task.create_task({
        **request.form,
        'user_id': session['user_id'],
    })
    return redirect('/user/dashboard')


#edit a task
@app.route('/task/update/<int:task_id>')
def get_update_task_form(task_id):
    
    if not 'user_id' in session:
        return redirect('/')
    
    return render_template('/task/edit_task.html', task = Task.get_one_task(task_id))


#edit a task
@app.route('/task/update', methods=['POST'])
def update_task():
    if not 'user_id' in session:
        return redirect('/')
    
    Task.update_task(request.form)
    
    return redirect('/user/dashboard')



@app.route('/task/delete/<int:task_id>')
def delete(task_id):
        Task.delete_task(task_id)
        return redirect('/user/dashboard')



