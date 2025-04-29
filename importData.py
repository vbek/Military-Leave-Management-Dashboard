import mysql.connector
import pandas as pd
import tkinter
from tkinter import messagebox


class CreateAndInsertDataFromCsvIntoTable:
    def __init__(self, csv_file, table_name, primary_key):
        self.csv_file = csv_file
        self.primary_key = primary_key
        self.table_name = table_name

    def __get_connection(self):
        from CreateConnection import CreateConnection
        db = CreateConnection('bibekdb')
        self.my_conn = db.create_connection()
        return self.my_conn

    def create_table(self, data):
        leave_table_name = 'leave_record_' + self.table_name
        split_data = self.table_name.split('_')
        displaying_table_name = split_data[0].upper()
        for i in range(1, len(split_data)):
            displaying_table_name += ' ' + split_data[i].upper()
        conn = self.__get_connection()
        # conn = self.create_connection()
        cursor = conn.cursor()
        import numpy as np
        df = pd.read_csv(self.csv_file, na_values=[0])

        query_to_check_table_name = 'SHOW TABLES LIKE %s'
        value_table_name = (self.table_name,)
        cursor.execute(query_to_check_table_name, value_table_name)
        table_exists = cursor.fetchone()
        if not table_exists:
            table_schema = ', '.join([f'{col} {df[col].dtype}' for col in df.columns])
            table_schema = table_schema.replace('float64', 'DOUBLE')
            table_schema = table_schema.replace('int64', 'INT')
            table_schema = table_schema.replace('object', 'VARCHAR(255)')
            table_schema += f', PRIMARY KEY({self.primary_key})'
            create_leave_table_schema = f'''CREATE TABLE {leave_table_name}
                    (
                        CompNo INT NOT NULL,
                        LeaveDate DATE NOT NULL DEFAULT '2022-02-22',
                        ReturnDate DATE NOT NULL DEFAULT '2022-02-22',
                        PRIMARY KEY (CompNo, LeaveDate),
                        FOREIGN KEY (CompNo) REFERENCES {self.table_name}(CompNo) ON DELETE CASCADE,
                        UNIQUE (CompNo, LeaveDate)
                        
                    );'''
            trigger_name = 'trigger_insert_' + self.table_name
            trigger_schema = f'''CREATE TRIGGER {trigger_name}
                    AFTER INSERT ON {self.table_name}
                    FOR EACH ROW
                    BEGIN
                        INSERT INTO {leave_table_name} (CompNo, LeaveDate, ReturnDate)
                        VALUES (NEW.CompNo, '2022-02-22', '2022-02-22');
                    END;'''
            try:
                cursor.execute(f'CREATE TABLE {self.table_name} ({table_schema});')
                cursor.execute(f'''ALTER TABLE {self.table_name}
                                            ADD COLUMN Photo LONGBLOB NULL;''')
                cursor.execute(f'''ALTER TABLE {self.table_name}
                                            MODIFY COLUMN Phone VARCHAR(255) DEFAULT NULL,
                                            MODIFY COLUMN Loc VARCHAR(255) DEFAULT NULL,
                                            MODIFY COLUMN Trade VARCHAR(255) DEFAULT NULL,
                                            MODIFY COLUMN Address VARCHAR(255) DEFAULT NULL,
                                            MODIFY COLUMN DOB VARCHAR(255) DEFAULT NULL,
                                            MODIFY COLUMN Sex VARCHAR(45) DEFAULT NULL,
                                            MODIFY COLUMN Remarks VARCHAR(255) DEFAULT NULL,
                                            MODIFY COLUMN bloodgp VARCHAR(255) DEFAULT NULL;''')
                cursor.execute(create_leave_table_schema)
                cursor.execute(trigger_schema)
                data['sorted_unit_name'].append(displaying_table_name)
                # unit_name_list_combobox.insert(END, displaying_table_name)
                messagebox.showinfo("SUCCESS", "New Unit Data has been Added")
            except mysql.connector.Error as err:
                conn.rollback()
                messagebox.showerror("ERROR", err)
            conn.commit()
            cursor.close()
            conn.close()
            self.__insert_data()

        else:
            tkinter.messagebox.showwarning("WARNING", "Table already exists")
            cursor.close()
            conn.close()

    def __insert_data(self):
        df = pd.read_csv(self.csv_file, keep_default_na=False)
        conn = self.__get_connection()
        cursor = conn.cursor()
        for i, row in df.iterrows():
            try:
                cursor.execute(f"""INSERT INTO {self.table_name} 
                (Unit, CompNo, Rnk, Name, Phone, Loc, Trade, Address, DOB, Sex, bloodgp, Remarks)
                VALUES {tuple(row)}""")
                conn.commit()
            except mysql.connector.Error as err:
                conn.rollback()
                messagebox.showerror("ERROR", err)
        cursor.close()
        conn.close()
