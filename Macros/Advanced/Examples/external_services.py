# Name: Discord/PushBullet send message
# Description: Example functions to send message to Discord/PushBullet
# Author: Reetus
# Era: Any

import clr
clr.AddReference('System.Net.Http')
from System.Net.Http import HttpClient, FormUrlEncodedContent
from System.Net.Http.Headers import AuthenticationHeaderValue
from System.Collections.Generic import Dictionary

def Discord(message):
	webhook = '<webhook url here>'
	dict = {"content": message}
	response = HttpClient().PostAsync( webhook, FormUrlEncodedContent(Dictionary[str,str](dict)))
	return response.Result.IsSuccessStatusCode

def PushBullet(title, message):
	# generate access token @ https://www.pushbullet.com/#settings/account
	accessToken = '<access token here>'
	http = HttpClient()
	dict = {"type": "note", "title":title, "body": message}
	http.DefaultRequestHeaders.Authorization = AuthenticationHeaderValue( "Bearer", accessToken );
	response = http.PostAsync( "https://api.pushbullet.com/v2/pushes", FormUrlEncodedContent(Dictionary[str,str](dict)))
	return response.Result.IsSuccessStatusCode
	
print Discord('hello')
print PushBullet('title', 'hello')
