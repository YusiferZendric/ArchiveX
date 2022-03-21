from flask import Flask, render_template,request,session
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = "mysecret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weakness.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class save(db.Model):
    _id = db.Column("id", db.Integer,primary_key=True)
    level = db.Column(db.Integer,nullable=False)
    weakness = db.Column(db.String(400),nullable=False)
    subject = db.Column(db.String(20),nullable=False)

    def __init__(self, level, weakness,subject):
        self.level = level
        self.weakness = weakness
        self.subject = subject
        
@app.route("/")
def main():
    return render_template("intro.html")
@app.route("/home")
def home():
    return render_template('index.html')
@app.route("/view")
def view():

    return render_template('view.html',)

@app.route("/<subject>")
def submitMistakes(subject):
    if subject!="favicon.ico":
        session['subject'] = subject
    if subject=="favicon.ico":
        subject = session['subject']
    return render_template('subject.html', subject=subject)
@app.route("/success", methods=['GET',"POST"])
def success():
    if request.method == 'POST':
        option = request.form['select']
        session['option'] = option
        weakness = request.form['weakness']
        session['weakness'] = weakness
        data = save.query.filter_by(level=option, weakness=weakness).first()
        print(data)
        if data is None:
            data = save(option, weakness,session['subject'])
            db.session.add(data)
            db.session.commit()
            print(f"subject: {session['subject']}")
            return render_template('success.html',success="success")
        else:
            return render_template('success.html',warning="warning",subject=session['subject'])

@app.route("/<sub>/view/<level>")
def subject_view(sub,level):
    data = save.query.all()
    Data = {}
    print(len(data))
    index=0
    for rows in data:
        index+=1
        print(f"index: {index}")
        try:
            Data[rows.subject]['level'].append(rows.level)
            Data[rows.subject]['weakness'].append(rows.weakness)
        except:
            Data[rows.subject] = {"level":[],"weakness":[]}
            Data[rows.subject]['level'] = [rows.level]
            Data[rows.subject]['weakness'] = [rows.weakness]         
    print(Data)
    return render_template('view.html',data=Data,subject=sub,list=list, len=len,level=level)

if __name__ == '__main__':
    app.run(debug=True)

