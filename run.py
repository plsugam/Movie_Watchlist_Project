from app import create_app
from app.database import create_tables

app = create_app()

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
