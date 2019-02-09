#!/usr/bin/env python
# -*- encoding:utf-8 -*-


import os
import requests
import configparser


class KintoneHandler:
	def __init__(self, _kintone_token, app):
		"""
		:param _kintone_token:
		:param app:
		"""
		self.token = _kintone_token
		self.app = app
		self.url_1recode = 'https://devmyumit.cybozu.com/k/v1/record.json'
		self.url_allrecodes = 'https://devmyumit.cybozu.com/k/v1/records.json'
		self.response_data = ''
		self.headers = {
			'X-Cybozu-API-Token': self.token
		}

	def get_request(self, _data=None):
		'''
		:param _data: {'field': 'value'}
		:return: success or failure as T/F
		'''

		url = self.url_allrecodes

		# initialize _data by dict when input data is empty
		if _data:
			pass
		else:
			_data = dict()

		_data['app'] = self.app

		try:
			res = requests.get(url, params=_data, headers=self.headers)
			self.response_data = res.json()
		except Exception as _e:
			print(_e)
			return False

		return True

	def get_response_data(self):
		return self.response_data

	def register_request(self, _data):
		'''
		:param _data:{'field': 'value'}
		:return: success or failure as T/F
		'''

		record = {d[0]: {'value': d[1]} for d in _data.items()}
		request_data = {
			'app': self.app,
			'record': record,
		}

		try:
			res = requests.post(self.url_1recode, json=request_data, headers=self.headers)
			res_data = res.json()
		except Exception as _e:
			print(_e)
			return False

		# check the request result by response data
		if 'id' in res_data.keys():
			return True
		else:
			return False

	def register_many_request(self, _data):
		'''
		:param _data: [{'field': 'value'}]
		:return: success or failure as T/F
		'''

		records = list()
		for data in _data:
			recode = {d[0]: {'value': d[1]} for d in data.items()}
			records.append(recode)

		request_data = {
			'app': self.app,
			'records': records
		}

		try:
			res = requests.post(self.url_allrecodes, json=request_data, headers=self.headers)
			res_data = res.json()
		except Exception as _e:
			print(_e)
			return False

		# check the request result by response data
		if 'ids' in res_data.keys():
			return True
		else:
			return False

	def update_request(self, _id, _data):
		'''
		:param _id: record id
		:param _data:{'field': 'value'}
		:return: success or failure as T/F
		'''

		record = {d[0]: {'value': d[1]} for d in _data.items()}
		request_data = {
			'app': self.app,
			'record': record,
			'id': _id
		}

		try:
			res = requests.put(self.url_1recode, json=request_data, headers=self.headers)
			res_data = res.json()
		except Exception as _e:
			print(_e)
			return False

		# check the request result by response data
		if 'revision' in res_data.keys():
			return True
		else:
			return False


if __name__ == '__main__':
	inifile = configparser.ConfigParser()

	# set kintone token by setting.ini
	try:
		inifile.read('./setting.ini', 'UTF-8')
		token_env = inifile.get('kintone', 'KintoneToken')
	except IOError as e:
		print("Config file \"{0}\" is not found.".format(e))
		raise IOError

	KINTONE_TOKEN = os.environ[token_env]

	k = KintoneHandler(KINTONE_TOKEN, app=5)

	if k.get_request({'query': 'keyword like "ええ良くってよ"'}):
		mergen_list = k.get_response_data()

		mergen_list = mergen_list['records']
		record_num = mergen_list[0]['レコード番号']['value']

		print(record_num)
		count = mergen_list[0]['count']['value']

		print(k.update_kintone(record_num, {'count': int(count) + 1}))

	else:
		raise ConnectionError


