from app.config.mysqlconnection import connectToMySQL
from app.models.user_model import User

# constructor
class Task:
    db = 'task_tracker_db'
    
    def __init__(self, data):
        self.id = data['id']
        self.description = data['description']
        self.status = data['status']
        self.priority = data['priority']
        self.due_date = data['due_date']
        self.user_id = data.get('user_id')
        self.first_name = data.get('first_name', '')
        self.last_name = data.get('last_name', '')
        
        self.user = {
            'first_name': data.get('first_name', ''),
            'last_name': data.get('last_name', '')
        }
        
        self.poster = None
        
        if 'users.id' in data:
            self.poster = User({
                'id': data['users.id'],
                'first_name' : data['first_name'],
                'last_name' : data['last_name'],
                'email' : data['email'],
                'password' : data['password'],
            })

    
    @classmethod
    def get_one_task(cls, task_id):
        query = """
            SELECT tasks.*, users.first_name, users.last_name
            FROM tasks
            LEFT JOIN users ON tasks.user_id = users.id
            WHERE tasks.id = %(id)s
        """
        data = {'id': task_id}
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0]) if results else None
    

    @classmethod
    def get_all_tasks(cls):
        query = """
            SELECT tasks.*, users.first_name, users.last_name
            FROM tasks
            LEFT JOIN users ON tasks.user_id = users.id;
        """
        results = connectToMySQL(cls.db).query_db(query)
        
        tasks = []
        for row in results:
            task = cls(row)
            task.user = {
                'first_name': row['first_name'],
                'last_name': row['last_name']
            }
            tasks.append(task)
        
        return tasks
    
    @classmethod
    def get_tasks_by_user(cls, user_id):
        query = """
            SELECT tasks.*, users.first_name, users.last_name
            FROM tasks
            LEFT JOIN users ON tasks.user_id = users.id
            WHERE tasks.user_id = %(user_id)s;
        """
        data = {'user_id': user_id}
        results = connectToMySQL(cls.db).query_db(query, data)
        
        tasks = []
        for row in results:
            task = cls(row)
            task.user = {
                'first_name': row['first_name'],
                'last_name': row['last_name']
            }
            tasks.append(task)
        
        return tasks

    
    @classmethod
    def create_task(cls, data):
        query = """
            INSERT INTO tasks
            (status, due_date, description, priority, user_id)
            VALUES
            (%(status)s,%(due_date)s, %(description)s, %(priority)s, %(user_id)s)
        """
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update_task(cls, data):
        query = """
        UPDATE tasks
        SET status = %(status)s, due_date = %(due_date)s, description = %(description)s, priority = %(priority)s
        WHERE id = %(id)s 
        """
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete_task(cls, id):
        query = """
            DELETE
            FROM tasks
            WHERE id = %(id)s
        """
        return connectToMySQL(cls.db).query_db(query, {'id':id})

