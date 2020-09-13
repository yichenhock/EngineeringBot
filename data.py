import asyncio
import json
import os
from os import getenv
from dotenv import load_dotenv
from random import sample
import boto3
import decimal

from constants import DATA_PATH, MAX_LECTURER_LEVEL

data = {}
_data_files = {}
load_dotenv()
boto_kwargs = {
    "aws_access_key_id": getenv("AWS_ACCESS_KEY_ID"),
    "aws_secret_access_key": getenv("AWS_SECRET_ACCESS_KEY"),
    "region_name": getenv("AWS_REGION")

}


async def saveloop():
    while True:
        save_data()
        await asyncio.sleep(10)


def replace_decimals(obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj:
            obj[k] = replace_decimals(obj[k])
        return obj
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj

def replace_floats(obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = replace_floats(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj:
            obj[k] = replace_floats(obj[k])
        return obj
    elif isinstance(obj, float):
        return decimal.Decimal(obj)
    else:
        return obj

def load_data(bot):
    global data
    # checks if data file exist, if not, writes an empty dict to it
    # if os.path.exists(DATA_PATH+"data.json"):
    #     with open(DATA_PATH+"data.json", "r") as json_file:
    #         data = json.load(json_file)
    # else:
    #     data = {}
    #
    dynamodb = boto3.Session(**boto_kwargs).resource("dynamodb")
    table = dynamodb.Table('data')
    try:
        response = table.get_item(Key={'id': "data"})
    except ClientError as e:
        print(e.response['Error']['Message'])
        data = {}
    else:
        data = replace_decimals(response["Item"]["data"])
    # print(data)
    bot.loop.create_task(saveloop())


def add_data(*keys):
    """Add or insert a data entry."""

    keys, value = keys[:-1], keys[-1]

    current_dict = data
    for key in keys[:-1]:
        key = str(key)
        if not key in current_dict:
            current_dict[key] = {}
        current_dict = current_dict[key]

    key = str(keys[-1])
    if isinstance(current_dict, dict):
        current_dict[key] = value
    save_data()

def get_data(*keys, default_val=None):
    """Get a data entry."""
    current_dict = data
    for key in keys[:-1]:
        key = str(key)
        if not key in current_dict:
            return default_val
        current_dict = current_dict[key]

    key = str(keys[-1])
    if isinstance(current_dict, dict):
        return current_dict.get(key, default_val)
    else:
        return default_val

def save_data():
    # with open(DATA_PATH+'data.json', 'w') as outfile:
    #     json.dump(data, outfile, sort_keys=True, indent=4)
    dynamodb = boto3.Session(**boto_kwargs).resource("dynamodb")
    table = dynamodb.Table('data')
    response = table.put_item(Item={"id":"data",
                          "data": replace_floats(data)})

def _get_from_filename(filename, default = None, cached=True):
    """Starts with an underscore to signify this should only be used in this file."""
    if not filename in _data_files or not cached:
        dynamodb = boto3.Session(**boto_kwargs).resource("dynamodb")
        table = dynamodb.Table('data')
        try:
            response = table.get_item(Key={'id': filename})
        except ClientError as e:
            print(e.response['Error']['Message'])
            _data_files[filename] = default
            return _data_files[filename]
        if response.get("Item"):
            _data_files[filename] = replace_decimals(response["Item"]["data"])
        else:
            _data_files[filename] = default
    return _data_files[filename]


def get_items():
    return _get_from_filename("items", [])

def get_labs():
    return _get_from_filename("labs", [], cached=False)

def get_lecturers():
    return _get_from_filename("lecturers", [])

def get_main_questions():
    return _get_from_filename("main_questions", [], cached=False)

def get_trivia_questions_data():
    return _get_from_filename("trivia_questions", [], cached=False)

def get_labs_subset(n):
    labs = get_labs()
    return sample(labs, min(n, len(labs)))
