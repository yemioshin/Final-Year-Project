import os
from overview import create_app


app = create_app()

if __name__ == '__main__':
    #app.run(debug=False, port=5002)
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')

    