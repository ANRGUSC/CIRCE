from flask import Flask
import psutil
import json
app = Flask(__name__)

@app.route('/') #web route url
def performance():
    response = {} #create a response json object
    response["memory"]=psutil.virtual_memory().percent #Return statistics about system memory usage
    response["cpu"]=psutil.cpu_percent() #Return a float representing the current system-wide CPU utilization as a percentage.
    return json.dumps(response) #output performance information by json format

if __name__ == '__main__':
    app.run(host='0.0.0.0') #run this web application on 0.0.0.0 and default port is 5000
