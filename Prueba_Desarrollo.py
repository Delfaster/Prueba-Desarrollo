import json
import csv
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def cargar_datos_json(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

def cargar_datos_csv(csv_file):
    users = {}
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            users[row['user_id']] = row['user_manager']
    return users

def inicializacion_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS db_info (
                        database_name TEXT,
                        owner_email TEXT,
                        manager_email TEXT,
                        classification TEXT)''')
    cursor.execute('DELETE FROM db_info')
    conn.commit()
    return conn, cursor

def insertar_datos_database(cursor, databases, users):
    for db in databases:
        database_name = db.get('database')
        owner_email = db.get('owner')
        classification = db.get('classification')

        if not database_name or not classification:
            continue
        
        if not owner_email:
            owner_email = 'todero@gmail.com'
        
        manager_email = users.get(owner_email)
        cursor.execute('''INSERT INTO db_info (database_name, owner_email, manager_email, classification)
                          VALUES (?, ?, ?, ?)''', 
                       (database_name, owner_email, manager_email, classification))

def enviar_emails(cursor, smtp_server, smtp_port, smtp_user, smtp_password):
    for db in cursor.execute('SELECT * FROM db_info WHERE classification="high"'):
        database_name, owner_email, manager_email, classification = db
        if not manager_email:
            continue

        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = manager_email
        msg['Subject'] = f'Validación de la clasificación de {database_name}'
        body = f'Espero su "OK" respecto a la clasificación de alta criticidad para la base de datos: {database_name}.'
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, manager_email, msg.as_string())

def main():
    json_file = 'datos_json.json'
    csv_file = 'datos_csv.csv'
    db_name = 'databases.db'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'diego.dacr96@gmail.com'
    smtp_password = 'krbg dmjn yshm xspv'

    databases = cargar_datos_json(json_file)
    users = cargar_datos_csv(csv_file)
    conn, cursor = inicializacion_database(db_name)

    insertar_datos_database(cursor, databases, users)
    conn.commit()

    enviar_emails(cursor, smtp_server, smtp_port, smtp_user, smtp_password)
    conn.close()

if __name__ == '__main__':
    main()
