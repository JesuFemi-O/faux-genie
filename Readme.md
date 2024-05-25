# Faux Genie

The idea here is to create a simple system that's capable of:

- Generating fake events data that follow a realistic date sequence, mimicing common events that are generated in an e-commerce website
- allowing users interact with the data generator via a cli application to write data to a postgres application
- exposing APIs with token based authentication to retrieve the fake data

## Project Motivation
Learning to build custom Data ingestion capabilities for API based sources means that you need access to a production grade API to work it. The challenge for most learners is that they don't have access to a shopify or Paypal account for example, that will enable them to learn to develop custom ETL/ELT pipeline.

One of the Biggest challenge when learning advanced ETL concepts is dynamic data. Lack of dynamic data makes it difficult to practice concepts like incremental data loading and backfills.

Faux-Genie is a data generator and API service that will generate and serve data to users allowing them to build interesting ETL/ELT systems.

Personally, I have developed Faux-Genie to let me learn/master using tools like Meltano and DLTHub for ingesting API sources. I have also set some standards for how I intend to develop this project. at the time of development of this project, I'm actively reading Robert Viafore's Robust python and so this project is also an excuse to put my knowledge to practice. Note that, I'm actively studying multiple Software and data engineering concepts to develop this project and at the end of this project I should have brushed up on things like:

- Data validation with Pydantic Models
- Using ORMs in Python (SQLalchemy)
- Developing APIs with FastAPI
- Event Driven Microservices using RabbitMQ*
- Unit Testing

# Project Structure

```bash

.
├── Readme.md
├── aladdin
├── docker-compose.yml
├── faux
│   ├── Readme.md
│   ├── faux
│   │   ├── __init__.py
│   │   ├── config
│   │   │   └── products.json
│   │   ├── core
│   │   │   ├── __init__.py
│   │   │   ├── faux_utils.py
│   │   │   └── models.py
│   │   ├── database
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── db_models.py
│   │   │   └── db_utils.py
│   │   ├── main.py
│   │   └── simulator
│   │       ├── sim_helpers.py
│   │       └── sim_utils.py
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── test_faux
├── genie
└── ideas
    └── scratchpad.md

```

# Known Limitations

- The timestamp value in the customer table can be somewhat misleading and this because of how we simulate historic visits
- The order_line_items table has all items that were added to cart instead of final items in cart at the point of checkout. This is deliberate and should be considered an "engineering team bug that will be fixed in the 'future' ".
- The remove from cart event isn't as dynamic as one would expect...You can only delete an item from the cart, you cannot modify qty
- Faux is designed to force you to consider the events table as your single source of truth

# What I'm looking to improve on in the nearest Future
- Data is first generated as a json object / python dictionary... users shouldn't have to rely on postgres as it's a sink. So I'm looking to achieve more loos coupling between source and "sinks"

- At the moment, a customer can only order once, I'll like to iterate this work to a point where customers who abandonned their cart in a previous shopping session can comeback and attempt to successfully checkout while customers who successfully checkedout can start a new shopping session. Because of the concept of historic visits, I'm unable to think of a clean way to do this at the moment while still maintaining high degree of loose coupling between the code generator and the database, and I'm yet to formalise the conepts of sinks, so if data was previously dumped to a JSON file for example how do i achieve this? if you have some ideas please reach out!!


# The wildcards!

- I have this crazy idea to add another service called `Kingfisher` to let me explore the possibilites of building an MLOPS system where I have api services working in async to prepare training data, trigger model development, deployment and inference and this would be powered by pub/sub or rabbitMQ... This is rather far fetched at the moment and is not a priority for me but reach out if you'll like to hear more about it!


# What the (ideal) final system should have:

- Faux: The data generator & core engine
- Genie: The API service to return fake data powered by Faux
- Aladdin: The cli service to generate fake data Powered by Faux
- KingFisher: The MLOPs system designed to build and Serve ML models based on Faux Data
