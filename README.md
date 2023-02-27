# Lyes HAMIDOUCHE's technical test

This project was generated via [manage-fastapi](https://ycd.github.io/manage-fastapi/)!


# To run the project
Requirements:
 - docker (Install information [here](https://docs.docker.com/get-docker/))
 - docker-compose (Install information [here](https://docs.docker.com/compose/install/))

Follow the steps below:

```bash
cd </path/to/this/folder> # the path where you did put this folder
docker-compose build
docker-compose up -d
docker-compose exec database bash /var/tmp/setup.sh
```
To stop the server
```bash
cd </path/to/this/folder> # the path where you did put this folder
docker-compose stop
```

What I did to populate data (I skipped bien-dans-ma-ville.fr pages parsing):
- I started from an empty database
- I launched the script below on a database that has been freshly set up
  ```bash
  scripts/populate_empty_database_with_rent_indicators.py --filepath initdata/indicateurs-loyers-appartements.csv --encoding iso-8859-1
  ```
- I created a dump.

To play with it:
- FastAPI, you know the deal, once the server is running [http://localhost:8000/docs](http://localhost:8000/docs)

## Disclaimer about what has been done here


- This technical test has been done by a developer which is very familiar with Django + Django Rest Framework.

The test has been made with these ideas in mind:

- Since the focus was on only one route (function) routing has not been tackled here.
  - Absolutely aware of its importance. I'll leave it there for the exercice.
- Inputs must be validated (Serialization + Validation + Deserialization)
- Easy to deploy
  - Docker + docker-compose configuration
  - A ready to use database dump (almost realistic dump included inside the code)
- Must have its own structure
  - A file for Schemas
  - A file for Models
  - A package for external services (such as Government API service or Scrapping bien-dans-maville.com)
- Documented when needed
- Tested
  - I must confess about one thing, since I'm new with such framework, some tests have not been done. In real life I would have been testing everything.
- Most of the operations that have been done here might seem simplistic but the idea was to provide you with a code that works with no big trouble.


# After reading the exercise

The stated problem being mentioned, the development of the project were the following:
 - Upgrade my knowledge about FastAPI
 - Model specification  and Code architecture
 - Experiment approaches to retrieve informationsabout city rating (Bien dans ma ville)
 - Find a way to provide you with a ready to use code
 - Try to make the solution performant enough
   - I tested a solution that would create the objects as long as we request database but I had queries lasting 2+ minutes due to website parsing

# Model

We divided model into 4 entities:
- Department
- City: which hold the information about the city (department, insee code, population)
- ApartmentRentIndicator (square meter ret price)
- CityZipcpde (we could have used a string to reference zipcodes, since some cities have many zipcodes, instantiate an object per zipcode)

### Thoughts:

- This model makes it easy to be extended to region, country.
- Being not comfortable a lot with SQLAlchemy I'm not sure if there would be a more
  efficient way to query database in a django way ("ex" filter(city__department__code=). Thus, even
  if I'm not proud with the foreign key to Department added to `ApartmentRentIndicator`, it kind of does the job to quickly
  filter on all the cities of a department in a single query.
- Using a unique table would have been a simpler way to query informations (instead of joining other tables to perform the request).
However, splitting the model into 4 entities enables separating responsibilities.
# Challenges and Technical choices
## City rating:
With the resources given, I've tried to look for a way to find a database or a csv file I could exploit.
I even had a look to "kelquartier" or "ville idéale" to see if there was an api or something like that could
be used in a more convenient way. Having to look for a solution anyway. I chose to use what the website provided me as information.
- A search url to query my search, which is unfortunately only uses city names to perform some search queries.
  - The search url provides with a link which I could suffix with "avis.html" to access to rating page
- I used beautifulsoup to parse web pages and access their content conveniently.
  - Unfortunately I do not know how it is compared to other alternatives on the market.
  - Anyway, as it did the job for me. It was perfect.


## Response time:
The app having to answer within a very quick time. Performance could not be
provided directly at a first call, because:
- With no information in DB, we would have to call GeoService to populate database with administrative informations
  such as city, department, population, ...etc.
- Parsing many web pages for ratings could be time and resource consuming.

To summarize, performance would come from data that have been already pre-computed.
For the exercise, I assumed that our database would be initially set up with
the apropriate data. The script `scripts/populate_empty_database_with_rend_indicators.py`
An example of What a worker would look like. I commented in it the
line where we call the site that retrieves the rating of the city and replaced it with a random
`float` in order to be able to provide you a database dump that you could use directly to play with.

# Asynchronous computation --> another potential solution
One kind of solution that I would implement if I had more time. If not retrieving cities rating immediately at call
is an option.
- Parse the CSV file provided by governement and insert department, cities and rent related informations.
- City Rating could be used in way in db for example:
  - -1 if not computed yet (can be used to launch a task that retrieves it asynchronously with a tool such as celery or any equivalent tool that works with fastapi)
  - None if not found
  - a value `x` with 0 <= `x` <= 5 if found.
- Same treatment could be applied for the other informations (population , ...)


# Summary

My concerns in my code, at least some of them:
- A simple and easily maintainable code architecture (I tried to document myself about good naming on FastAPI but I'm conditionned a little bit by Django Framework)
  - Separated database models, models (validators and serializers), services files, tests
  - Data setup. I deliberately added it in order to give you the opportunity to paly with code. However, service files seem to be operationnal.
  - Documentation when it brings value to the code.
  - I used `manage-fastapi` tool because I found it helpful for what I wanted to do. (pre-commit, scaffolding a project quickly, ...etc.)
- Logging, there are some missing, and logs are not very detailed or formated but focused on services
- Documentation, but only when it brings value to code (especially when it holds business related information)
- Inputs and Outputs: Data Validation and Rendering `pydantic`.
- Queries: Indexes on some columns suspected to be used intensively for querying.
- Migration management: not seen here but when it's possible to squash many migrations, we should do it.
- [Not done enough here] Unit tests + did not mock tests
- [Skipped Here] Asynchronous tasks to perform any computation supposed to be long.
- [Skipped Here] A cache could help improve performance
  - Database objects caching
  - Caching results for next calls if useful
- [Skipped Here] Continuous Integration. Github actions or Gitlab CI could be helpful in a real life case.
- [Skipped Here] A more professionnal import script or any other procedure
  - Checks whether infos exist on db or not ... (other checks)

# Conclusion
No matter whether you want the following of the recruitement process. I'm very thankful for having the opportunity to do this test
and play a little bit with FastAPI for the first time. Any advice or recommendation will be highly appreciated and will help me improve on this framework.
