from flask import render_template
from . import main
from .forms import DateTimeForm
from .utils import build_query, parse_response, parse_satellite
import requests

@main.route('/',methods=['GET'])
def index():
	return render_template('index.html', title='Home')

@main.route('/calculate',methods=['GET','POST'])
def calculate():
	form = DateTimeForm()
	satellite_id = "25544" # ISS Zarya
	result = None
	if form.validate_on_submit():
		s_date_time = form.input_date_time.data
		(query, headers) = build_query(satellite_id)
		response = requests.get(query, headers=headers)
		tle_dict = parse_response(response)
		if tle_dict:
			(error, r, v) = parse_satellite(tle_dict, s_date_time)
			if error == 0:
				result = {"tle_date_time":"TLE DateTime: ", "l1":f"Position (X, Y, Z) in km: {r}", "l2":f"Velocity (dx, dy, dz) in km/s: {v}", "msg":"Satellite/space object position and velocity calculated"}
			else:
				result = {"msg":"Something went wrong. Try again."}	
		else:
			result = {"msg":"Something went wrong. Try again."}
	return render_template('calculate.html', title='Earth', form=form, result=result)