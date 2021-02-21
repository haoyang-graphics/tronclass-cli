import json
import shelve
from urllib.parse import urljoin

from requests import Session
from bs4 import BeautifulSoup


class Api:
    def __init__(self, base_url, user_name, cache: shelve.Shelf, session: Session):
        self._base_url = base_url
        self._user_name = user_name
        self._session = session
        self._cache = cache

    def _get_api_url(self, path):
        return urljoin(self._base_url, path)

    def _api_call(self, path, method='GET', **kwargs):
        kwargs.setdefault('allow_redirects', True)
        return self._session.request(method, self._get_api_url(path), **kwargs)

    def get_todo(self):
        return self._api_call('api/todos').json()['todo_list']

    def get_user_id(self):
        cache_key = f'api.users.{self._user_name}'
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached
        html = self._api_call('user/index').content
        soup = BeautifulSoup(html, 'html.parser')
        id = soup.find(id='userId').get('value')
        self._cache[cache_key] = id
        return id

    def _get_pages(self, path, params, data_key, page_size=20):
        page = 1
        while True:
            params = {
                'page': page,
                'page_size': page_size,
                **params
            }
            res = self._api_call(path, params=params)
            res.raise_for_status()
            data = res.json()
            yield from data[data_key]

            if page >= data['pages']:
                break
            page += 1

    def get_courses(self, conditions={}, fields='id,name'):
        user_id = self.get_user_id()
        params = {
            'conditions': json.dumps(conditions),
            'fields': fields,
        }
        return self._get_pages(f'api/users/{user_id}/courses', params, 'courses')

    def get_homework(self, course_id, conditions={}):
        params = {
            'conditions': json.dumps(conditions),
        }
        return self._get_pages(f'api/courses/{course_id}/homework-activities', params, 'homework_activities')

    def get_activities(self, course_id, fields='id,title,type'):
        params = {
            'fields': fields,
        } if fields != '' else None
        res = self._api_call(f'api/courses/{course_id}/activities', params=params)
        res.raise_for_status()
        return res.json()['activities']
