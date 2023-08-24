from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import certifi
from datetime import datetime
import hashlib
import requests
from bs4 import BeautifulSoup



headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/ 537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/ 537.36'}
url = "https://www.instagram.com/whynotcoffee.id/"
data = requests.get(url, headers=headers)

req = data.text
soup = BeautifulSoup(req,'html.parser')

body_div = soup.select('body > div')
second_div = body_div[1]['id']
body_div = soup.select(f'body > #{second_div}')
print(body_div)


# for contest in contests:
#     start_time = contest.select_one('.start-time')
#     titles = contest.select_one('.contest_title ')
#     if not start_time:
#         continue
#     start_time = start_time.text.strip()
#     titles = titles.text.strip()
#     print(start_time)

# password = 'admin123'
# hash_pwl = hashlib.md5(password.encode())
# password = hash_pwl.hexdigest()
# print(password)