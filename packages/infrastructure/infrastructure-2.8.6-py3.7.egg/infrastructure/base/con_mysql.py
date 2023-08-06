# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-12-03 15:42:51
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2021-01-15 16:59:36

from robot.api import logger
import os
import json
import base64
try:
	import pymysql
except:
	os.popen("pip install pymysql -i https://mirrors.ustc.edu.cn/pypi/web/simple/").read()
import threading

class UseMysql(object):
	_instance_lock = threading.Lock()

	def __init__(self):
		pass

	def __new__(cls, *args, **kwargs):
		# print(dir(cls))
		if not hasattr(cls, '_instance'):
			# print(dir(UseMysql))
			with UseMysql._instance_lock:
				if not hasattr(cls, '_instance'):
					db = pymysql.connect("10.69.12.184","maoyongfan",base64.b64decode('bTEyMzQ1Ng==').decode(),"helloBikeDB")
					self.cursor = db.cursor()
					UseMysql._instance = super().__new__(cls)

		return UseMysql._instance


	def getTokenInfos(self):
		sql = "select helloBikeToken,user_agent from helloBikeDB.helloBikeUserInfo where id=1" 
		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall()[0]
			# print(results)
			return results[0],results[1]
		except Exception as e:
			raise Exception("获取token信息失败")

	def getWeekNum(self,rd_id):
		sql = "select week_num from helloBikeDB.helloBikeJavaCoverage_record where id={id}".format(id=rd_id) 
		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall()[0]
			print(results)
			return results[0]
		except Exception as e:
			raise Exception("获取week_num信息失败")

if __name__ == '__main__':
	us = UseMysql()
	print(us.getWeekNum(5834))
	print(id(us))


	