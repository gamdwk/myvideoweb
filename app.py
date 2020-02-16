#!flask/bin/python
from app import app, db

if __name__ == '__main__':
    # db.drop_all(app=app)
    app.run(debug=True, host='0.0.0.0', port=8080)
