import os
import ssl
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


class Database:
    def __init__(self):
        self.client = MongoClient(os.getenv('URI'))
        self.db = self.client['project_uni']

    def get_question_count(self, question_number=1) -> int:
        query = f'question_{question_number}'
        raw_data = self.db[query].find()
        answers = {}
        for i in raw_data:
            if i['body'] in list(answers.keys()):
                answers[i['body']] += 1
            else:
                answers[i['body']] = 1

        return answers
    def upload_question(self, question_number=1, answer=''):
        query = f'question_{question_number}'
        response = self.db[query].insert_one({"body" : answer})
        print(response)

if __name__ == "__main__":
    my_db = Database()
    print(my_db.get_question_count(1))