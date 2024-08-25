from app import app

from app.controllers import user_controller, task_controller

if __name__ == "__main__":
    app.run(debug=True)
