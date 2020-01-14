# Consult Request
# *****************************

import json
from app import db, auth, email_service, app
from app.models import EmailLog
from app.models import User
from sqlalchemy import desc, asc, exists, or_, func
from sqlalchemy.exc import IntegrityError
from flask import jsonify, make_response, request, Blueprint
import requests

consult_blueprint = Blueprint('consult', __name__, url_prefix='/api')


@consult_blueprint.route('/consult_category_list', methods=["GET"])
@auth.login_required
def consult_category_list():
    return make_response(
        jsonify([*app.config['JIRA_PROJECT_TICKET_ROUTE_LOOKUP']]), 200
    )


@consult_blueprint.route('/consult_request_list', methods=["GET"])
@auth.login_required
def consult_request_list():
    # args = request.args
    user_id = request.values.get('user_id')

    user = User.query.filter_by(id=user_id).first_or_404()

    try:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        r = requests.get(
            ''.join([app.config['API_UVARC_URL'],
                     'get-all-customer-requests', '/?email={}']).format(user.email),
            headers=headers
        )
        if(r.status_code == 200):
            response_data = []
            r_objects = json.loads(r.text)
            for r_object in r_objects:
                if (r_object['project_name'] in app.config['UNIQUE_JIRA_CONSULT_PROJECTS']):
                    response_data.append(r_object)

            return make_response(jsonify(response_data), r.status_code)
        else:
            print(r.text)
            return make_response(jsonify(
                {
                    "status": "error",
                    "message": "Couldn't submit consult request, please contact iTHRIV system admin"
                }
            ), r.status_code)
    except Exception as ex:
        print(str(ex))
        raise Exception(
            "Couldn't submit consult request, please contact iTHRIV system admin: {}".format(str(ex)))


@consult_blueprint.route('/consult_request', methods=["GET", "POST"])
@auth.login_required
def consult_request():
    request_data = request.get_json()
    user_id = request_data['user_id']
    user = User.query.filter_by(id=user_id).first_or_404()
    # admins = User.query.filter_by(
    #     role="Admin", institution_id=user.institution_id).all()

    try:
        jira_project_ticket_route_info = app.config[
            'JIRA_PROJECT_TICKET_ROUTE_LOOKUP'][
            request_data['request_category']][
            user.institution.name].split('|')
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'email': user.email,
            'name': user.display_name,
            'category': request_data['request_category'],
            'description': request_data['request_text'],
            'JIRA_PROJECT_TICKET_ROUTE': '{}|{}|{}'.format(
                jira_project_ticket_route_info[0],
                request_data['request_type'],
                jira_project_ticket_route_info[1],
            ),
            'REQUEST_CLIENT': 'ITHRIV'
        }
        if request_data['request_title'] is not None and request_data['request_title'].lstrip() != '':
            data['request_title'] = request_data['request_title']
        r = requests.post(
            ''.join([app.config['API_UVARC_URL'],
                     'general-support-request', '/']),
            headers=headers,
            data=data
        )
        if(r.status_code == 200):
            return make_response(r.text, r.status_code)
        else:
            print(r.text)
            if r.reason:
                return make_response(jsonify(
                    {
                        "status": "error",
                        "message": "Couldn't submit consult request: {}".format(r.reason)
                    }
                ), r.status_code)
            else:
                return make_response(jsonify(
                    {
                        "status": "error",
                        "message": "Couldn't submit consult request, please contact iTHRIV system admin"
                    }
                ), r.status_code)
    except Exception as ex:
        print(str(ex))
        raise Exception(
            "Couldn't submit consult request, please contact iTHRIV system admin: {}".format(str(ex)))

    # Send consult request email to each admin for the institution
    # for admin in admins:
    #     tracking_code = email_service.consult_email(user, admin, request_data)
    #     log = EmailLog(user_id=admin.id, type="consult_request",
    #                    tracking_code=tracking_code)
    #     db.session.add(log)
    #     db.session.commit()

    return ''
