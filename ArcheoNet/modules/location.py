import streamlit_js_eval


def get_geolocation():
	getgeolocation = """
	new Promise((resolve, reject) => {
	  navigator.geolocation.getCurrentPosition(
		pos => resolve({
		  latitude: pos.coords.latitude,
		  longitude: pos.coords.longitude,
		  accuracy: pos.coords.accuracy,
		  error: null
		}),
		err => resolve({
		  latitude: 0.00,
		  longitude: 0.00,
		  accuracy: 0.00,
		  error: err.message
		})
	  );
	});
	"""

	loc = (streamlit_js_eval(js_expressions=getgeolocation))

	try:
		latitude = loc["latitude"]
		longitude = loc["longitude"]
		if latitude == 0 and longitude == 0:
			latitude = None
			longitude = None
	except:
		latitude = None
		longitude = None
		print("Location data is unavatible")

	return latitude, longitude