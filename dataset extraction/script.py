import csv
import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()
DB_NAME = os.getenv('NAME')
DB_USER = "postgres"
DB_PASSWORD = os.getenv('PASSWORD')
DB_HOST = "localhost"
DB_PORT = "5432"


def create_tables(conn):
    """Create tables if they don't exist (based on db.sql)"""
    with conn.cursor() as cur:
        # Create models table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS models (
                model_name character varying(50) NOT NULL,
                year integer NOT NULL,
                engine_capacity integer,
                transmission character varying(10),
                fuel_type character varying(10),
                PRIMARY KEY (model_name, year)
            );
        """)

        # Create cars table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                car_id SERIAL PRIMARY KEY,
                model_name character varying(50),
                year integer,
                price integer,
                spare_key boolean,
                ownership integer,
                km_driven integer,
                imperfections integer,
                repainted_parts integer,
                FOREIGN KEY (model_name, year) REFERENCES public.models(model_name, year)
            );
        """)

        conn.commit()


def import_data(conn, csv_file):
    """Import data from CSV file to database"""
    with conn.cursor() as cur:
        # First, read and process the CSV file
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # We'll collect unique model-year combinations for the models table
            models_data = set()
            cars_data = []

            for row in reader:
                # Prepare model data
                model_name = row['Model Name'].split(' ', 2)[2]  # Remove year & company from model name
                year = int(row['Manufacturing_year'])
                engine_capacity = int(row['Engine capacity']) if row['Engine capacity'] else None
                transmission = row['Transmission']
                fuel_type = row['Fuel type']

                models_data.add((model_name, year, engine_capacity, transmission, fuel_type))

                # Prepare car data
                spare_key = row['Spare key'].lower() == 'Yes'
                ownership = int(row['Ownership'])
                km_driven = int(row['KM driven'])
                imperfections = int(row['Imperfections'])
                repainted_parts = int(row['Repainted Parts'])
                price = int(row['Price'])

                cars_data.append((model_name, year, price, spare_key, ownership, km_driven,
                                  imperfections, repainted_parts))

            # Insert models data
            for model in models_data:
                cur.execute("""
                    INSERT INTO public.models 
                    (model_name, year, engine_capacity, transmission, fuel_type)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (model_name, year) DO NOTHING;
                """, model)

            # Insert cars data
            for car in cars_data:
                cur.execute("""
                    INSERT INTO public.cars 
                    (model_name, year, price, spare_key, ownership, km_driven, imperfections, repainted_parts)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """, car)

            conn.commit()

            print(f"Inserted {len(models_data)} models and {len(cars_data)} cars.")


def main():
    try:
        # Connect to the database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        # Create tables if they don't exist
        create_tables(conn)

        # Import data from CSV
        import_data(conn, 'dataset.csv')

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()