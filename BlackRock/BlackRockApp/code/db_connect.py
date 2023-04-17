# a code that connects to the Postgres database

import psycopg
from datetime import datetime

class DBConnection:
	def __init__(self, user, password, host="127.0.0.1", port="5432", db="rentequipmentservicedb"):
		self.host = host
		self.port = port
		self.db = db
		self.user = user
		self.password = password

	def get_connection_credentials(self):
		return "host="+self.host+" port="+self.port+" dbname="+self.db+" user="+self.user+" password='"+self.password+"'"


	def connect(self):
		try:
			self.conn = psycopg.connect(host=self.host, port=self.port, dbname=self.db, user=self.user, password=self.password)
		except:
			print("Unable to connect to database")

	def create_accounting(self, start_date, end_date):
		with psycopg.connect(self.get_connection_credentials()) as conn:
			with conn.cursor() as cur:
				start_datetime = start_date + ' ' + datetime.now().strftime("%H:%M:%S")
				result = cur.execute("INSERT INTO rent_accounting (username, comment, start_date, end_date) VALUES (%s, %s, %s, %s)", (self.user, '', start_date, end_date))

	def add_equipment_to_accounting(self, equipment_id):
		with psycopg.connect(self.get_connection_credentials()) as conn:
			with conn.cursor() as cur:

				acc_id = cur.execute("SELECT id FROM public.rent_accounting ra WHERE ra.username = %s ORDER BY id DESC LIMIT 1", [self.user]).fetchone()[0]
				result = cur.execute("INSERT INTO public.rented_equipment (accounting, deterioration, equipment) VALUES (%s, %s, %s)", (acc_id, 0, equipment_id))

	def add_countable_equipment_to_accounting(self, equipment_id, amount):
		with psycopg.connect(self.get_connection_credentials()) as conn:
			with conn.cursor() as cur:

				acc_id = cur.execute("SELECT id FROM public.rent_accounting ra WHERE ra.username = %s ORDER BY id DESC LIMIT 1", [self.user]).fetchone()[0]
				result = cur.execute("INSERT INTO public.rented_countable_equipment (accounting, equipment, amount, returned_amount) VALUES (%s, %s, %s, %s)", (acc_id, equipment_id, amount, 0))	