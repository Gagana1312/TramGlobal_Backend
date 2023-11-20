

# print("demo")
import random
import string
import json


from flask import Flask, render_template, redirect, request

app = Flask(__name__)
shortened_url = {} 
users = {}



def generate_short_URL(length = 6):
    letters = string.ascii_letters + string.digits
    short_url=  ''.join(random.choice(letters) for _ in range(length))
    return short_url



@app.route("/", methods=["GET", "POST"])
def index():
    global users

    if request.method == "POST":
        user = request.form.get('user')
        if user:
            # If the user doesn't exist, initialize the user's data
            users.setdefault(user, {"tier": None, "requests_left": None, "history": []})
            selected_tier = users[user]["tier"]
            requests_allowed = users[user]["requests_left"]
            if selected_tier is None:
                selected_tier = int(request.form.get('tier'))
                requests_allowed = {
                    1: 1000,
                    2: 500,
                    3: 100,
                }.get(selected_tier, 10)  

            if users[user]["tier"] is not None:
                requests_allowed = users[user]["requests_left"]

            users[user].update({"tier": selected_tier, "requests_left": requests_allowed})

            if requests_allowed and requests_allowed > 0:
                long_url = request.form['long_url']
                custom_short_url = request.form.get('custom_short_url')

               # Check if either long_url or custom_short_url is provided and not empty
                if long_url or custom_short_url:
                    url_to_shorten = long_url if not custom_short_url else custom_short_url
                    short_url = generate_short_URL() 
                    
                    while short_url in shortened_url:
                        short_url = generate_short_URL()

                    shortened_url[short_url] = {"long_url": url_to_shorten, "user": user}
                    requests_allowed -= 1

                    users[user]["requests_left"] = requests_allowed
                    users[user].setdefault("history", []).append(short_url)

                    with open("urls.json", "w") as f:
                        json.dump([shortened_url, users], f)

                    return render_template("index.html", shortened_url=f"{request.url_root}{short_url}", username=user)
                else:
                    return "Please provide either a long URL or a custom short URL", 400

            return "Request limit reached for this tier", 403
        return "User not found or unauthorized", 401

    return render_template("index.html")




@app.route("/<short_url>")
def redirect_url(short_url):
    if short_url in shortened_url:
        long_url = shortened_url[short_url]["long_url"]
        # Log redirection or perform analytics here if needed
        return redirect(long_url)
    else:
        return "URL not found", 404
    
    
    
@app.route("/history/<username>")
def user_history(username):
    if username in users:
        user_history = users[username].get("history", [])
        return render_template("history.html", user=username, history=user_history)
    else:
        return "User not found", 404
    
if __name__ == "__main__":
    with open("urls.json", "r") as f:
        data = json.load(f)
    app.run(debug=True, port = 8000)
    
    