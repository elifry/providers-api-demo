# Providers API

This is a Flask Rest API that manages providers data. It allows users to filter providers by various attributes and skills.

Solution to the [Assignment](/src/assignment.md)

## Features

- Load providers data from a json file
- Filter providers by any attribute
- Filter providers by any active
- Favor providers with fewer matches
- Favor providers with higher rating
- Return providers data as json responses

## Setup and Install

To run this project, you need to have Python 3 and pip installed on your system.

- Clone this repository
- Navigate to the project directory
- Install the required packages using the command `pip install -r requirements.txt` or just use VSCode to install the packages by selecting the python interpreter and selecting the virtual environment
- Run the app using the command `python app.py`
- The app will run on http://localhost:5000 by default
- You can use any tool like Postman or curl to send requests to the app
- Alternatively, you can use the Swagger UI to send requests to the app. To do this, run the app and navigate to http://localhost:5000/docs

## Usage

The app has one route:
- `/providers`

You can add traits separated by commas, with "|" as options within that trait. Note that spaces in requests are replaced with "+".

Here are some examples of requests and responses:

- To get all the providers, send a GET request to `/providers`
- To get all 50 year old providers, send a GET request to `/providers?traits=age:50`
- To get all female providers between the ages 25 and 35, `/providers?traits=sex:female,age:25-35`
- To get the providers who have "Code Refactoring" in their primary skills and "Reusability" as a secondary skill, send a GET request to `/providers?traits=primary_skills:Code+Refactoring,secondary_skill:Reusability`
  - Note that `secondary_skill` is a typo in the assignment.
- To get the providers who are from China and have "Assamese" as their language, send a GET request to `/providers?traits=country:China,language:Assamese`
- Active providers: `/providers?active=true`
- Inactive providers: `/providers?active=false`

And of course you can combine all of these filters.

All results will first be filtered by rating, then by how many times they have been returned, so that providers which have been returned fewer times get put towards the front of the list.