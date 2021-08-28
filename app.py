import subprocess
from subprocess import Popen, PIPE, check_output
from flask import Flask, jsonify
from flask import request
import json


app = Flask(__name__)

@app.route('/flipkart', methods = ['GET'])
def scheduleFlipkart():
    product_name =  request.args['q']

    open('output.jl', 'w').close()


    if product_name:
        p = subprocess.check_output(
            "scrapy runspider flipkart.py -a category='{}' -o output.jl".format(product_name), 
            shell=True)
        

        # print(e.output)
        data = []
        with open('output.jl') as f:
            for line in f:
                data.append(json.loads(line))
        return jsonify(data)
    return "Querry param not passed"


if __name__ == "__main__":
    p = subprocess.check_output("echo -ne '\n' | shub login", shell=True)
    output = p.decode("utf-8")
    print(output)
    app.run(debug=True, host='0.0.0.0')


