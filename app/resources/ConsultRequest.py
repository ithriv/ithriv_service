# Consult Request
# *****************************

from app import db, auth, email_service
from app.models import EmailLog
from app.models import User
from flask import request, Blueprint

consult_blueprint = Blueprint('consult', __name__, url_prefix='/api')


@consult_blueprint.route('/consult_request', methods=["GET", "POST"])
@auth.login_required
def consult_request():
    request_data = request.get_json()
    user_id = request_data['user_id']
    user = User.query.filter_by(id=user_id).first_or_404()
    admins = User.query.filter_by(
        role="Admin", institution_id=user.institution_id).all()

    # Send consult request email to each admin for the institution
    for admin in admins:
        tracking_code = email_service.consult_email(user, admin, request_data)
        log = EmailLog(user_id=admin.id, type="consult_request",
                       tracking_code=tracking_code)
        db.session.add(log)
        db.session.commit()

    return ''
