import requests
from bs4 import BeautifulSoup as bs
import json
import configparser as cfg

#get api key to openweathermap
def get_key_from_config_file(config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'key')

#get ip address
def get_ip_address():
    ip_url = "http://checkip.dyndns.org/"
    html_page = requests.get(ip_url).content
    content = bs(html_page, "html.parser")
    ip = content.find('body').getText().split(": ")[1]
    print(ip)
    return ip

#get city
def get_city(ip):
    city_url = "http://ipinfo.io/" + str(ip) + "/json"
    json_data = requests.get(city_url).content
    data = json.loads(json_data)
    city = data['city']
    print(city)
    return city


#get weather
def get_weather(city, key):
        weather_endpoint = "http://api.openweathermap.org/data/2.5/weather?q="
        weather_url = weather_endpoint + str(city) + "&appid=" + str(key)
        weather_json = requests.get(weather_url).content
        weather_data = json.loads(weather_json)
        weather = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        #conver temperature unit from Kelvin to Celsius
        temp = float(weather_data['main']['temp'] - 273.15)
        msg = "City: " + str(city) + "\nWeather: " + str(weather) + "\nDescription: " + str(description) + "\nTemperature: " + str(temp)
        return msg

if __name__ == '__main__':
    ip = get_ip_address()
    city = get_city(ip)
    key = get_key_from_config_file('config.cfg')
    msg = get_weather(city, key)
    print(msg)