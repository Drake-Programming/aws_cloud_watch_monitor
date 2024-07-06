import urllib3
import json

http = urllib3.PoolManager()


def handler(event, context):
    print('calling discord!!!')
    url = "https://discord.com/api/webhooks/1259053918583914579/bib6HI-ClmpH2azKi6QuwY8qpZO2U6IfDXxOhtWj6Ahzr0ObMBkO1KbT9LhTZdD28G-N"
    msg = {
        "content": event['Records'][0]['Sns']['Message'],
    }

    encoded_msg = json.dumps(msg).encode('utf-8')
    headers = {
        'Content-Type': 'application/json'
    }
    resp = http.request('POST', url, body=encoded_msg, headers=headers)
    print({
        "message": event['Records'][0]['Sns']['Message'],
        "status_code": resp.status,
        "response": resp.data
    })
