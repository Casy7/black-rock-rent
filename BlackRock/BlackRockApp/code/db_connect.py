# a code that connects to the Postgres database

import psycopg
from datetime import datetime
from .classes import *

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

	def get_all_user_accountings(self):
		with psycopg.connect(self.get_connection_credentials()) as conn:
			with conn.cursor() as cur:

				acc_id = cur.execute("SELECT * FROM public.rent_accounting ra WHERE ra.username = %s ORDER BY id DESC", [self.user]).fetchall()

				user_rent_accountings = []

				for acc in acc_id:
					user_rent_accounting = UserRentAccounting(acc[0], acc[3], acc[4], acc[5], acc[6]) 
					user_rent_accountings.append(user_rent_accounting)
					acc_unique_equipment = cur.execute("SELECT * FROM public.rented_equipment WHERE accounting = %s", [acc[0]]).fetchall()
					for eq in acc_unique_equipment:
						eq_info = cur.execute("SELECT id, name, cathegory, price FROM public.equipment WHERE id = %s", [eq[2]]).fetchone()
						user_rent_accounting.equipment_list.append(UserRentedUniqueEquipment(eq_info[0], eq_info[1], eq_info[2], eq_info[3], 1))
					
					acc_countable_equipment = cur.execute("SELECT * FROM public.rented_countable_equipment WHERE accounting = %s", [acc[0]]).fetchall()
					for eq in acc_countable_equipment:
						eq_info = cur.execute("SELECT id, name, cathegory, price FROM public.equipment WHERE id = %s", [eq[1]]).fetchone()
						user_rent_accounting.equipment_list.append(UserRentedCountableEquipment(eq_info[0], eq_info[1], eq_info[2], eq_info[3], eq[2], eq[3]))

				return user_rent_accountings
			

	def get_cathegory_id(self, path):
		parent_id = ""
		with psycopg.connect(self.get_connection_credentials()) as conn:
			with conn.cursor() as cur:
				path = path.split('/')
				parent_dir = path[0]
				parent_id = cur.execute("SELECT id FROM cathegory WHERE name = %s AND parent_cathegory IS NULL", [parent_dir]).fetchone()[0]
				for dir in path[1:]:
					parent_id = cur.execute("SELECT id FROM cathegory WHERE name = %s AND parent_cathegory = %s", [dir, parent_id]).fetchone()[0]
		
		return parent_id

	def create_new_equipment(self, new_equipment):
		new_equipment_id = -1
		with psycopg.connect(self.get_connection_credentials()) as conn:
			with conn.cursor() as cur:
				result = cur.execute("INSERT INTO equipment (name, cathegory, price, img_path, description, amount) VALUES (%s, %s, %s, %s, %s, %s)",
				                     (new_equipment.name, self.get_cathegory_id(new_equipment.cathegory), new_equipment.price, './', new_equipment.description, new_equipment.amount))
				
				new_equipment_id = cur.execute("SELECT id FROM equipment WHERE name = %s AND cathegory = %s AND description = %s AND amount = %s", (
										new_equipment.name,
										self.get_cathegory_id(new_equipment.cathegory),
										new_equipment.description,
										new_equipment.amount)
									).fetchone()[0]
				if new_equipment.amount == 1:

					unique_equipment_deterioration = cur.execute(
										"INSERT INTO unique_equipment (id, deterioration) VALUES (%s, %s)", (new_equipment_id, 1))
		
		return new_equipment_id
		


					