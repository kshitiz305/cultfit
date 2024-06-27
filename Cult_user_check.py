#codementor.py

import requests
import datetime
import time
import uuid
from pytz import timezone
import logging



logging.basicConfig(filename='app.txt', level=logging.INFO, format='%(asctime)s - %(message)s')



import json
import os

# Function to load data from JSON file
def load_data_from_json(json_file):
    data = []
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
    return data

# Function to append or update data in JSON file
def append_or_update_data(json_file, new_data):
    data = load_data_from_json(json_file)
    
    # Check if an entry with the same 'name' already exists, update it; otherwise, append new data
    updated = False
    for entry in data:
        if entry['name'] == new_data['name']:
            entry.update(new_data)  # Update existing entry
            updated = True
            break
    
    if not updated:
        data.append(new_data)  # Append new entry if 'name' doesn't exist
    
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Data appended/updated in {json_file}:")






cookies = {
    '_cacc':
    'b1b1c3ed5ab7b193012bd9be0ccbc9e4177cbae14c7f3303e7037c4469eb90b5df71b5204ec65de792c939af092845c151dd',
    '_lgn': '1',
}

headers = {
    'x-access-token':
    'b1b1c3ed5ab7b193012bd9be0ccbc9e4177cbae14c7f3303e7037c4469eb90b5df71b5204ec65de792c939af092845c151dd',
    'Accept': 'application/json, text/plain, */*',
    'x-requested-from': 'cm-mobile',
    # 'Cookie': '_cacc=b1b1c3ed5ab7b193012bd9be0ccbc9e4177cbae14c7f3303e7037c4469eb90b5df71b5204ec65de792c939af092845c151dd; _lgn=1',
    'Accept-Language': 'en-us',
    'User-Agent': 'Codementor/2 CFNetwork/1220.1 Darwin/20.3.0',
    'Connection': 'keep-alive',
}

from flask import Flask

app = Flask(__name__)




def get_interested_sent_list():
  response_ = requests.get(
      'https://api.codementor.io/api/v2/requests/search?search_type=interested',
      cookies=cookies,
      headers=headers)
  response__ = requests.get(
      f"https://api.codementor.io/api/v2/requests/search?before_timestamp={response_.json()[14]['created_at']}&search_type=interested",
      cookies=cookies,
      headers=headers)
  response_1 = requests.get(
      f"https://api.codementor.io/api/v2/requests/search?before_timestamp={response__.json()[14]['created_at']}&search_type=interested",
      cookies=cookies,
      headers=headers)

  first_list = [i["random_key"] for i in response_.json()]
  # response_.json()[14]['created_at']
  first_list.extend([i["random_key"] for i in response__.json()])
  first_list.extend([i["random_key"] for i in response_1.json()])
  logging.info("Intrested Fetched")
  return set(first_list)


def send_interest(random_key,user_name,details):
    import ai_message_maker   
    my_message = ai_message_maker.get_the_ai_message(user_name, details)
#     json_data = {
#         'message': f'''Hi {user_name},
# After conducting a thorough investigation, we have determined that the root cause of the can be solved after a short discussion and guidance through a session. So, I propose the connect to solve the issues.
# If you have any further questions, please do not hesitate to contact us.''',
#     }
    my_message = my_message['candidates'][0]['content']['parts'][0]['text']
    json_data = {'message':f"""{my_message}"""}

    response = requests.post(
        f'https://api.codementor.io/api/v2/requests/{random_key}/interests',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    logging.info(f"Interest messgage sent to {user_name} at {str(datetime.datetime.now())} with {my_message}")
    return response.status_code


def send_message(user_name_id, user_name):
  json_data = {
      'message': {
          'content':
          # f'Hi {user_name}, \nI am confident that I am the best candidate for your project. My extensive experience and skills in the field make me uniquely qualified to deliver exceptional results. I have a proven track record of successfully completing projects within budget and on time, while consistently exceeding client expectations. My attention to detail and ability to think outside the box ensure that I consistently deliver innovative solutions. In addition, I am a strong communicator and work well in collaborative environments. I am dedicated to building long-term relationships with clients and always strive to exceed their expectations. I would love the opportunity to discuss the project in more detail and show you why I am the best choice for your project. I look forward to hearing from you soon. Sincerely, Kshitiz',
          f'Hi {user_name}, \n Please do let me know more about the project ',
        'type': 'message',
          'request': {
              'temp_message_id': str(uuid.uuid4()),
          },
      },
  }

  response = requests.post(
      f'https://api.codementor.io/api/v2/chats/messages/{user_name_id}',
      cookies=cookies,
      headers=headers,
      json=json_data,
  )
  logging.info(f'Message sent to {user_name_id}')
  return response.status_code



# https://api.codementor.io/api/v2/requests/search?search_type=interested
# sent_interested_list = get_interested_sent_list()
def get_employee():
    
    headers = {
        'clientversion': '10.23',
        'user-agent': 'CureFit/34822 CFNetwork/1220.1 Darwin/20.3.0',
        'appsource': 'flutter',
        'microappversion': '4.0.0',
        'deviceid': '38F0B58C-5117-4006-B965-986DA31E2580',
        'encrypteddeviceid': 'LUqg1YAYkri%2B9VwVUR5lFf5PYlR4BTBId0q6YgVieq6wRyzKpVp1MngpB7RGQwBy%0D%0A0GqFJK2x9S2bLX%2BgAH7NevD9urSLGTTGSc0reE%2BYYI%2BzeGX99NDXUGMUKbGreNC2%0D%0A4ucxklYBPrFEFsJHL8GeTHKCGtpWmiafqxhgtw03%2BvkkyvkyAf5IOVAgKKk9K8eH%0D%0A8UxGfm6roGKZxjfxjrb95GuFHbfAk9Ymh3Yq5MCb0LH4jABDPxgnKd0DSnQgLLMY%0D%0Ad6DaBdo0MupFZWiK2VGXmYaAXaiGZeur66zwnRkkJFtaHJhjNw8ZlmtLNWaRgpEP%0D%0AHVpbNxxEp5kPKFDpO9GncC4QbnNDw4tfqLM9HYs9dD%2BSCTjKwMj4xGx2TZiG1yCf%0D%0A4jY%2FvkjEu5lyTL3JhY%2B3D7YjhZgkLWOSPMkMfG%2Bpa7B1NqQwOedOEIUhaa6Cc8m2%0D%0A%2FiIP7HQl8xxhgJBxZwZR35Yyi8o00fnWYQA7kZfHTsBvvDdrsZ6BKtY%2BcbeSRx6p%0D%0AVHX7chUY7rRoLkLKYTfRl4MQncAVtH4aEuOH3MgdN4kmj9U8s5ZRqAfWzwwkJUYd%0D%0A3Bk46zf9ny102RwiUHjs2ZuMHRbqwg3esmC8cv0pL6PQ8lDzkqwrx7QJsvdBFmHW%0D%0AD2QMKo5VFBiu6gydc7uNyZ32xJ16zZs0i6cJTfsqPGQ%3D',
        'devicemodel': 'iPhone',
        'accept-language': 'en-us',
        'timezone': 'IST',
        'x-tenant-id': 'curefit',
        'at': 'CFAPP:1a60af56-fc73-40e2-8fb3-31c03f874e24',
        'accept': 'application/json',
        'content-type': 'application/json; charset=utf-8',
        'devicebrand': 'apple',
        'x-request-id': '256db110-71b7-0a90-4271-ebb3ca99fb70',
        'osname': 'ios',
    }
    #2767938
    #93309548 Yamini
    #30738421 Unknown
    params = {
        'cultUserId': '2767938',#Akriti
    }

    response = requests.get('https://www.cult.fit/api/v2/community/profile', params=params, headers=headers)

    res = response.json()
    json_file = "data.json"

    with open(json_file, 'r') as f:
        final_data = json.load(f)

    # New data to append or update
    for i in final_data:
        if res['widgets'][0]['classesAttended'] > i['count']:
            i['time'].append(datetime.datetime.now(timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S.%f'))
            new_data1 = {"name":res['widgets'][0]['name'],"count":res['widgets'][0]['classesAttended'],"time":i['time']}  # Update existing entry

            # Append or update new data
            append_or_update_data(json_file, new_data1)

            # Read and print final data from JSON file
            with open(json_file, 'r') as f:
                final_data = json.load(f)
            
            print("\nFinal data in JSON file:")
            print(final_data)


    

def main():

  response = requests.get(
      'https://api.codementor.io/api/v2/requests/search?search_type=related',
      cookies=cookies,
      headers=headers)
  notification_data = response.json()
  for i in range(notification_data.__len__()):
    # https://api.codementor.io/api/notifications/summary
    # latest_updatetime = 1699263813
    if notification_data[i]['random_key'] not in sent_interested_list:
      # latest_updatetime = notification_data[i]['created_at']
      random_key = notification_data[i].get('random_key')
      send_interest(random_key, notification_data[i]['user']['name'],notification_data[0]['title'])
      time.sleep(5)
      # send_message(notification_data[i]['user']['username'],
                   # notification_data[i]['user']['name'])
      sent_interested_list.add(notification_data[i]['random_key'])

    else:
      pass
      # logging.info(f"Skipped {notification_data[i]['random_key']}")


# while True:
#   main()

@app.route('/parkplus', methods=['GET'])
def park_plus():
    headers = [{
    'authority': 'parkplus-gamification.parkplus.io',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'app-name': 'Park+ PWA',
    'authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTI5ODkyMTUsInN1YiI6Ijg2MjYxOTIiLCJ1bmlxdWVfaWQiOiJTVlNVZ3ZLZWZSaVdSUHRidG1EV0ZRaEpNbmt3c3R5ZllHbFJXUlBZWE5Id2poRlRYV1lKRllZdm9tWlVvZWJTIiwiaHR0cHM6Ly9wYXJrd2hlZWxzLmNvLmluLyI6eyJ1c2VyX2lkIjo4NjI2MTkyLCJuYW1lIjoiS3NoaXRpeiBndXB0YSIsImVtYWlsIjoiIiwicGhvbmVfbnVtYmVyIjoiODg4Mjk2MTUxNyIsInJvbGUiOiJjbGllbnQiLCJkZXZpY2VfaWQiOiIiLCJ2ZXJzaW9uIjo0fX0.a-EN19jR6VC0YPJmsI-QI2c0uAn3nv-wU-DBXdbXttI',
    'cache-control': 'no-cache',
    'client-id': '8186c1be-660f-428c-93a7-6480c2d8af66',
    'client-secret': 'hjjh0uw8c3j7vw5jgba8',
    'origin': 'https://parkplus.io',
    'package-name': 'web.pwa',
    'platform': 'web',
    'pragma': 'no-cache',
    'referer': 'https://parkplus.io/',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
},{
    'authority': 'parkplus-gamification.parkplus.io',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTI5OTAyNTUsInN1YiI6IjE0MzkxNDgzIiwidW5pcXVlX2lkIjoiYWVJWE5qSm9Ia3d4THVDd05XWFRJUmV5YWlXZ2xUeUx4c0tHT3JEZ1RTd2lMcmRLWnh1YnJrRkZzUW5pWm9CUCIsImh0dHBzOi8vcGFya3doZWVscy5jby5pbi8iOnsidXNlcl9pZCI6MTQzOTE0ODMsIm5hbWUiOiIgIiwiZW1haWwiOiJLc2hpdGl6MzA1QGdtYWlsLmNvbSIsInBob25lX251bWJlciI6IjkzMTU4NTIwNjkiLCJyb2xlIjoiY2xpZW50IiwiZGV2aWNlX2lkIjoiIiwidmVyc2lvbiI6NH19.aOH7z5Ec8DI6MojFcwYAch80evVsAfoEE8G8nzsZR5g',
    'cache-control': 'no-cache',
    'client-id': '8186c1be-660f-428c-93a7-6480c2d8af66',
    'client-secret': 'hjjh0uw8c3j7vw5jgba8',
    'native-platform': 'PWA',
    'origin': 'https://parkplus.io',
    'platform': 'web',
    'referer': 'https://parkplus.io/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'version-name': '[object Object]',
}]

    params = {
        'reward_group_id': '1',
        'use_wallet': 'true',
        'latitude': '',
        'longitude': '',
    }

    def method_call(i):
        if i == 3:
            params['use_wallet'] = 'false'
        else:
            params['use_wallet'] = 'true'

        response = requests.get('https://parkplus-gamification.parkplus.io/api/v1/spin-the-wheel/spin', params=params,
                                headers=header)
        if response.status_code == 200:

            logging.info(response.json().get('data')['reward_result']['metadata']['title'])
        else:
            logging.info(response.json()['message'])

    for header in headers:

        for i in range(4):
            method_call(i)
    header = [{
        'authority': 'parkplus-gamification.parkplus.io',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MDgxNTczMzcsInN1YiI6IjE0MzkxNDgzIiwidW5pcXVlX2lkIjoiUlprQWNoQ1VBZFFPQm1tSG1SV3VZRUJYcnRURmd0dmRvSmVoRnJKeURsZ2NxT0RXcGJ0UHZUWXJkU2JNekJGQSIsImh0dHBzOi8vcGFya3doZWVscy5jby5pbi8iOnsidXNlcl9pZCI6MTQzOTE0ODMsIm5hbWUiOiIgIiwiZW1haWwiOiJLc2hpdGl6MzA1QGdtYWlsLmNvbSIsInBob25lX251bWJlciI6IjkzMTU4NTIwNjkiLCJyb2xlIjoiY2xpZW50IiwiZGV2aWNlX2lkIjoiIiwidmVyc2lvbiI6NH19.uYPEJreArPZWaC0lzeUrEJQrEhXarB9l_deRXEHNUZY',
        'cache-control': 'no-cache',
        'client-id': '8186c1be-660f-428c-93a7-6480c2d8af66',
        'client-secret': 'hjjh0uw8c3j7vw5jgba8',
        'native-platform': 'PWA',
        'origin': 'https://parkplus.io',
        'platform': 'web',
        'referer': 'https://parkplus.io/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'version-name': '[object Object]',
    }, {
        'authority': 'parkplus-gamification.parkplus.io',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MDg0NzI2OTYsInN1YiI6Ijg2MjYxOTIiLCJ1bmlxdWVfaWQiOiJ1WmlEQ2tQVk1tSXpMTkRuR1VQRVdrWGp6clZtRUJpd0xJbFdoZVZNUkV2YnFQeGpoZk5WRHJ3ck9CS1RmY1d6IiwiaHR0cHM6Ly9wYXJrd2hlZWxzLmNvLmluLyI6eyJ1c2VyX2lkIjo4NjI2MTkyLCJuYW1lIjoiS3NoaXRpeiBndXB0YSIsImVtYWlsIjoiIiwicGhvbmVfbnVtYmVyIjoiODg4Mjk2MTUxNyIsInJvbGUiOiJjbGllbnQiLCJkZXZpY2VfaWQiOiIiLCJ2ZXJzaW9uIjo0fX0.4kvdMVg1iLk3RLfwAq_22n4EvXQHiPqtRJ5KwPKwDrU',
        'cache-control': 'no-cache',
        'client-id': '8186c1be-660f-428c-93a7-6480c2d8af66',
        'client-secret': 'hjjh0uw8c3j7vw5jgba8',
        'native-platform': 'PWA',
        'origin': 'https://parkplus.io',
        'platform': 'web',
        'referer': 'https://parkplus.io/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'version-name': '[object Object]',
    }]

    for headers in header:
        params = {
            'is_played': 'true',
        }
        question = 1
        response = requests.get('https://social-community.parkplus.io/api/v3/user/quiz', params=params, headers=headers)
        a = response.json()
        for i, j in response.json()['data']['question_map'].items():
            logging.info(j['question_text'])
            counter = 0
            for dictionary in j["options"]:
                counter += 1
                if dictionary["id"] == str(j['correct_option_id']):
                    logging.info(f'{counter, dictionary["option_text"]}')
                    break

            json_data = {
                'quiz_id': a['data']['quiz_id'],
                'question_index': question,
                'question_id': i,
                'selected_option_id': dictionary['id'],
                'selected_option_text': dictionary['option_text'],
                'is_last_question': False if question < 5 else True,
            }

            response = requests.post('https://social-community.parkplus.io/api/v3/user/submit-answer', headers=headers,
                                     json=json_data)
            question += 1
            logging.info(response.json())
    return "Park Plus ran successfully"

@app.route('/cron2', methods=['GET'])
def endpoint():
    get_employee()
    logging.info(
      f" {datetime.datetime.now(timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S.%f')}"
  )
    return "This is the / endpoint."

@app.route('/', methods=['GET'])
def cron_endpoint():
  logging.info('cron triggered')
  while True:
    # main()
    get_employee()
    time.sleep(1800)
    logging.info(
      f"rolled once {datetime.datetime.now(timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S.%f')}"
  )
  return "This is the /api/cron endpoint."

@app.route('/logs')
def view_logs():
    with open('app.txt', 'r') as log_file:
        logs = log_file.read()
    return '<pre>' + logs + '</pre>'

if __name__ == '__main__':
    # app.run(port=5002)
    while True:
    # main()
        get_employee()
        time.sleep(1800)


