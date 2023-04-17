# a code that connects to the Postgres database

import psycopg

class DBConnection:
	def __init__(self, user, password, host="127.0.0.1", port="5432", db="rentequipmentservicedb"):
		self.host = host
		self.port = port
		self.db = db
		self.user = user
		self.password = password

	def connect(self):
		try:
			self.conn = psycopg.connect(host=self.host, port=self.port, dbname=self.db, user=self.user, password=self.password)