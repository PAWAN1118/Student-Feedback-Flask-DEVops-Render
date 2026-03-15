from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, Response, jsonify
from .database import (
    add_feedback, get_feedback_by_id, update_feedback,
    delete_feedback, search_feedback, get_stats,
    get_paginated_feedback, export_csv
)

feedback_bp = Blueprint(
    'feedback', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/feedback/static'
)


def _db():
    return current_app.config['DB_PATH']


def _per_page():
    return current_app.config.get('PER_PAGE', 6)


@feedback_bp.route('/')
def index():
    page     = request.args.get('page', 1, type=int)
    query    = request.args.get('q', '').strip()
    per_page = _per_page()

    if query:
        feedbacks = search_feedback(_db(), query)
        total     = len(feedbacks)
        start     = (page - 1) * per_page
        feedbacks = feedbacks[start:start + per_page]
    else:
        feedbacks, total = get_paginated_feedback(_db(), page, per_page)

    total_pages = max(1, (total + per_page - 1) // per_page)

    return render_template(
        'index.html',
        feedbacks=feedbacks,
        stats=get_stats(_db()),
        page=page,
        total_pages=total_pages,
        total=total,
        query=query,
        app_name=current_app.config.get('APP_NAME', 'Student Feedback System'),
        app_tagline=current_app.config.get('APP_TAGLINE', 'Academic Excellence Portal'),
    )


@feedback_bp.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name    = request.form.get('name', '').strip()
        course  = request.form.get('course', '').strip()
        rating  = request.form.get('rating', '').strip()
        message = request.form.get('message', '').strip()
        if not name or not message:
            flash('Name and feedback message are required!', 'error')
            return render_template('feedback.html', form_data=request.form)
        add_feedback(_db(), name, course, rating, message)
        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('feedback.index'))
    return render_template('feedback.html', form_data={})


@feedback_bp.route('/edit/<int:feedback_id>', methods=['GET', 'POST'])
def edit(feedback_id):
    fb = get_feedback_by_id(_db(), feedback_id)
    if not fb:
        flash('Feedback not found.', 'error')
        return redirect(url_for('feedback.index'))
    if request.method == 'POST':
        name    = request.form.get('name', '').strip()
        course  = request.form.get('course', '').strip()
        rating  = request.form.get('rating', '').strip()
        message = request.form.get('message', '').strip()
        if not name or not message:
            flash('Name and feedback message are required!', 'error')
            return render_template('edit.html', fb=fb)
        update_feedback(_db(), feedback_id, name, course, rating, message)
        flash('Feedback updated successfully!', 'success')
        return redirect(url_for('feedback.index'))
    return render_template('edit.html', fb=fb)


@feedback_bp.route('/delete/<int:feedback_id>', methods=['POST'])
def delete(feedback_id):
    delete_feedback(_db(), feedback_id)
    flash('Feedback deleted.', 'success')
    return redirect(url_for('feedback.index'))


@feedback_bp.route('/api/stats')
def api_stats():
    return jsonify(get_stats(_db()))


@feedback_bp.route('/api/export.csv')
def api_export():
    return Response(
        export_csv(_db()),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=feedback.csv'}
    )


@feedback_bp.route('/health')
def health():
    return jsonify({'status': 'ok', 'message': 'Feedback System running'}), 200
