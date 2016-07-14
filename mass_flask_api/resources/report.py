from flask import jsonify

from mass_flask_api.config import api_blueprint
from mass_flask_core.utils import AuthFunctions, AdminAccessPrivilege
from .base import BaseResource
from mass_flask_api.utils import get_pagination_compatible_schema, register_api_endpoint
from mass_flask_api.schemas import ReportSchema
from mass_flask_core.models import Report


class ReportResource(BaseResource):
    schema = ReportSchema()
    pagination_schema = get_pagination_compatible_schema(ReportSchema)
    model = Report
    query_key_field = 'id'
    filter_parameters = []

    @AuthFunctions.check_api_key()
    def get_list(self):
        """
        ---
        get:
            description: Get a list of all reports.
            responses:
                200:
                    description: A list of reports is returned.
                    schema: ReportSchema
        """
        return super(ReportResource, self).get_list()

    @AuthFunctions.check_api_key()
    def get_detail(self, **kwargs):
        """
        ---
        get:
            description: Get a single report object
            parameters:
                - in: path
                  name: id
                  type: string
            responses:
                200:
                    description: The report is returned.
                    schema: ReportSchema
                404:
                    description: No report with the specified id has been found.
        """
        return super(ReportResource, self).get_detail(**kwargs)

    def post(self):
        return jsonify({'error': 'Method not allowed for this endpoint.'}), 405

    def put(self, **kwargs):
        return jsonify({'error': 'Method not allowed for this endpoint.'}), 405

    @AuthFunctions.check_api_key(privileges=[AdminAccessPrivilege()])
    def delete(self, **kwargs):
        """
        ---
        delete:
            description: Delete an existing report object
            parameters:
                - in: path
                  name: id
                  type: string
            responses:
                204:
                    description: The object has been deleted.
                400:
                    description: The server was not able to delete an object based on the request data.
                404:
                    description: No report with the specified id has been found.
        """
        return super(ReportResource, self).delete(**kwargs)

    @AuthFunctions.check_api_key()
    def get_json_report_object(self, **kwargs):
        """
        ---
        get:
            description: Get the contents of a JSON report object
            parameters:
                - in: path
                  name: id
                  type: string
                - in: path
                  name: object_name
                  type: string
            responses:
                200:
                    description: The JSON report object is returned.
                400:
                    description: Invalid request.
                404:
                    description: No report with the specified id has been found.
        """
        report = self.model.objects(id=kwargs['id']).first()
        if not report:
            return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs['id'])}), 404
        else:
            obj = report.json_report_objects[kwargs['object_name']]
            if not obj:
                return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs['object_name'])}), 404
            else:
                file = obj.read()
                return file, 200, {'Content-Type': 'application/json'}

    @AuthFunctions.check_api_key()
    def get_raw_report_object(self, **kwargs):
        """
        ---
        get:
            description: Get the contents of a raw binary report object
            parameters:
                - in: path
                  name: id
                  type: string
                - in: path
                  name: object_name
                  type: string
            responses:
                200:
                    description: The raw binary report object is returned.
                400:
                    description: Invalid request.
                404:
                    description: No report with the specified id has been found.
        """
        report = self.model.objects(id=kwargs['id']).first()
        if not report:
            return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs['id'])}), 404
        else:
            obj = report.raw_report_objects[kwargs['object_name']]
            if not obj:
                return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs['object_name'])}), 404
            else:
                file = obj.read()
                return file, 200, {'Content-Type': 'binary/octet-stream'}


register_api_endpoint('report', ReportResource)

api_blueprint.add_url_rule('/report/<id>/json_report_object/<object_name>/', view_func=ReportResource().get_json_report_object, methods=['GET'], endpoint='json_report_object')
api_blueprint.apispec.add_path(path='/report/{id}/json_report_object/{object_name}/', view=ReportResource.get_json_report_object)
api_blueprint.add_url_rule('/report/<id>/raw_report_object/<object_name>/', view_func=ReportResource().get_raw_report_object, methods=['GET'], endpoint='raw_report_object')
api_blueprint.apispec.add_path(path='/report/{id}/raw_report_object/{object_name}/', view=ReportResource.get_raw_report_object)
