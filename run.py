from flask import Flask
from flask_cors import CORS
import module.testroute as testroute
import module.register as register
import module.login as login
import module.edit_service as edit_service
import module.get_service as get_service
import module.service as service

app = Flask(__name__)
CORS(app)

app.config['DATABASE'] = 'userdata.db'

app.register_blueprint(testroute.bp)
app.register_blueprint(register.bp)
app.register_blueprint(login.bp)
app.register_blueprint(edit_service.bp)
app.register_blueprint(get_service.bp)
app.register_blueprint(service.bp)

if __name__ == '__main__':
    app.run(debug=True)
