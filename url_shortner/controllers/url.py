from datetime import datetime, timedelta
from flask import request, redirect

from app import app
from models.url import URLMapper
from utils import (
    db_session,
    generate_random_string,
    standard_200_data_return,
    standard_400_return,
    standard_404_return,
    token_required,
)


@app.route("/create-short-url/", methods=["POST"])
@token_required
def create_short_url(current_user):
    session = db_session()

    def after_validation(long_url, expiry, usage_limit):
        url_object = (
            session.query(URLMapper).filter_by(user_id=current_user.id,long_url=long_url).first()
        )
        if not url_object:
            while True:
                url_key = generate_random_string()
                existing = (
                    session.query(URLMapper).filter_by(url_key=url_key).count()
                )
                if existing == 0:
                    break
            url_mapper = URLMapper(
                user_id=current_user.id,
                long_url=long_url,
                url_key=url_key,
                expiry_datetime=expiry,
                usage_limit=usage_limit,
            )
            session.add(url_mapper)
            session.commit()
            data = {
                "long_url": url_mapper.long_url,
                "short_url": "/u/" + url_mapper.url_key,
                "expiry": url_mapper.expiry_datetime.isoformat(),
            }
            response = (
                standard_200_data_return(data),
                200,
            )
            return response
        url_object.expiry_datetime = expiry
        if usage_limit:
            url_object.usage_limit = usage_limit
        session.add(url_object)
        session.commit()
        data = {
            "long_url": url_object.long_url,
            "short_url": "/u/" + url_object.url_key,
            "expiry": url_object.expiry_datetime.isoformat(),
        }
        response = (
            standard_200_data_return(data, "This long_url already exist"),
            200,
        )
        return response

    try:
        data = request.get_json()
        print("data", data)
        long_url = data.get("long_url")
        if not long_url:
            raise ValueError("long_url is a required field")

        absolute_expiry = data.get("absolute_expiry")
        relative_expiry = data.get("relative_expiry")
        usage_limit = data.get("usage_limit")
        today = datetime.now()
        if absolute_expiry:
            min_expiry = today + timedelta(hours=1)
            max_expiry = today + timedelta(days=365)
            expiry = datetime.fromisoformat(absolute_expiry)
            if min_expiry <= expiry <= max_expiry:
                return after_validation(long_url, expiry, usage_limit)
            else:
                response = standard_400_return("Invalid expiry"), 400
        elif relative_expiry:
            days = relative_expiry.get("days", 0)
            hours = relative_expiry.get("hours", 0)
            minutes = relative_expiry.get("minutes", 0)
            seconds = relative_expiry.get("seconds", 0)
            delta = timedelta(
                days=days, hours=hours, minutes=minutes, seconds=seconds
            )
            if timedelta(hours=1) <= delta <= timedelta(days=365):
                expiry = today + delta
                response = after_validation(long_url, expiry, usage_limit)
            else:
                response = standard_400_return("Invalid expiry"), 400
        else:
            response = (
                standard_400_return(
                    "Either relative_expiry or absolute_expiry should be present"
                ),
                400,
            )
    except ValueError as err:
        response = standard_400_return(err), 400
    finally:
        if session:
            session.close()
    return response


@app.route("/u/<string:url_key>", methods=["GET"])
def redirect_short_url(url_key):
    session = db_session()
    url_mapper = session.query(URLMapper).filter_by(url_key=url_key).first()
    if url_mapper:
        expiry_datetime = url_mapper.expiry_datetime
        usage_limit = url_mapper.usage_limit
        hit_count = url_mapper.hit_count
        today = datetime.now()
        if expiry_datetime < today or (
            usage_limit is not None and usage_limit <= hit_count
        ):
            # NOTE: delete url_mapper obj from db
            session.delete(url_mapper)
            session.commit()
            return (
                standard_404_return("URL not found, Usage limit exhausted"),
                404,
            )
        else:
            url_mapper.hit_count += 1
            long_url = url_mapper.long_url
            session.commit()
            session.close()
            return redirect(
                long_url, code=302
            )  # NOTE: 302: for temporary redirects
    else:
        session.close()
        return standard_404_return("URL not found"), 404


@app.route("/get-urls/", methods=["GET"])
@token_required
def get_all_urls(current_user):
    session = db_session()
    url_mappers = (
        session.query(URLMapper).filter_by(user_id=current_user.id).all()
    )
    return (
        standard_200_data_return(
            [
                {
                    "long_url": um.long_url,
                    "short_url": "/u/" + um.url_key,
                    "expiry": um.expiry_datetime.isoformat(),
                    "hit_count": um.hit_count,
                    "usage_limit": um.usage_limit,
                }
                for um in url_mappers
            ]
        ),
        200,
    )
