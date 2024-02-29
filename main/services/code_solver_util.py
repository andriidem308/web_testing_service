import json


def read_json_s3(file_field):
    try:
        file_content = file_field.open(mode='r')
        file_content_str = file_content.read()
        return json.loads(file_content_str)

    except Exception as e:
        print("Error while reading test file on S3:", e)
        return None

def read_json_local(file_path):
    with open(file_path) as tests_file:
        return json.load(tests_file)