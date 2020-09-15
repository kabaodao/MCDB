import requests
import json
import base64
import boto3
import os


file_path = "json/command_usagetime.json"
s3 = boto3.resource(
    's3',
    region_name='ap-northeast-1',
    aws_access_key_id=os.environ["AWS_S3_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_S3_SECRET_ACCESS_KEY"]
)


# mojang_api_url class
class mojang_api_url():
    def __init__(self, mciduuid):
        self.mciduuid = mciduuid

    def mcid_to_uuid(self):
        if len(self.mciduuid) > 16:
            return self.mciduuid
        else:
            UserUrl = f"https://api.mojang.com/users/profiles/minecraft/{self.mciduuid}"
            response = requests.get(UserUrl)
            UserData = response.json()
            UUID = UserData['id']
        return UUID

    def data_profile(self):
        ProfileUrl = f"https://sessionserver.mojang.com/session/minecraft/profile/{self.mciduuid}"
        response = requests.get(ProfileUrl)
        ProfileData = response.json()
        DecodeProfileData = base64.b64decode(ProfileData['properties'][0]['value']).decode()
        ReDecodeProfileData = json.loads(DecodeProfileData)
        return ReDecodeProfileData

    def data_history(self):
        HistoryUrl = f"https://api.mojang.com/user/profiles/{self.mciduuid}/names"
        response = requests.get(HistoryUrl)
        HistoryData = response.json()
        return HistoryData


# language class
class language():
    def load_language_english():
        json_open = open("json/language/en.json", "r")
        json_load = json.load(json_open)
        return json_load


# usagetime class
class usagetime():
    def upload_usagetime():
        s3.Bucket(os.environ["AWS_S3_BUCKET_NAME"]).upload_file(file_path, "command_usagetime.json")

    def load_usagetime():
        with open(file_path, "r") as f:
            data = json.load(f)

        return data

    def write_usagetime(n):
        with open(file_path, "r") as f:
            data = json.load(f)

        data[n] = data[n] + 1

        with open(file_path, "w") as f:
            json.dump(data, f)
