from flask import Flask, render_template, redirect, request, flash
from bson.objectid import ObjectId
import pymongo
app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def hello_world():
    mydb = myclient['mydatabase']
    mycol = mydb["questions"]
    data = []
    print(data)
    for x in mycol.find():
        if(x['info']!="details"):
            data.append(x)
    return render_template('index.html', data=data)

@app.route('/saveqsn',methods = ['POST'])
def index():
    qtype = request.form['qtype'] 
    qmarks = request.form['qmarks']
    qstat = request.form['qstat']
    oa = request.form["oa"]
    ob = request.form["ob"]
    oc = request.form["oc"]
    mydb = myclient['mydatabase']
    mycol = mydb["questions"]
    print(qmarks, qstat, qtype)
    if(qstat!="" and qmarks!="" and qtype!="none"):
        mydict = { "type": qtype, "marks": qmarks, "question": qstat, "optA": oa, "optB": ob, "optC": oc, "info": "qsn" }
        x = mycol.insert_one(mydict)
    else:
        flash("Enter all the required fields to proceed!")
    return redirect("/")

@app.route('/paper')
def paper():
    mydb = myclient['mydatabase']
    mycol = mydb["questions"]
    data = []
    for x in mycol.find():
        data.append(x)
    return render_template('paper.html', data=data )

@app.route('/delete', methods = ['POST'])
def delete():
    mydb = myclient['mydatabase']
    mycol = mydb["questions"]
    qsnid = request.form['delid']
    query = {"_id": ObjectId(qsnid)}
    mycol.delete_one(query)
    return redirect('/')

@app.route('/edit', methods = ['POST'])
def edit():
    mydb = myclient['mydatabase']
    mycol = mydb["questions"]
    qsnid = request.form['edid']
    query = {"_id": ObjectId(qsnid)}
    x = mycol.find_one(query)
    data = []
    for y in mycol.find():
        data.append(y)
    return render_template('index.html', x=x, ch=1, data=data )

@app.route('/saveedit',methods = ['POST'])
def saveedit():
    qtype = request.form['qtype']
    print("qtype ",qtype)
    qmarks = request.form['qmarks']
    qstat = request.form['qstat']
    print("qstat ",qstat)
    oa = request.form["oa"]
    ob = request.form["ob"]
    oc = request.form["oc"]
    qsnid = request.form['qsnid']
    mydb = myclient['mydatabase']
    mycol = mydb["questions"]
    myquery = { "_id": ObjectId(qsnid) }
    if(qstat!="" and qmarks!="" and qtype!="none"):
        newvalues = { "$set": { "type": qtype, "marks": qmarks, "question": qstat, "optA": oa, "optB": ob, "optC": oc } }
        mycol.update_one(myquery, newvalues)
    return redirect('/')

@app.route('/finalize', methods = ['POST'])
def final():
    ttime = request.form["ttime"]
    subj = request.form["subj"]
    mydb = myclient['mydatabase']
    mycol = mydb["questions"]
    if(ttime!="" and subj!=""):
        mydict = { "total_time": ttime, "subject": subj, "info": "details" }
        x = mycol.insert_one(mydict)
    else:
        flash("Enter all the required fields to proceed!")
    return redirect("/done")

@app.route('/done')
def done():
    return render_template("done.html")

if __name__ == "__main__":
    app.run(debug=True)