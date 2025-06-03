import psycopg2
from dotenv import load_dotenv
import os
import sys
load_dotenv()


class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname=os.getenv("NAME"),
                user="postgres",
                password=os.getenv("PASSWORD"),
                host="localhost",
                client_encoding='UTF-8',
                connect_timeout=5
            )
            print("Успешное подключение к БД!")
        except psycopg2.OperationalError as e:
            print(f"Ошибка подключения к БД: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            sys.exit(1)

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()
            print("Подключение к БД закрыто")

    def get_filter_data(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT model_name FROM Models;")
            models = [row[0] for row in cursor.fetchall()]

            cursor.execute("SELECT DISTINCT fuel_type FROM Models;")
            fuel_types = [row[0] for row in cursor.fetchall()]

            cursor.execute("SELECT DISTINCT transmission FROM Models;")
            transmissions = [row[0] for row in cursor.fetchall()]

            return models, fuel_types, transmissions

    def add_car(self, model_name, year, price, km_driven, engine_capacity,
                fuel_type, transmission, ownership, spare_key, imperfections, repainted_parts):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO models 
                    (model_name, year, engine_capacity, transmission, fuel_type)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (model_name, year) DO NOTHING;
            """, (model_name, year, engine_capacity, fuel_type, transmission))
            cursor.execute("""
                INSERT INTO cars 
                    (model_name, year, price, km_driven,
                    ownership, spare_key, imperfections, repainted_parts)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (model_name, year, price, km_driven, ownership, spare_key, imperfections, repainted_parts))
            cursor.execute("SELECT COUNT(*) FROM cars")
            car_id = cursor.fetchone()[0]
            self.conn.commit()
            return car_id

    def filter_cars(self, model="", year="", price_min="", price_max="",
                   fuel_type="", transmission=""):
        query = """
        SELECT car_id, cars.model_name, cars.year, price, km_driven, engine_capacity, 
               fuel_type, transmission, ownership, spare_key, 
               imperfections, repainted_parts
        FROM cars JOIN models ON cars.model_name=models.model_name AND cars.year = models.year
        WHERE 1=1
        """
        params = []

        if model:
            query += " AND cars.model_name LIKE %s"
            params.append(f"%{model}%")
        if year:
            query += " AND cars.year = %s"
            params.append(year)
        if price_min:
            query += " AND price >= %s"
            params.append(price_min)
        if price_max:
            query += " AND price <= %s"
            params.append(price_max)
        if fuel_type:
            query += " AND fuel_type = %s"
            params.append(fuel_type)
        if transmission:
            query += " AND transmission = %s"
            params.append(transmission)

        query += " ORDER BY price LIMIT 200;"

        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def get_all_cars(self):
        query = """
        SELECT car_id, cars.model_name, cars.year, price, km_driven, engine_capacity, 
               fuel_type, transmission, ownership, spare_key, 
               imperfections, repainted_parts
        FROM cars JOIN models ON cars.model_name=models.model_name AND cars.year = models.year
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def update_car(self, car_id, price, km_driven
                  ,ownership, spare_key, imperfections, repainted_parts):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                UPDATE cars 
                SET 
                    price = %s,
                    km_driven = %s,
                    ownership = %s,
                    spare_key = %s,
                    imperfections = %s,
                    repainted_parts = %s
                WHERE car_id = %s
            """, (price, km_driven, ownership, spare_key, imperfections, repainted_parts, car_id))
            self.conn.commit()

    def delete_car(self, car_id):
        with self.conn.cursor() as cursor:
            cursor.execute("DELETE FROM cars WHERE car_id = %s", (car_id,))
            self.conn.commit()

    def get_car_by_id(self, car_id):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT cars.model_name, cars.year, price, km_driven, engine_capacity, 
                       fuel_type, transmission, ownership, spare_key, 
                       imperfections, repainted_parts
                FROM cars JOIN models ON cars.model_name=models.model_name AND cars.year = models.year
                WHERE car_id = %s
            """, (car_id,))
            return cursor.fetchone()