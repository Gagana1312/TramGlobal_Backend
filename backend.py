

# print("demo")


#END POINT TO SHORTEN URLS

def shorten_url(long_url, user_tier):
    # Generate a unique short URL for the provided long URL
    # Logic to create a user preferred URL if provided by the user
    # Store the mapping of short URL to long URL in a database

    # Check user tier and decrement request count accordingly

    # Return the shortened URL
    #return short_url


#ENDPOINT TO GET HISTORY

def get_history(user_id):
    # Retrieve all URLs shortened by the given user_id from the database

    # Return the list of shortened URLs
    #return user_urls


#REDIRECTION

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    # Retrieve the long URL associated with the short URL from the database

    # Perform a redirect to the long URL
    #return redirect(long_url)
    
    
#TIER BIASED REQUEST HANDLING

def handle_request(user_tier):
    # Define tiers with corresponding request limits

    # Decrement request count for each request made by the user based on their tier

    # Check if the user has exceeded their limit and handle accordingly
    #if requests_remaining < 0:
        # Return an error or handle request limit exceeded
        pass

    # Allow the request to proceed
    #return "Request processed successfully"
