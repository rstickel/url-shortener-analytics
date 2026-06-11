from flask import render_template, redirect, url_for, flash, request, current_app
from src.views import main_bp
from src.forms import ShortenURLForm
from src.models import db, ShortURL, ClickEvent
from urllib.parse import urlparse
from user_agents import parse


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    form = ShortenURLForm()
    if form.validate_on_submit():
        long_url = form.long_url.data
        custom_code = form.custom_code.data

        if custom_code:
            # Check if custom code exists already (form validation also handles this)
            existing_url = ShortURL.query.filter_by(short_code=custom_code).first()
            if existing_url:
                flash('Custom short code already in use. Please choose another.', 'danger')
                return render_template('index.html', form=form)
            short_code = custom_code
        else:
            # Generate a unique short code
            short_code = None
            while short_code is None or ShortURL.query.filter_by(short_code=short_code).first():
                short_code = ShortURL.generate_short_code()

        new_url = ShortURL(long_url=long_url, short_code=short_code)
        db.session.add(new_url)
        db.session.commit()
        flash('Your URL has been shortened!', 'success')
        return redirect(url_for('main.short_url_details', short_code=short_code))

    recent_urls = ShortURL.query.order_by(ShortURL.created_at.desc()).limit(5).all() # For display
    return render_template('index.html', form=form, recent_urls=recent_urls)


@main_bp.route('/<short_code>')
def redirect_to_long_url(short_code):
    short_url_entry = ShortURL.query.filter_by(short_code=short_code).first_or_404()

    # Record click event
    ip_address = request.remote_addr
    user_agent_string = request.headers.get('User-Agent')
    referrer = request.headers.get('Referer')

    # Parse user agent for more details
    ua = parse(user_agent_string) if user_agent_string else None

    # Geo-location (placeholder - needs actual integration with a Geo-IP service)
    country = None
    city = None
    # Example: if using a Geo-IP service like ipapi.com (requires 'requests' library)
    # import requests
    # try:
    #     response = requests.get(f"http://ipapi.com/json/{ip_address}?key=YOUR_API_KEY").json()
    #     country = response.get('country_name')
    #     city = response.get('city')
    # except Exception as e:
    #     current_app.logger.error(f"Geo-IP lookup failed for {ip_address}: {e}")

    click_event = ClickEvent(
        short_url=short_url_entry,
        ip_address=ip_address,
        user_agent=user_agent_string,
        referrer=referrer,
        country=country,
        city=city
    )
    db.session.add(click_event)
    db.session.commit()

    return redirect(short_url_entry.long_url)


@main_bp.route('/<short_code>/details')
def short_url_details(short_code):
    short_url_entry = ShortURL.query.filter_by(short_code=short_code).first_or_404()
    short_link = url_for('main.redirect_to_long_url', short_code=short_code, _external=True)
    return render_template('short_url.html', short_url_entry=short_url_entry, short_link=short_link)


@main_bp.route('/<short_code>/stats')
def analytics(short_code):
    short_url_entry = ShortURL.query.filter_by(short_code=short_code).first_or_404()
    clicks = short_url_entry.clicks
    total_clicks = len(clicks)

    # Process data for display (e.g., aggregate by day, referrer, browser)
    click_data = {
        'total_clicks': total_clicks,
        'clicks_by_day': {},
        'top_referrers': {},
        'top_browsers': {},
        'top_os': {},
        'top_countries': {},
        'top_cities': {}
    }

    for click in clicks:
        # Clicks by day
        day = click.timestamp.strftime('%Y-%m-%d')
        click_data['clicks_by_day'][day] = click_data['clicks_by_day'].get(day, 0) + 1

        # Referrers
        referrer_host = urlparse(click.referrer).netloc if click.referrer else 'Direct/Unknown'
        click_data['top_referrers'][referrer_host] = click_data['top_referrers'].get(referrer_host, 0) + 1

        # User Agent parsing
        if click.user_agent:
            ua = parse(click.user_agent)
            browser = ua.browser.family if ua.browser.family else 'Unknown'
            os_name = ua.os.family if ua.os.family else 'Unknown'
            click_data['top_browsers'][browser] = click_data['top_browsers'].get(browser, 0) + 1
            click_data['top_os'][os_name] = click_data['top_os'].get(os_name, 0) + 1

        # Geo data
        if click.country:
            click_data['top_countries'][click.country] = click_data['top_countries'].get(click.country, 0) + 1
        if click.city:
            click_data['top_cities'][click.city] = click_data['top_cities'].get(click.city, 0) + 1

    # Sort for display
    click_data['clicks_by_day'] = sorted(click_data['clicks_by_day'].items())
    click_data['top_referrers'] = sorted(click_data['top_referrers'].items(), key=lambda item: item[1], reverse=True)[:5]
    click_data['top_browsers'] = sorted(click_data['top_browsers'].items(), key=lambda item: item[1], reverse=True)[:5]
    click_data['top_os'] = sorted(click_data['top_os'].items(), key=lambda item: item[1], reverse=True)[:5]
    click_data['top_countries'] = sorted(click_data['top_countries'].items(), key=lambda item: item[1], reverse=True)[:5]
    click_data['top_cities'] = sorted(click_data['top_cities'].items(), key=lambda item: item[1], reverse=True)[:5]

    return render_template('analytics.html', short_url_entry=short_url_entry, click_data=click_data)

