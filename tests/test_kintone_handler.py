import unittest
import configparser
from db_handler import kintone_handler

# set kintone token by setting.ini
inifile = configparser.ConfigParser()
try:
	inifile.read('../db_handler/setting.ini', 'UTF-8')
	token_env = inifile.get('kintone', 'KintoneToken')
except IOError as e:
	print("Config file \"{0}\" is not found.".format(e))
	raise IOError


class TestKintoneHandler(unittest.TestCase):
	def setUp(self):
		self.obj = kintone_handler.KintoneHandler(_kintone_token=token_env, app=5)

	def test_get_request(self):
		self.assertTrue(self.obj.get_request())
