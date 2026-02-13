from flask import render_template, request, redirect, url_for, flash, abort
from app.users import bp
from app.services.user_service import UserService


@bp.route('/')
def list_users():
    """List all users."""
    users = UserService.get_all_users()
    return render_template('users/list.html', users=users)


@bp.route('/new', methods=['GET'])
def new_user():
    """Show create user form."""
    return render_template('users/new.html')


@bp.route('', methods=['POST'])
def create_user():
    """Create a new user."""
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')

    if not email or not password:
        flash('Email and password are required', 'danger')
        return redirect(url_for('users.new_user'))

    if password != confirm_password:
        flash('Passwords do not match', 'danger')
        return redirect(url_for('users.new_user'))

    try:
        user = UserService.create_user(email, password)
        flash(f'User {user.email} created successfully', 'success')
        return redirect(url_for('users.view_user', id=user.id))
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('users.new_user'))


@bp.route('/<int:id>')
def view_user(id):
    """View a single user."""
    user = UserService.get_user_by_id(id)
    if not user:
        abort(404)

    # Get user's note count
    note_count = len(user.notes)
    return render_template('users/view.html', user=user, note_count=note_count)


@bp.route('/<int:id>/password', methods=['GET'])
def edit_password(id):
    """Show change password form."""
    user = UserService.get_user_by_id(id)
    if not user:
        abort(404)

    return render_template('users/password.html', user=user)


@bp.route('/<int:id>/password', methods=['POST'])
def update_password(id):
    """Update user password."""
    old_password = request.form.get('old_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')

    if not old_password or not new_password:
        flash('All fields are required', 'danger')
        return redirect(url_for('users.edit_password', id=id))

    if new_password != confirm_password:
        flash('New passwords do not match', 'danger')
        return redirect(url_for('users.edit_password', id=id))

    try:
        UserService.update_password(id, old_password, new_password)
        flash('Password updated successfully', 'success')
        return redirect(url_for('users.view_user', id=id))
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('users.edit_password', id=id))


@bp.route('/<int:id>/delete', methods=['POST'])
def delete_user(id):
    """Delete a user."""
    try:
        UserService.delete_user(id)
        flash('User deleted successfully', 'success')
        return redirect(url_for('users.list_users'))
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('users.list_users'))
