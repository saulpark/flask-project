from flask import render_template, request, redirect, url_for, flash, abort
from app.notes import bp
from app.notes.services import NoteService

# Hardcoded user ID since auth is disabled
CURRENT_USER_ID = 1


@bp.route('/')
def list_notes():
    """List all notes for the current user."""
    notes = NoteService.get_all_notes(CURRENT_USER_ID)
    return render_template('notes/list.html', notes=notes)


@bp.route('/new', methods=['GET'])
def new_note():
    """Show create note form."""
    return render_template('notes/new.html')


@bp.route('', methods=['POST'])
def create_note():
    """Create a new note."""
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()

    if not content:
        flash('Content is required', 'danger')
        return redirect(url_for('notes.new_note'))

    # For plain textarea, wrap content in basic JSON structure
    content_delta = f'{{"ops":[{{"insert":"{content}\\n"}}]}}'

    try:
        note = NoteService.create_note(CURRENT_USER_ID, title, content_delta)
        flash('Note created successfully', 'success')
        return redirect(url_for('notes.view_note', id=note.id))
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('notes.new_note'))


@bp.route('/<int:id>')
def view_note(id):
    """View a single note."""
    note = NoteService.get_note_by_id(id)
    if not note:
        abort(404)

    # For now, just extract plain text from Delta JSON
    import json
    try:
        delta = json.loads(note.content_delta)
        content = ''.join(op.get('insert', '') for op in delta.get('ops', []))
    except:
        content = note.content_delta

    return render_template('notes/view.html', note=note, content=content)


@bp.route('/<int:id>/edit', methods=['GET'])
def edit_note(id):
    """Show edit note form."""
    note = NoteService.get_note_by_id(id)
    if not note:
        abort(404)

    # Extract plain text for editing
    import json
    try:
        delta = json.loads(note.content_delta)
        content = ''.join(op.get('insert', '') for op in delta.get('ops', []))
    except:
        content = note.content_delta

    return render_template('notes/edit.html', note=note, content=content)


@bp.route('/<int:id>', methods=['POST'])
def update_note(id):
    """Update an existing note."""
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()

    if not content:
        flash('Content is required', 'danger')
        return redirect(url_for('notes.edit_note', id=id))

    # Wrap content in basic JSON structure
    content_delta = f'{{"ops":[{{"insert":"{content}\\n"}}]}}'

    try:
        note = NoteService.update_note(id, title, content_delta)
        flash('Note updated successfully', 'success')
        return redirect(url_for('notes.view_note', id=note.id))
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('notes.edit_note', id=id))


@bp.route('/<int:id>/delete', methods=['POST'])
def delete_note(id):
    """Delete a note."""
    try:
        NoteService.delete_note(id)
        flash('Note deleted successfully', 'success')
        return redirect(url_for('notes.list_notes'))
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('notes.list_notes'))


@bp.route('/<int:id>/share', methods=['POST'])
def share_note(id):
    """Enable sharing for a note."""
    try:
        token = NoteService.share_note(id)
        flash(f'Note shared! Public link: {request.host_url}p/{token}', 'success')
        return redirect(url_for('notes.view_note', id=id))
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('notes.view_note', id=id))


@bp.route('/<int:id>/unshare', methods=['POST'])
def unshare_note(id):
    """Disable sharing for a note."""
    try:
        NoteService.unshare_note(id)
        flash('Note unshared successfully', 'success')
        return redirect(url_for('notes.view_note', id=id))
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('notes.view_note', id=id))


@bp.route('/p/<token>')
def public_note(token):
    """Public read-only view of a shared note."""
    note = NoteService.get_note_by_token(token)
    if not note:
        abort(404)

    # Extract plain text from Delta JSON
    import json
    try:
        delta = json.loads(note.content_delta)
        content = ''.join(op.get('insert', '') for op in delta.get('ops', []))
    except:
        content = note.content_delta

    return render_template('notes/public.html', note=note, content=content)
