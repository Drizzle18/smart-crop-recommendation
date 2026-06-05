"""This is the main entry point for the Flask application.
It imports the create_app function from the app package, 
creates an instance of the Flask application, and runs it in debug mode
if this script is executed directly.
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)