import mysql.connector
from faker import Faker
from datetime import datetime, timedelta
import os
import random

# Database connection details (adjust if needed)
DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "mysecretpassword")
DB_NAME = os.environ.get("DB_NAME", "mydb")

# Number of person records to create
NUM_PERSON_RECORDS = 20
NUM_DIAGNOSIS_RECORDS = 34
NUM_DRUG_RECORDS = 47
NUM_OUTPATIENT_VISITS_PER_PERSON = 12

# Number of inpatient visits without outpatient visit overlap
NUM_SPECIAL_INPATIENT_PERSONS = 5
special_inpatient_person_ids = set()

# Initialize Faker
fake = Faker('de_DE')
current_year = 2025
currencies = ["EUR", "USD", "GBP", "CHF"]
telemedicine_options = ["Yes", "No"]

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




def insert_person_data(mydb, data):
    """Inserts a single person's data into the Person table and returns the ID."""
    cursor = mydb.cursor()
    sql = """
    INSERT INTO Person (FirstName, LastName, DateOfBirth, PlaceOfBirth, CountryOfBirth, Title, HealthInsuranceID, HealthInsuranceCardID, Address, PostalCode, FederalState)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data['FirstName'],
        data['LastName'],
        data['DateOfBirth'],
        data['PlaceOfBirth'],
        data['CountryOfBirth'],
        data['Title'],
        data['HealthInsuranceID'],
        data['HealthInsuranceCardID'],
        data['Address'],
        data['PostalCode'],
        data['FederalState']
    )
    try:
        cursor.execute(sql, values)
        mydb.commit()
        return cursor.lastrowid
    except mysql.connector.Error as err:
        print(f"Error inserting data into 'Person': {err}")
        mydb.rollback()
        return None



def insert_drug_data(mydb, data):
    """Inserts a single drug's data into the Drug table."""
    cursor = mydb.cursor()
    sql = """
    INSERT INTO Drug ( ChemicalSubstance, BrandName, GenericName, Dosage, PackageSize)
    VALUES (%s, %s, %s,  %s, %s)
    """
    values = (
        data['ChemicalSubstance'],
        data['BrandName'],
        data['GenericName'],
        data['Dosage'],
        data['PackageSize']
    )
    try:
        cursor.execute(sql, values)
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"Error inserting data into 'Drug': {err}")
        mydb.rollback()


def insert_diagnosis_data(mydb, data):
    """Inserts a single diagnosis's data into the Diagnosis table."""
    cursor = mydb.cursor()
    sql = """
    INSERT INTO Diagnosis ( DiagnosisDescription, ICDCode)
    VALUES (%s, %s)
    """
    values = (
        data['DiagnosisDescription'],
        data['ICDCode']
    )
    try:
        cursor.execute(sql, values)
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"Error inserting data into 'Diagnosis': {err}")
        mydb.rollback()


def insert_prescription_data(mydb, data):
    """Inserts a single prescription's data into the Prescription table."""
    cursor = mydb.cursor()
    sql = """
    INSERT INTO Prescription (DrugID, OrdonanceDate, PickUpDate, DeliveryInterval)
    VALUES (%s, %s, %s,  %s)
    """
    values = (
        data['DrugID'],
        data['OrdonanceDate'],
        data['PickUpDate'],
        data['DeliveryInterval']
    )
    try:
        print('inserting prescription')
        cursor.execute(sql, values)
        mydb.commit()
        return cursor.lastrowid
    except mysql.connector.Error as err:
        print(f"Error inserting data into 'Prescription': {err}")
        mydb.rollback()



def insert_outpatient_visit(mydb, visit_data):
    """Inserts a single outpatient visit record."""
    cursor = mydb.cursor()
    sql = """
    INSERT INTO OutpatientVisit (
        PersonID, Date,
        DiagnosisID, PrescriptionID
    )
    VALUES (%s, %s, %s, %s)
    """
    values = (
        visit_data['PersonID'],
        visit_data['Date'],
        visit_data['DiagnosisID'],
        visit_data['PrescriptionID']
    )
    try:
        cursor.execute(sql, values)
        mydb.commit()
        return cursor.lastrowid
    except mysql.connector.Error as err:
        print(f"Error inserting outpatient visit: {err}")
        print(f"Values: {values}")
        mydb.rollback()
        return None
    finally:
        cursor.close()




def main():
    import pandas as pd

    #drop_database()
    db_connection = connect_to_database()
    if not db_connection:
        return

    cursor = db_connection.cursor()

    person_data = pd.read_csv('/app/data/person.tsv', sep='\t', header=0)
    for idx, row in person_data.iterrows():
        print(row['DateOfBirth'])
        insert_person_data(db_connection, row)
    
    drug_data = pd.read_csv('/app/data/drug.tsv', sep='\t', header=0)
    for idx, row in drug_data.iterrows():
        print(row)
        insert_drug_data(db_connection, row)

    diagnosis_data = pd.read_csv('/app/data/diagnosis.tsv', sep='\t', header=0)
    for idx, row in diagnosis_data.iterrows():
        print(row)
        insert_diagnosis_data(db_connection, row)
    


    prescription_data= pd.read_csv('/app/data/prescription.tsv', sep='\t', header=0)
    for idx, row in prescription_data.iterrows():
        print(row)
        insert_prescription_data(db_connection, row)


    visit_data= pd.read_csv('/app/data/visit.tsv', sep='\t', header=0)
    for idx, row in visit_data.iterrows():
        print(row)
        insert_outpatient_visit(db_connection, row)





    db_connection.close()
    print("Data generation complete.")

if __name__ == "__main__":
    main()
