# We're building a matching engine and need your help!

You are tasked with creating a light-weight service for sorting, ranking, and displaying a list of skilled service providers. Providers have several attributes which are filterable.

The service should factor in these attributes as well as factors related to the use of the service when generating results.

Below are several user stories which outline the functionality expected in this service, as well as an attached `.json` file with some mock provider data to seed the project. The service can be expressed in any way you choose, as long as there is an interface to generate a list of providers based on the requirements in the user stories.

Please use Python to code the service.

## User Stories

- I would like to be able to exclude/include certain providers from results based on their active property
- I would like to be able to filter through providers on a combination of any of their user traits
- I would like the order of results to adjust based on how many times a provider has been returned; surfacing providers who have been returned fewer times towards the front of the list.
- I would like higher ranked providers to always be surfaced towards the front of the list.

### The user stories purposefully leave room for interpretation and flexibility in how you decide to implement them; don't overthink them. The point of this exercise is to create a body of work we can discuss / review in the followup. Feel free to bring in any other interesting ideas/concepts you would like in a matching engine.

## Things we're looking out for in our review:

- Extensibility of code
- Consistency
- Organization of code
- Familiarity with Python
- Documentation if necessary
- Tests

 