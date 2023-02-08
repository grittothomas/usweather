from flask import Flask, request
from flask_restx import Api, Resource, fields
import psycopg2
import json
from flask import jsonify

app = Flask(__name__)
api = Api(app, version='1.0', title='Weather API',
          description='A weather API that retrieves data from a PostgreSQL database',
          doc='/api/docs/')

# Define the model for weather data
weather_data = api.model('WeatherData', {
    'date': fields.String(required=True, description='Date of weather data in format "YYYY-MM-DD"'),
    'station': fields.String(required=True, description='Name of the weather station'),
    'max_temp': fields.Float(required=True, description='Maximum temperature'),
    'min_temp': fields.Float(required=True, description='Minimum temperature'),
    'precipitation': fields.Float(required=True, description='Precipitation')
})

@api.route("/api/weather")
class Weather(Resource):
    @api.doc(params={'date': 'Date of weather data in format "YYYY-MM-DD"',
                     'station': 'Name of the weather station',
                     'page': 'Page number for pagination',
                     'per_page': 'Number of items per page for pagination'})
    @api.marshal_list_with(weather_data)
    def get(self):
        """
        Endpoint for retrieving weather data.
        
        Returns:
            List of weather data in the format:
                [{
                    "date": "YYYY-MM-DD",
                    "station": "station name",
                    "max_temp": max_temp,
                    "min_temp": min_temp,
                    "precipitation": precipitation
                }, ...]
        """
        conn = psycopg2.connect(
            host="localhost",
            database="weather_data",
            user="postgres",
            password="password"
        )
        cursor = conn.cursor()

        date = request.args.get("date")
        station = request.args.get("station")
        page = request.args.get("page")
        per_page = request.args.get("per_page")

        params = []
        query = "SELECT date, station, max_temp, min_temp, precipitation FROM weather_data WHERE date IS NOT NULL"

        if date:
            query += " AND date = %s"
            params.append(date)

        if station:
            query += " AND station = %s"
            params.append(station)

        if page and per_page:
            query += " LIMIT %s OFFSET %s"
            params.append(per_page)
            params.append((int(page) - 1) * int(per_page))

        cursor.execute(query, params)
        result = cursor.fetchall()

        weather_data_list = []
        for row in result:
            weather_data_list.append({
                "date": row[0].strftime("%Y-%m-%d"),
                "station": row[1],
                "max_temp": row[2],
                "min_temp": row[3],
                "precipitation": row[4]
            })
        return jsonify(weather_data_list)
    
if __name__ == "__main__":
    app.run(debug =True)