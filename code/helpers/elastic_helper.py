import json
import os
from typing import List
from elasticsearch import Elasticsearch

class ElasticSearchHelper:
    @staticmethod
    def get_users_ids_with_steps(vivanta_user_ids: List[int]) -> dict:
        elastic_string = os.environ.get('ELASTIC_ENDPOINT') + ":" + os.environ.get('ELASTIC_PORT')
        es = Elasticsearch(elastic_string, api_key=os.environ.get('ELASTIC_KEY')) 

        query_file_path = "code/elastic_request.json"
        with open(query_file_path, 'r', encoding='utf-8') as file:
            query = json.load(file)
        query["query"]["bool"]["must"][0]["terms"]["vivanta_user_id"] = vivanta_user_ids
        index_name = os.environ.get('ELASTIC_HEALTH_DATA_INDEX')
        response = es.search(index=index_name, body=query)
        user_ids = []
        for bucket in response['aggregations']['id_unique_users']['buckets']:
            user_ids.append(bucket['key'])
        return user_ids
