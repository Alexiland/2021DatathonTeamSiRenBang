from flask import Flask, render_template, request
from utils.util import *
app = Flask(__name__)


@app.route('/')
def index():
    print("successful")
    return render_template('index.html')


@app.route('/hello')
def hello():
    return render_template('hello.html')

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/result_display/<transMat>')
def result_display(transMat):
    return render_template('result_display.html', transMat=transMat)

@app.route('/login',methods = ['POST', 'GET'])
def login():
    testMat = [['Month', 'TotalCost', 'AvgCost'],
              ['2004',  1000,      400],
              ['2005',  1170,      460],
              ['2006',  660,       1120],
              ['2007',  1030,      540]]
    if request.method == 'POST':
        agency = request.form['an']
        vendor = request.form['vn']

        if not is_valid_agency(agency) or not is_valid_vendor(vendor):
            return render_template('not_found.html', transMat=testMat)
        else:
            # both vendor and agency are valid
            if not agency == "":
                agency_matrix = lookup_agency_info(agency)

            if not vendor == "":
                vendor_matrix = lookup_vendor_info(vendor)
        return render_template('result_display.html', transMat=testMat)
    else:
        agency = request.args.get('an')
        return render_template('result_display.html', transMat=testMat)

if __name__ == '__main__':
    app.run(debug=True)

