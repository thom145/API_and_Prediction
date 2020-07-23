from flask import Flask, request, abort, jsonify, render_template
from flask_restful import Resource, Api
from json import dumps
import pandas as pd
import datetime


# load the data that will be used
try:
	df_predicted = pd.read_csv("data/result/prediction.csv") # contains prediction
except FileNotFoundError as e:
    print(e.strerror)

app = Flask(__name__, template_folder="HTMLPages")
api = Api(app)

@app.route("/")
def home():
	return render_template("index.html")


class global_checks:
	global check_key
	def check_key(orva_key):
		unique_keys = list(df_predicted['key'].unique()) # get all unique keys
		# check if given key exists
		if orva_key in unique_keys:
			return True
		else:
			return False

	global check_date_format
	def check_date_format(date_text):
		try:
			datetime.datetime.strptime(date_text, '%Y-%m-%d')
		except:
			return False
		return True

	global check_date
	def check_date(date_text):
		unique_dates = list(df_predicted['created_date_formated'].unique()) # get all unique keys
		date_given = datetime.datetime.strptime(date_text, '%Y-%m-%d')
		# should be dynamic and not static....
		latest_predicted_date = datetime.datetime.strptime('2018-05-10', '%Y-%m-%d')

		if date_given < latest_predicted_date:
			return True
		else:
			return False


class error_handeling:
	def bad_request(message, orva_key):
	    response = jsonify({'status': 404,
							'message': message,
							'help': 'The key: ' + str(orva_key) + ' is not present in the database. Right Format: orva-*key_number*'})
	    response.status_code = 404
	    return response

class Fake_Result(Resource):
	def get(self, orva_key):
		"""
		Will always return the same key, which is orva-1

		return
			orva_1_results (dictionary): information (key, resolutiondate) about key orva-1
		"""
		result_orva_1 = df_predicted.loc[df_predicted['key'] == 'orva-1']
		orva_1_values = result_orva_1[['key', 'resolutiondate']]
		orva_1_results = orva_1_values.to_dict('index')
		return orva_1_results[2165]

class Prediction_Result(Resource):
	def get(self, orva_key):
		def get_prediction():
			"""
			Get the prediction for a specific key if resolutiondate is unknown
			if resoltiondate is known return resolutiondate

			return
				value (dictionary): contains the key plus prediction
			"""
			new_orva = orva_key.upper()
			if check_key(new_orva):
				result = df_predicted.loc[df_predicted['key'] == new_orva]
				if result['resolutiondate'].values[0] != '0':
					result = result[['key', 'resolutiondate']]
					key = result.index[0]
				else:
					result = result[['key', 'predicted_date']]
					key = result.index[0]
				to_dict = result.to_dict('index')
				return to_dict[key]
			else:
				return error_handeling.bad_request("Check for valuable keys", orva_key)

		value = get_prediction()
		return value

class Planning(Resource):
	def get(self, date):
		if check_date_format(date):
			if check_date(date):
				# filter data
				df_filterd = df_predicted.loc[df_predicted['created_date_formated'] <= date]
				df_filterd = df_filterd.loc[df_filterd['predicted_date_formated'] > date]


				df_filterd = df_filterd[['key', 'predicted_date']] # select columns
				df_filterd.columns = ['key', 'predicted_resolution_date'] # rename columns
				df_dict = df_filterd.to_dict('records') # from dataframe to dictionary
				return {'Date': date, 'issues': df_dict}
			else:
				return "Date Format is correct, however nothing has been planned after this date"
		else:
			return "Incorrect data format, should be YYYY-MM-DD"


# add api functionalities to API master object
api.add_resource(Fake_Result, '/issue/<string:orva_key>/resolve-fake')  # bind url identifier to class
api.add_resource(Prediction_Result, '/issue/<string:orva_key>/resolve-prediction')  # bind url identifier to class
api.add_resource(Planning, '/release/<string:date>/resolved-since-now')  # whatever the number is, multiply by 2

if __name__ == '__main__':
    app.run(debug=True)
