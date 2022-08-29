from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import json
from datetime import datetime

db_connect = create_engine('postgresql://postgres:admin@localhost:5432/postgres')
app = Flask(__name__)
api = Api(app)


class IncidentsByReportDate(Resource):
    def get(self):
        conn = db_connect.connect()
        date_from = request.args.get('date_from') or f"'1900-01-01'"
        date_to = request.args.get('date_to') or f"'{datetime.now().date()}'"
        page = request.args.get('page')
        try:
            page = 0 if page is None else int(page) - 1
            query = conn.execute(
                f"select * from police_department_calls_for_service where report_date between {date_from} and {date_to}"
                f" LIMIT 20 OFFSET {20 * page};"
            )
        except:
            return "BAD_REQUEST", 400
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return json.dumps(result, default=str)


api.add_resource(IncidentsByReportDate, '/incidents')

if __name__ == '__main__':
    app.run()

# http://127.0.0.1:5000/incidents?date_from='2016-04-01'&date_to='2016-04-01'&page=2 - request example
