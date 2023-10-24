import json
import os
import re
import sys
from django.core.wsgi import get_wsgi_application
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + '/app')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()
from api.models import Answer


def json_to_dict(data, inPath):
    with open(os.path.join(inPath, data), 'r', encoding='utf-8') as infile:
        load_data = json.load(infile)
    return load_data


def dict_to_json(data, filename, outPath):
    with open(os.path.join(outPath, filename), 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent='\t', ensure_ascii=False)


def upload_data(path):
    with open(path, 'r', encoding='UTF-8') as f:
        dataset = json.load(f)
        for key in dataset.keys():
            data = dataset[key]
            for q in data['query']:
                output = {'type': 'simpleText', 'text': re.sub('[.] ', '.\n', data['answer'])}
                if data['link'] or data['image']:
                    items = []
                    if data['image']:
                        items.append({'type': 'image', 'src': data['image']})
                    if data['link']:
                        items.append({'type': 'buttons', 'items': [{'label': '바로가기', 'action': 'webLink', 'webLinkUrl': data['link']}]})
                    output['items'] = items
                Answer.objects.create(input=data['question'], output=[output], query=q)


def upload_origin(path):
    with open(path, 'r', encoding='UTF-8') as f:
        dataset = json.load(f)
        for data in dataset:
            for q in data['query']:
                Answer.objects.create(input=data['input'], output=data['output'], query=q)


def change_format():
    dataset = []
    answers = Answer.objects.all()
    for answer in answers:
        dataset.append({'input': answer.input, 'output': answer.output, 'query': answer.query})
    return dataset


def change_format2():
    dataset = {}
    answers = Answer.objects.all()
    for answer in answers:
        if answer.input in dataset:
            if len(dataset[answer.input]['output']) < len(answer.output):
                dataset[answer.input]['output'] = answer.output
            dataset[answer.input]['query'].append(answer.query)
        else:
            dataset[answer.input] = {'output': answer.output, 'query': [answer.query]}
    return dataset


def download(filename, outPath):
    dataset = change_format()
    dict_to_json(dataset, filename, outPath)


def upload(data, inPath):
    dataset = json_to_dict(data, inPath)
    for data in dataset:
        Answer.objects.create(input=data['input'], output=data['output'], query=data['query'])


def data(path):
    with open(path, 'r', encoding='UTF-8') as f:
        dataset = json.load(f)
        for key in dataset.keys():
            data = dataset[key]
            print(data['location'])


def save_data(dataset, key):
    data, query = dataset[key], dataset[key]['query']
    if type(query) == list:
        query.append(data['classification'])
    else:
        query = [query, data['classification']]
    for q in query:
        output = {'type': 'simpleText', 'text': re.sub('[.] ', '.\n', data['answer'])}
        if data['link'] or data['image']:
            items = []
            if data['image']:
                items.append({'type': 'image', 'src': data['image']})
            if data['link']:
                items.append({'type': 'buttons', 'items': [{'label': '바로가기', 'action': 'webLink', 'webLinkUrl': data['link']}]})
            output['items'] = items
        Answer.objects.create(input=data['question'], output=[output], query=q)


def combine_data(data, inPath, outPath):
    combine = {}
    for file in os.listdir(inPath):
        combine.update(json_to_dict(file, inPath))
    dict_to_json(combine, data, outPath)


def upload_data2(data, inPath):
    dataset = json_to_dict(data, inPath)
    dic = {}
    for key in dataset.keys():
        save_data(dataset, key)
        classification = dataset[key]['classification'].split('/')
        for i in range(0, len(classification) - 1):
            key, item = '/'.join(classification[:i + 1]), '/'.join(classification[:i + 2])
            if not key in dic:
                dic[key] = [item]
            else:
                if not item in dic[key]:
                    dic[key].append(item)
    for key in dic.keys():
        output = [{"type": "simpleText", "text": ' - '.join(key.split('/'))}]
        buttons = []
        for data in dic[key]:
            buttons.append(
                {"label": data.split('/')[-1], "action": "message", "messageText": data, "messageLabel": True})
        output.append({"type": "buttons", "items": buttons})
        Answer.objects.create(input=key, output=output, query=key)


def update(filename, path):
    dataset = json_to_dict(filename, path)
    for data in dataset:
        output = data['output']
        d = output[0]
        if d['type'] == 'simpleText':
            d['type'] = 'cardText'
            d['title'] = data['input']
            output[0] = d
            data['output'] = output
    dict_to_json(dataset, filename, path)

def update2(filename, path):
    dataset = json_to_dict(filename, path)
    for data in dataset:
        query = data['query']
        if len(query) > 1:
            data['query'] = query[:-1]
    dict_to_json(dataset, filename, path)

def check(filename, path):
    dataset = json_to_dict(filename, path)
    datas = []
    for data in dataset:
        inp = data['input']
        if inp in datas:
            print(inp)
        else:
            datas.append(inp)
# download(change_format())
# upload_origin('dataset/example.json')
# upload_data('dataset/chatbot_made.json')
# combine_data('chatbot_data.json', 'dataset/chatbot', 'dataset')
# upload_data2('chatbot_data.json', 'dataset')
# download('db.json', 'dataset')
# update2('db.json', 'dataset')
upload('db.json', 'dataset')
# check('db.json', 'dataset')
