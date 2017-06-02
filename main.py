from flask import Flask, render_template, url_for, redirect, request
from werkzeug.utils import secure_filename
import os
import psycopg2
from utilities import execute_sql_statement

app = Flask(__name__)


@app.route('/')
def index():
    '''
    It shows a list of links which are pointing to specific roots.

    '''
    return render_template('index.html')


@app.route('/mentors')
def mentors():
    '''
    On this page you should show the result of a query
    that returns the name of the mentors plus the name and country
    of the school (joining with the schools table) ordered by the
    mentors id column (columns: mentors.first_name, mentors.last_name, schools.name, schools.country).

    '''
    mentor_data = execute_sql_statement("""SELECT mentors.first_name, mentors.last_name, schools.name, schools.country
                                           FROM mentors
                                           INNER JOIN schools
                                                ON schools.city = mentors.city
                                           ORDER BY mentors.id ASC;""")
    return render_template('mentors.html', data_set=mentor_data)


@app.route('/all-school')
def all_school():
    '''
    On this page you should show the result of a query
    that returns the name of the mentors plus the name and country
    of the school (joining with the schools table) ordered by the mentors id column.
    BUT include all the schools, even if there's no mentor yet!
    columns: mentors.first_name, mentors.last_name, schools.name, schools.country
    '''
    all_school_data = execute_sql_statement("""SELECT mentors.first_name, mentors.last_name, schools.name, schools.country
                                               FROM mentors
                                               RIGHT JOIN schools
                                                 ON schools.city = mentors.city
                                               ORDER BY mentors.id ASC;""")
    return render_template('all_school.html', data_set=all_school_data)


@app.route('/mentors-by-country')
def mentors_by_country():
    '''
    On this page you should show the result of a query
    that returns the number of the mentors per country
    ordered by the name of the countries columns: country, count
    '''
    country_data = execute_sql_statement("""SELECT schools.country, COUNT(mentors.city) AS Number_of_mentors
                                            FROM mentors
                                            INNER JOIN schools
                                               ON schools.city = mentors.city
                                            GROUP BY schools.country;""")
    return render_template('country.html', data_set=country_data)


@app.route('/contacts')
def contacts():
    '''
    On this page you should show the result of a query
    that returns the name of the school plus the name of
    contact person at the school (from the mentors table) ordered by the name of the school
    columns: schools.name, mentors.first_name, mentors.last_name
    '''
    contacts_data = execute_sql_statement("""SELECT schools.name, mentors.first_name, mentors.last_name
                                             FROM mentors
                                             INNER JOIN schools
                                                ON mentors.id = schools.contact_person
                                             GROUP BY schools.name, mentors.first_name, mentors.last_name
                                             ORDER BY schools.name ASC;""")
    return render_template('contacts.html', data_set=contacts_data)


@app.route('/applicants')
def applicants():
    '''
    On this page you should show the result of a query
    that returns the first name and the code of the applicants
    plus the creation_date of the application (joining with the applicants_mentors table)
    ordered by the creation_date in descending order BUT only for applications later than 2016-01-01
    columns: applicants.first_name, applicants.application_code, applicants_mentors.creation_date
    '''
    applicants_data = execute_sql_statement("""SELECT applicants.first_name, applicants.application_code, applicants_mentors.creation_date
                                               FROM applicants
                                               INNER JOIN applicants_mentors
                                                    ON applicants_mentors.applicant_id = applicants.id
                                               WHERE applicants_mentors.creation_date > '2016-01-01'
                                               GROUP BY applicants.first_name, applicants.application_code,
                                                        applicants_mentors.creation_date
                                               ORDER BY applicants_mentors.creation_date DESC;""")
    return render_template('applicants.html', data_set=applicants_data)


@app.route('/applicants-and-mentors')
def applicants_and_mentors():
    '''
    On this page you should show the result of a query
    that returns the first name and the code of the applicants
    plus the name of the assigned mentor (joining through the applicants_mentors table)
    ordered by the applicants id column
    Show all the applicants, even if they have no assigned mentor in the database!
    In this case use the string 'None' instead of the mentor name
    columns: applicants.first_name, applicants.application_code, mentor_first_name, mentor_last_name
    '''
    applicants_and_mentors_data = execute_sql_statement("""SELECT applicants.first_name, applicants.application_code, mentors.first_name, mentors.last_name
                                                           FROM applicants
                                                           LEFT JOIN applicants_mentors
                                                                ON applicants_mentors.applicant_id = applicants.id
                                                           LEFT JOIN mentors
                                                                ON mentors.id = applicants_mentors.mentor_id
                                                            GROUP BY applicants.id, applicants.first_name, 
                                                                     applicants.application_code, mentors.first_name, 
                                                                     mentors.last_name
                                                            ORDER BY applicants.id ASC;""")
    return render_template('applicants_and_mentors.html', data_set=applicants_and_mentors_data)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()