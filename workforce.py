#imports

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy.sql import text

app = Flask(__name__)
application = app 
db_name = 'pandas_test.db'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = '9cq7DLqHe6'

# Flask-Bootstrap requires this line
Bootstrap(app)

#tables

#main emplpoyment stats table
class StateStatistics(db.Model):
    __tablename__ = 'OESStatesWDescNRaceNUnemploy'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String)
    industry_title = db.Column(db.String)
    occ_code = db.Column(db.String)
    occ_title = db.Column(db.String)
    total_employment = db.Column(db.Float)
    total_pct_of_industry_employment_ = db.Column(db.String)
    mean_hourly_wage = db.Column(db.String)
    mean_annual_wage = db.Column(db.String)
    hourly_pct10 = db.Column(db.String)
    socdefinition = db.Column(db.String)
    Women = db.Column(db.String)
    White = db.Column(db.Float)
    BlackorAfricanAmerican = db.Column(db.Float)
    Asian = db.Column(db.Float)
    HispanicorLatino = db.Column(db.Float)
    unemployrate = db.Column(db.Float)
#list of states
class States(db.Model):
    __tablename__ = 'FIPScodes'
    id = db.Column(db.Integer, primary_key=True)
    stname = db.Column(db.String)
    st = db.Column(db.Integer)
    stusps = db.Column(db.String)

#list of industries
class Industries(db.Model):
    __tablename__ = 'industries'
    id = db.Column(db.Integer, primary_key=True)
    NAICSSector = db.Column(db.String)

#list of occupations
class Occupations(db.Model):
    __tablename__ = 'modifiedoccuprace'
    id = db.Column(db.Integer, primary_key=True)
    occupations = db.Column(db.String)


# get workforce IDs and names for the select menu BELOW
stats = StateStatistics.query.order_by(StateStatistics.id).all()
states = States.query.order_by(States.id).all()
indust = Industries.query.order_by(Industries.id).all()
occupation = Occupations.query.order_by(Occupations.id).all()

# create the list of tuples needed for the choices value
pairs_list = []
for occ in occupation:
    pairs_list.append( (occ.occupations, occ.occupations) )
industry_list=[]
for indu in indust:
    industry_list.append((indu.NAICSSector, indu.NAICSSector))
state_list = []
for state in states:
    state_list.append( (state.stname, state.stname) )

# Flask-WTF form magic
# set up the quickform - select includes value, option text (value matches db)
# all that is in this form is one select menu and one submit button
class WorkerForm(FlaskForm):
    occ = SelectField( 'Tell me about',
      choices=pairs_list)
    industry = SelectField("who work in", choices=industry_list)
    state = SelectField( 'from',
    choices=state_list)

    submit = SubmitField('Submit')

    #form.occ.choices = [(occ.occ_code, occ.occ_title)for occ in OccupationalEmploymentStatisticsbyStatesIndustryOccupation.query.filter_by(state='state').all()]


# routes

@app.route('/', methods=['GET', 'POST'])
def index():
    form = WorkerForm()
    return render_template('index.html', form=form)

@app.route('/stat', methods=['POST'])
def stat_detail():
    my_occ = request.form['occ']
    my_industry = request.form['industry']
    my_state = request.form['state']
    the_stat = StateStatistics.query.filter(StateStatistics.occ_title==my_occ, StateStatistics.state==my_state, StateStatistics.industry_title==my_industry).first()
    if not the_stat:
        return render_template('error.html')
    return render_template('workforce.html', the_stat=the_stat)


if __name__ == '__main__':
    app.run(debug=True)
