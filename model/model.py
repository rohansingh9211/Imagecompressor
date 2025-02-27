import mysql.connector
class Models():
    def __init__(self):
        try:
            self.connect = mysql.connector.connect(host="localhost", user="root", password="Rohan@123", database="flask_db")
            self.cons = self.connect.cursor(dictionary=True)
            print("Database Connection Done Successfully!")
        except Exception as err:
            print(err)
        
    def csv_storage_system(self):
        self.cons.execute("SELECT * from ImageProcessingTask")
        result = self.cons.fetchall()
        print(result)
            
            
    def create_csv_storage_system(self, id, input_csv=None, output_csv=None, status="pending"):
        """Insert a new record into ImageProcessingTask (MySQL-compatible)."""
        query = """
            INSERT INTO ImageProcessingTask (id, status, input_csv, output_csv) 
            VALUES (%s, %s, %s, %s)
        """
        self.cons.execute(query, (id, status, input_csv, output_csv))
        self.connect.commit()
        print("Data inserted successfully")


    def update_csv_storage_system(self, id, status=None, input_csv=None, output_csv=None):
        """Update an existing record in ImageProcessingTask."""
        query = "UPDATE ImageProcessingTask SET "
        params = []
        
        if status:
            query += "status = %s, "
            params.append(status)
        if input_csv:
            query += "input_csv = %s, "
            params.append(input_csv)
        if output_csv:
            query += "output_csv = %s, "
            params.append(output_csv)

        query = query.rstrip(", ")  
        query += " WHERE id = %s"
        params.append(id)

        self.cons.execute(query, tuple(params))
        self.connect.commit() 
        print("Data updated successfully")
