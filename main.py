"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask
from flask.ext.wtf import Form
from wtforms import StringField, IntegerField
from flask import render_template, flash, redirect
import random

app = Flask(__name__)
app.secret_key = '12456732456787652353465u57645hrtshsrth'
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


class DataEntryForm(Form):
    people = StringField('people')
    num_presents = IntegerField('num_presents')


def doit(people, num_presents_to_buy):
    picked = []

    allocations = {

    }

    presents_bought = {

    }

    for person in people:
        print person
        people_left = list(people)
        people_left.remove(person)
        for p in picked:
            people_left.remove(person)

        allocations[person] = []

        while len(allocations[person]) < num_presents_to_buy:
            if not people_left:
                print "no more people"
                break
            if len(people_left) > 1:
                index = random.randint(0, len(people_left) - 1)
            else:
                index = 0
            candidate = people_left[index]
            print " => {}".format(candidate)
            if candidate in presents_bought and presents_bought[candidate] == num_presents_to_buy:
                print "candidate already has 3 presents"
                people_left.remove(people_left[index])
            else:
                if candidate not in allocations[person]:
                    allocations[person].append(candidate)
                    if candidate not in presents_bought:
                        presents_bought[candidate] = 0
                    presents_bought[candidate] += 1
                    people_left.remove(candidate)
                else:
                    print "already buying for candidate"

    return allocations, presents_bought


def calculate_matrix(people, num_presents):
    done = False
    while not done:
        done = True
        allocations, presents_bought = doit(people, num_presents)
        for person, num in presents_bought.iteritems():
            if num != num_presents:
                done = False
                break
    return allocations


@app.route('/', methods=['GET', 'POST'])
def hello():
    """Return a friendly HTTP greeting."""
    form = DataEntryForm()
    if form.validate_on_submit():
        results = calculate_matrix(form.people.data.split(','), form.num_presents.data)
        return render_template('results.html', results=results)
    return render_template('data_entry.html', title="Present Matrx", form=form)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
