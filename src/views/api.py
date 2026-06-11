from flask import jsonify, request, url_for, current_app
from src.views import main_bp
from src.forms import ShortenURLForm
from src.models import db, ShortURL


@main_bp.route('/api/shorten', methods=['POST'])
def api_shorten():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    long_url = data.get('long_url')
    custom_code = data.get('custom_code')

    form = ShortenURLForm(long_url=long_url, custom_code=custom_code)

    # Manually validate the form without CSRF for API context
    if not form.long_url.validate(form) or (custom_code and not form.custom_code.validate(form)):
        errors = {}
        if form.long_url.errors: errors['long_url'] = form.long_url.errors
        if form.custom_code.errors: errors['custom_code'] = form.custom_code.errors
        return jsonify({"error": "Validation failed", "details": errors}), 400

    if custom_code:
        existing_url = ShortURL.query.filter_by(short_code=custom_code).first()
        if existing_url:
            return jsonify({"error": "Custom code already in use."}), 409 # Conflict
        short_code = custom_code
    else:
        short_code = None
        while short_code is None or ShortURL.query.filter_by(short_code=short_code).first():
            short_code = ShortURL.generate_short_code()

    new_url = ShortURL(long_url=long_url, short_code=short_code)
    db.session.add(new_url)
    db.session.commit()

    short_link = url_for('main.redirect_to_long_url', short_code=short_code, _external=True)

    return jsonify({
        "short_url": short_link,
        "long_url": long_url,
        "short_code": short_code
    }), 201 # Created
