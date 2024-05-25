# Faux-Genie Idea board

## Development strategy

- we can use SQLAlchemny to build the tables in Faux and use our pydantic models to validate incoming data

- Tables to create:
    - Users 
    - Product
    - Event

- We need an ORM to build the request server that will connect to these tables and retrieve data.

- For the APIs first pass, we'll want paginated requests for:
    - GET /users
    - GET /products
    - GET /events by type(optional), start_date(required), end_date(optinal)

- All resources will be protected using token based auth

- We can setup an admin endpoint to generate new data
    - the idea here is to Use Genie to send a request to KingFisher
    - Faux will powered by KingFisher - A queuing service that will asynchronously fulfill data generation  requests based on a a start and end date

## Challenges I'm thinking through

- in my initial POC I was simulating historical visits that could Go a few days in the past for a customer before I start creating shopping events. The problem is that this historical events can lead to an issue if I'm ingesting the data incrementally into a destination. cos if I run the pipeline to add new data after syncing to a DWH it can create records from the past that will not be present in my DWH.

- To solve this problem, my strategy will be to have two type of data load
    - Init/historical run where I can simulate new visits
    - single runs where I won't try to create any historical visits

- Another challenge at the moment is finding a smart way to allow users make multiple orders.
    - The system is currently in a naive state where customers only complete a single order(Max 1 successful checkout per customer) or abandon their carts
    - I need a way to find customers whose previous order was successful to let them start new orders
    - I also need a smart way to identify events associated with a particular checkout


## Nice To Have:
- shipments could be a good idea to extend the application
    - we can generate a series of events showing how many times we attempt to deliver an order
    - for most customers we will deliver on first attempt
    - for a small percentage of customers we will make multiple attempts
    - delivery will transition from SHIPED -> Delivered -> Failed-Attempt [Max 2 retry] -> Failed 
    - the flow for failed delivery will be [shipped, failed_attempt, shipped, failed_attempt, shipped, failed]
    - When a delivery fails, we will process a refund to customer (This will be reflected in the Payments table)
    - orders cannot be cancelled after they have been paid for, refunds will only be 50% of Order value
- GraphQL endpoints
- one-to-many relationship models
    - Loans
    - LoanPayments
    a loan can have one to many payment installments



```python

# generate a customer
# customer = generate_new_users(num_users=1)[0]

# generate historic visits
    # 0 to many visits
    # whenever we run the simulator, we'll have:
    # window shoppers
    # future buyers - add/remove items/ cancel checkouts
    # buyers - successful / failed checkouts

# simulate window shopping
    # find 2-5 users from DB
    # generate 1 or 2 new users
    # for each user generate 2 - 5 visit events and event_date must not be earlier than their creation_date

# simulate future buyers
    # fetch 3 - 7 users from the DB
    # optionally generate a 1 to 3 users
    # for each user make a visits
    # make n add to cart events
    # make 0 to n remove from cart events
    # initiate a cancelled checkout if active cart > 0

# simulate buyers 
    # fetch 3 - 7 users from the DB
    # optionally generate a 1 to 3 users
    # for each user make a visits
    # make n add to cart events
    # make 0 to n-1 remove from cart events
    # initiate a successful or failed checkout 

```