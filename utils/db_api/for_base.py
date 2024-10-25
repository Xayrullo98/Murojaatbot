import sqlite3


class Database:
    def __init__(self, path):
        self.path_to_db = path

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item}=?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM usres:", fetchone=True)

    def delete_users(self):
        self.execute("DELETE FROM users WHERE TRUE", commit=True)

    def user_qoshish(self, ism: str, tg_id: int, username: str = None, ):

        sql = """
           INSERT INTO users(ism,  username, tg_id) VALUES(?, ?, ?)
           """
        self.execute(sql, parameters=(ism, username, tg_id), commit=True)

    def delete_admin(self, **kwargs):
            sql = "DELETE FROM admins WHERE "
            sql, parameters = self.format_args(sql, kwargs)

            return self.execute(sql, parameters=parameters, commit=True)

    def add_admin(self, name: str, tg_id: int ):

        sql = """
           INSERT INTO admins(name, tg_id) VALUES(?, ?)
           """
        self.execute(sql, parameters=(name, tg_id), commit=True)

    def select_all_admins(self):
        sql = """
            SELECT * FROM admins
            """
        return self.execute(sql, fetchall=True)
    #    # # driver section
    # def add_drivers(self, fullname: str, type: str, model: str, tel: str, tg_id: str, status: bool, created_at: str,
    #                 balance: int = 0):
    #
    #     sql = """
    #     INSERT INTO drivers(fullname,type,model,tel,tg_id,status,created_at,balance) VALUES(?, ?, ?, ?, ?, ?, ?, ?)
    #     """
    #     self.execute(sql, parameters=(fullname, type, model, tel, tg_id, status, created_at, balance), commit=True)
    #
    # def select_all_drivers(self):
    #     sql = """
    #         SELECT * FROM drivers
    #         """
    #     return self.execute(sql, fetchall=True)
    #
    # def delete_drivers(self, **kwargs):
    #     sql = "DELETE  FROM drivers WHERE "
    #     sql, parameters = self.format_args(sql, kwargs)
    #
    #     return self.execute(sql, parameters=parameters, commit=True)
    #
    # def select_drivers(self, **kwargs):
    #     sql = "SELECT * FROM drivers WHERE "
    #     sql, parameters = self.format_args(sql, kwargs)
    #
    #     return self.execute(sql, parameters=parameters, fetchone=True)
    #
    # # users section
    # def add_user(self, fullname: str, tg_id: str, tel: str, created_at: str, username: str = None, status: bool = 1, ):
    #
    #     sql = """
    #     INSERT INTO users(fullname,tg_id,tel,username,status,created_at) VALUES(?, ?, ?, ?, ?, ?)
    #     """
    #     self.execute(sql, parameters=(fullname, tg_id, tel, username, status, created_at), commit=True)
    #
    # def select_all_user(self):
    #     sql = """
    #         SELECT * FROM users
    #         """
    #     return self.execute(sql, fetchall=True)
    #
    # def delete_user(self, **kwargs):
    #     sql = "DELETE FROM users WHERE "
    #     sql, parameters = self.format_args(sql, kwargs)
    #
    #     return self.execute(sql, parameters=parameters, commit=True)
    #
    # def select_user(self, **kwargs):
    #     sql = "SELECT * FROM users WHERE "
    #     sql, parameters = self.format_args(sql, kwargs)
    #
    #     return self.execute(sql, parameters=parameters, fetchone=True)
    #
    # # Customer order section
    # def add_customer_order(self, from_place: str, to_place: str, number: str, tg_id: str, date: str, status: bool,
    #                        created_at: str,
    #                        price: float = 0):
    #     sql = """
    #         INSERT INTO Customer_orders(from_place, to_place, number, date, tg_id, status, created_at, price) VALUES(?, ?, ?, ?, ?, ?, ?, ?)
    #         """
    #     self.execute(sql, parameters=(from_place, to_place, number, date, tg_id, status, created_at, price),
    #                  commit=True)
    #
    # def select_all_customer_orders(self):
    #     sql = """
    #             SELECT * FROM Customer_orders
    #             """
    #     return self.execute(sql, fetchall=True)
    #
    # def delete_customer_orders(self, **kwargs):
    #     sql = "DELETE  FROM Customer_orders WHERE "
    #     sql, parameters = self.format_args(sql, kwargs)
    #
    #     return self.execute(sql, parameters=parameters, commit=True)
    #
    # def select_customer_orders(self, **kwargs):
    #     sql = "SELECT * FROM Customer_orders WHERE "
    #     sql, parameters = self.format_args(sql, kwargs)
    #
    #     return self.execute(sql, parameters=parameters, fetchall=True)
    #
    # # Driver orders section
    # def add_driver_order(self, from_place: str, to_place: str, number: str, tg_id: str, date: str, status: bool,
    #                      created_at: str,
    #                      price: float = 0):
    #     sql = """
    #         INSERT INTO Driver_orders(from_place, to_place, number, date, tg_id, status, created_at, price) VALUES(?, ?, ?, ?, ?, ?, ?, ?)
    #         """
    #     self.execute(sql, parameters=(from_place, to_place, number, date, tg_id, status, created_at, price),
    #                  commit=True)
    #
    # def select_all_driver_order(self):
    #     sql = """
    #             SELECT * FROM Driver_orders
    #             """
    #     return self.execute(sql, fetchall=True)
    #
    # def delete_driver_order(self, **kwargs):
    #     sql = "DELETE  FROM Driver_orders WHERE "
    #     sql, parameters = self.format_args(sql, kwargs)
    #
    #     return self.execute(sql, parameters=parameters, commit=True)
    #
    # def select_driver_order(self, **kwargs):
    #     sql = "SELECT * FROM Driver_orders WHERE "
    #     sql, parameters = self.format_args(sql, kwargs)
    #
    #     return self.execute(sql, parameters=parameters, fetchall=True)
    #
    # # models section
    # def select_all_models(self):
    #     sql = """
    #            SELECT * FROM models
    #            """
    #     return self.execute(sql, fetchall=True)
    #
    # # regions section
    # def select_all_regions(self):
    #     sql = """
    #               SELECT * FROM regions
    #               """
    #     return self.execute(sql, fetchall=True)
    # # def update_deadline(self, deadline, id):
    # #     # SQL_EXAMPLE = "UPDATE myfiles_menu SET email=mail@gmail.com WHERE id=12345"
    # #
    # #     sql = f"""
    # #        UPDATE drivers_students SET deadline=? WHERE id=?
    # #        """
    # #     return self.execute(sql, parameters=(deadline, id), commit=True)


def logger(statement):
    print(f"""
    -------------------------------------------------------
    Executing:
    {statement}
    -------------------------------------------------------
""")
