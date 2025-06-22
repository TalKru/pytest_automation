import pytest


class Customer:
    pass


# tests/conftest.py
@pytest.fixture
def make_customer():
    def make(first_name: str = "Cosmo", last_name: str = "Kramer", email: str = "test@example.com", **rest):
        customer = Customer(first_name=first_name, last_name=last_name, email=email, **rest)
        return customer

    return make


# tests/test_00.py
def test_customer(make_customer):
    customer_1 = make_customer(first_name="Elaine", last_name="Benes")
    assert customer_1.first_name == "Elaine"
    customer_2 = make_customer()
    assert customer_2.first_name == "Cosmo"


"""
HOW IT WORKS:
**Getting a Function from the Fixture:** The `make_customer` fixture doesn't give you a `Customer` object directly. 
Instead, it gives you a function (which we named `make` in that example).

**Object Constructor Functionality:** This `make` function *acts like* a specialized constructor or "factory method." 
You call it to create instances of your `Customer` class.

**Dynamic Object Creation at Runtime:** Within your test function, 
you can call this `make` function as many times as you need, passing different parameters each time. 
This allows you to create various `Customer` objects dynamically, tailored to the specific scenario of that test.

**Avoiding Hard-Coded Objects:** This is the key benefit. Instead of having a single, pre-defined, 
and potentially rigid `Customer` object provided by a simple fixture 
(which would be something like `@pytest.fixture def customer(): return Customer("Cosmo", "Kramer", "test@example.com")`), 
the factory fixture gives you the power to generate any kind of `Customer` you need, on demand, within the test.

This pattern is incredibly powerful for:
**Testing different scenarios:** You can easily create a "regular" customer, a "premium" customer, a "customer with no email," etc., all from the same fixture.
**Reducing code duplication:** The logic for creating a customer is centralized in the fixture, so you don't have to repeat it in every test.
**Improving readability:** Tests become cleaner as they focus on *what kind* of customer they need, rather than the details of *how* to construct it.

It's a staple in more advanced pytest usage, especially when dealing with complex data models or objects that have many variations.

...

First, let's assume you have a Customer class defined somewhere, like this:

class Customer:
    def __init__(self, first_name, last_name, email, **kwargs):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.extra_data = kwargs # To handle any other keyword arguments



Now, let's look at the make_customer fixture:

import pytest

@pytest.fixture
def make_customer(): # This is our fixture
    # This 'make' function is what the fixture *returns*
    def make(
        first_name: str = "Cosmo",
        last_name: str = "Kramer",
        email: str = "test@example.com",
        **rest # This captures any other keyword arguments you pass
    ):
        # Inside 'make', we create an instance of the Customer class
        customer = Customer(
            first_name=first_name, last_name=last_name, email=email, **rest
        )
        return customer

    return make # The fixture returns the 'make' function itself not a customer instance



What make does:

In this context, make is not a special keyword in Python or pytest. It's simply the name of a function that the make_customer fixture returns.

Think of it this way:

@pytest.fixture: This decorator tells pytest that make_customer is a fixture.
def make_customer():: When a test needs make_customer, pytest calls this function.
def make(...):: Inside make_customer, another function named make is defined. 
This make function is designed to create a Customer object. 
It has default values for first_name, last_name, and email, but you can override them. 
The **rest allows you to pass any other attributes to the Customer constructor.
return make: The crucial part! The make_customer fixture doesn't return a Customer object directly. 
Instead, it returns the make function itself.

How test_customer uses it:

def test_customer(make_customer): # pytest injects the 'make' function here
    # make_customer is now the 'make' function that was returned by the fixture
    customer_1 = make_customer(first_name="Elaine", last_name="Benes")
    assert customer_1.first_name == "Elaine"
    customer_2 = make_customer() # Calls 'make' with default arguments
    assert customer_2.first_name == "Cosmo"



When test_customer asks for make_customer, pytest runs the @pytest.fixture def make_customer(): function.
That fixture then returns the inner make function.
So, inside test_customer, the variable make_customer is now actually the function that can create customers.
You can then call make_customer() (which is really calling the inner make function) as many times as you need within your test, 
passing different arguments to create different Customer objects.

Why is this useful? (The "factory" part)

This pattern is called a "fixture factory" because the fixture (make_customer) 
acts as a factory for creating test data (the Customer objects).

Flexibility: Instead of getting a single, pre-made Customer object, you get a tool (the make function) 
that lets you create multiple Customer objects, each with specific details tailored to your test.
Customization: You can easily override default values (first_name="Cosmo") for specific tests without 
having to write a whole new fixture or re-initialize objects manually.
Reusability: You define the customer creation logic once in the fixture, 
and then any test can use make_customer to get a custom customer.
Reduced boilerplate: Imagine if you had to create a new Customer object with all its default values in every test where you needed one. 
This factory fixture streamlines that.
In summary:

The make_customer fixture provides a function (named make) that you can call in your tests to create instances of Customer with various configurations. 
It's like a specialized tool-maker for your test data. 
You ask the fixture for the tool, and then you use the tool to make as many customized Customer objects as you need within that test.
"""