import json, requests

accessKey = "386e706b6b578eb577ddc54331311c64";

def getWeather(cityname):
	with open('city.list.json') as cityList:
		cities = json.load(cityList);
		cityid = [c['id'] for c in cities if c['name'].lower() == cityname.lower()];
		# print cityid;
		if len(cityid):
			cityid = cityid[0];
			# print cityid
			url = 'http://api.openweathermap.org/data/2.5/weather?id=' + str(cityid) + '&appid=' + accessKey;
			resp = requests.get(url=url, params={});
			data = json.loads(resp.text);
			# print data
			# resp = None;
			# returnVal = data;
			
			return 'Its ' +  data['weather'][0]['description'] + ' with temperature ' + str(data['main']['temp'] - 273) + ' Degrees Celsius.';
		else:
			return 'Weather data is not available for your location!';

# def getWeather(cityname):
# if __name__ == '__main__':
# 	weatherData = getWeather('lahore');
# 	print 'Its ' +  weatherData['weather'][0]['description'] + ' with temperature ' + str(weatherData['main']['temp']);