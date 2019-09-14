import json
import sys
from os.path import join, dirname
from jsonschema import validate
import glob

def assert_valid_schema(data, schema_file):

    schema = _load_json_schema(schema_file)
    validate(data,schema)


def _load_json_schema(filename):

    relative_path = join('schema', filename)
    absolute_path = join(dirname(__file__), relative_path)

    with open(absolute_path) as schema_file:
        return json.loads(schema_file.read())                    

def filename():
    for filename in glob.glob(sys.argv[2]):
        with open(filename) as schema2_file:
            json_data = json.loads(schema2_file.read())
            return json_data

def test_validate_json():
    file = filename()
    assert_valid_schema(file, 'validate.json')         

def test_transaction():
    file = filename()
    if file['transaction'] < 0:
        assert False

def test_card_lenght():
    file = filename()
    if len(str(file['card_number'])) != 16:
        assert False  