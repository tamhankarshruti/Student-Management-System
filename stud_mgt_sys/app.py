from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3307/studentdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column( db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    marks = db.Column(db.Float, nullable=False)
    roll_num = db.Column(db.Integer, unique=True)

    def __repr__(self):
        return f"Student(id={self.id}, name={self.name}, marks={self.marks}, roll_num={self.roll_num})"

@app.route('/')
def index():
     return render_template("index.html")




@app.route("/studAdd", methods=['GET', 'POST'])
def add_view_stud():
        if request.method == "POST":
            print(request.form) #([('sname', 'shruti'), ('smarks', '85'), ('srollnum', '01')])
            try: 
                name = request.form['sname']
                marks = float(request.form['smarks'])
                roll_num = int(request.form['srollnum'])
                #print(f'{name} and {marks} and {roll_num}')
                s = Student(name=name, marks=marks, roll_num=roll_num)
                #print(s)
                db.session.add(s)
                db.session.commit()
                #return redirect("/listStud")
                return redirect('/')
            
            except:
                 return "There is problem while adding data"
                

        else:
            return render_template("add-stud.html")

@app.route('/listStud')
def list_view_stud():
     list = Student.query.all()
     return render_template("list-stud.html", data = list)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_view_stud(id):
    s = Student.query.get(id)
    #print(request.form)
    if request.method=="POST":
         name = request.form["sname"]
         marks = float(request.form["smarks"])
         roll_num = int(request.form["srollnum"])
         #print(name, marks, roll_num)
         s.name = name
         s.marks = marks
         s.roll_num = roll_num
         db.session.commit()
         return redirect('/listStud')
    else:
        return render_template("edit-student.html", s=s)


@app.route("/delete/<int:id>")
def delete(id):
     s = Student.query.get(id)
     db.session.delete(s)
     db.session.commit()
     return redirect("/listStud")


if __name__ == '__main__':
    app.run(debug=True)