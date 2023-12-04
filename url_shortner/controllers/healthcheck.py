from app import app
from utils import standard_200_message_return, token_required


@app.route("/healthcheck/")
def healthcheck():
    # TODO: Check database connection
    return standard_200_message_return("Success"), 200


@app.route("/test-token/")
@token_required
def test_token(current_user):
    return (
        standard_200_message_return(
            f"Success, welcome {current_user.name} <{current_user.email}>"
        ),
        200,
    )
