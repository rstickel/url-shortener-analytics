from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, Optional, Length, Regexp, ValidationError
from src.models import ShortURL


class ShortenURLForm(FlaskForm):
    long_url = StringField('Long URL', validators=[
        DataRequired(message='Please enter a URL.'),
        URL(message='Please enter a valid URL.')
    ], render_kw={"placeholder": "Enter your long URL here"})

    custom_code = StringField('Custom Short Code (optional)', validators=[
        Optional(),
        Length(min=3, max=100, message='Custom code must be between 3 and 100 characters.'),
        Regexp('^[a-zA-Z0-9_-]+$', message='Custom code can only contain letters, numbers, hyphens, and underscores.')
    ], render_kw={"placeholder": "e.g., mylink"})

    submit = SubmitField('Shorten URL')

    def validate_custom_code(self, field):
        if field.data and ShortURL.query.filter_by(short_code=field.data).first():
            raise ValidationError('This custom short code is already in use. Please choose another.')

