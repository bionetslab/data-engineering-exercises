import mysql.connector
import os

# Database connection details (adjust if needed)
DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "mysecretpassword")
DB_NAME = os.environ.get("DB_NAME", "mydb")

def connect_to_database():
    """Connects to the MySQL database."""
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None



def drop_database():
    """Drops the specified database."""
    mydb = connect_to_database()
    if mydb:
        cursor = mydb.cursor()
        try:
            cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
            mydb.commit()
            print(f"Database '{DB_NAME}' dropped successfully (if it existed).")
        except mysql.connector.Error as err:
            print(f"Error dropping database '{DB_NAME}': {err}")
            mydb.rollback()
        finally:
            cursor.close()
            mydb.close()
            
def create_database_and_tables():
    """Connects to MySQL and creates the database and tables."""
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = mydb.cursor()

        # Create the database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' created or already exists.")

        # Switch to the created database
        cursor.execute(f"USE {DB_NAME}")

        # Create Person table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Person (
            PersonID INT PRIMARY KEY AUTO_INCREMENT,
            FirstName VARCHAR(255),
            LastName VARCHAR(255),
            DateOfBirth DATE,
            PlaceOfBirth VARCHAR(255),
            CountryOfBirth VARCHAR(255),
            Title VARCHAR(50),
            HealthInsuranceID VARCHAR(255),
            HealthInsuranceCardID VARCHAR(255),
            Address VARCHAR(255),
            PostalCode VARCHAR(20),
            FederalState VARCHAR(255)
        )
        """)
        print("Table 'Person' created or already exists.")

        # Create Drug table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Drug (
            DrugID INT PRIMARY KEY AUTO_INCREMENT,
            ChemicalSubstance VARCHAR(255),
            BrandName VARCHAR(255),
            GenericName VARCHAR(255),
            Dosage VARCHAR(100),
            PackageSize INT
        )
        """)
        print("Table 'Drug' created or already exists.")

        # Create Diagnosis table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Diagnosis (
            DiagnosisID INT PRIMARY KEY AUTO_INCREMENT,
            DiagnosisDescription TEXT,
            ICDCode VARCHAR(50),
            INDEX (ICDCode)
        )
        """)
        print("Table 'Diagnosis' created or already exists.")

        # Create Prescription table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Prescription (
            PrescriptionID INT PRIMARY KEY AUTO_INCREMENT,
            OrdonanceDate DATE,
            PickUpDate DATE,
            DeliveryInterval INT,
            DrugID INT,
            FOREIGN KEY (DrugID) REFERENCES Drug(DrugID)
            )
        """)
        print("Table 'Prescription' created or already exists.")

        # Create OutpatientVisit table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS OutpatientVisit (
            VisitID INT PRIMARY KEY AUTO_INCREMENT,
            Date DATE,
            PersonID INT, 
            DiagnosisID INT,
            PrescriptionID INT,
            FOREIGN KEY (PersonID) REFERENCES Person(PersonID),
            FOREIGN KEY (DiagnosisID) REFERENCES Diagnosis(DiagnosisID),
            FOREIGN KEY (PrescriptionID) REFERENCES Prescription(PrescriptionID)
        )
        """)
        print("Table 'OutpatientVisit' created or already exists.")

        mydb.commit()
        cursor.close()
        mydb.close()
        print("Database and tables created successfully.")

    except mysql.connector.Error as err:
        print(f"Error creating database or tables: {err}")

if __name__ == "__main__":
    drop_database()
    create_database_and_tables()
DiagnosisID