

"""
How it works: pytest treats the fixture like a generator.
It executes the code up to yield, passes the yielded value (driver) to the test,
and once the test is complete, it resumes the fixture to execute the teardown code that comes after yield.
Robustness: This is fully robust.
If the test fails with an assertion error or any other exception,
pytest guarantees that the teardown code after yield will still be executed.
"""
@pytest.fixture(scope="function")
def driver() -> webdriver.Chrome:
    # --- SETUP CODE ---
    # Everything before the 'yield' runs before your test.
    print("SETUP: Creating Chrome driver...")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)

    # 'yield' passes the driver object to the test and pauses the fixture.
    yield driver

    # --- TEARDOWN CODE ---
    # Everything after the 'yield' runs after your test is finished.
    print("TEARDOWN: Closing Chrome driver...")
    driver.quit()

"""
To achieve the same result with addfinalizer, your code would look like this:
"""
@pytest.fixture(scope="function")
def driver(request) -> webdriver.Chrome:  # Note the 'request' parameter
    # --- SETUP CODE ---
    print("SETUP: Creating Chrome driver...")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)

    # Define an inner function for the teardown logic.
    def finalizer():
        print("TEARDOWN: Closing Chrome driver...")
        driver.quit()

    # Register the inner function to be called after the test.
    request.addfinalizer(finalizer)

    # Return the driver object to the test.
    return driver

"""
When Ever Use addfinalizer?
request.addfinalizer shines in complex scenarios where a single yield block is insufficient, 
typically when you manage multiple resources that need to be torn down independently.

Imagine a fixture that needs to:
1. Create a temporary user via an API.
2. Connect to a database.
3. If the database connection fails, you still want to ensure the temporary user is deleted.

 with yield, you can definitely handle the setup and some teardown, 
 but the main difference is how you manage multiple cleanup steps. 
 After the yield line, you're essentially in a single block of code for teardown. 
 If you have several independent cleanup actions, like closing the browser, 
 deleting temporary files, or rolling back database changes, 
 request.addfinalizer lets you organize those more cleanly. 
 It's about keeping your test code well-structured, especially as your tests get more complex.
 
 Example where it's essential to use the request finalizer:
 if you're testing a system that creates temporary files for processing. 
 You want to make sure those files are deleted after each test, regardless of whether the test passes or fails. 
 With request.addfinalizer, you can register a cleanup function that deletes the files, 
 and pytest will guarantee it runs, even if there are exceptions during the test(!). 

 You could put those cleanup lines after the yield in a single block. 
 The problem is that if any of those lines raise an exception, the rest of the cleanup code won't run. 
 request.addfinalizer ensures each cleanup step is independent, 
 so even if one fails, the others will still execute.leaks.
"""
@pytest.fixture
def user_with_db_session(request, api_client, db_config):
    # Resource 1: Create a user
    print("SETUP: Creating temporary user...")
    user = api_client.create_user()

    # Immediately register the cleanup for the user.
    # This will run even if the database connection below fails.
    request.addfinalizer(lambda: api_client.delete_user(user.id))

    # Resource 2: Connect to the database
    print("SETUP: Connecting to database...")
    db_session = db_config.connect()
    request.addfinalizer(lambda: db_session.close())  # Register DB cleanup

    return user, db_session

"""
In this case, you can register multiple cleanup functions (finalizers), 
and they are guaranteed to be called in the reverse order of registration (LIFO - Last In, First Out). 
This is a level of granular control that yield cannot provide.
"""



