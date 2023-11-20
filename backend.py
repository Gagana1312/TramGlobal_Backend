

# print("demo")
import random
import string
import json


from flask import Flask, render_template, redirect, request

app = Flask(__name__)
shortened_url = {} 
users = {
    "ABC": {"password": "abc123", "tier": 1, "requests_left": 1000},
    "XYZ": {"password": "xyz456", "tier": 2, "requests_left": 100},
    # Add more users as needed
}



def generate_short_URL(length = 6):
    letters = string.ascii_letters + string.digits
    short_url=  ''.join(random.choice(letters) for _ in range(length))
    return short_url



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user = request.form.get('user')
        if user in users:
            if users[user]["requests_left"] > 0:
                long_url = request.form['long_url']
                custom_short_url = request.form.get('custom_short_url')

                if custom_short_url:
                    if custom_short_url in shortened_url.values():
                        return "Custom URL already in use", 400
                    short_url = custom_short_url
                else:
                    short_url = generate_short_URL()
                    while short_url in shortened_url:
                        short_url = generate_short_URL()

                shortened_url[short_url] = {"long_url": long_url, "user": user}
                users[user]["requests_left"] -= 1

                # Update user's history of shortened URLs
                users[user].setdefault("history", []).append(short_url)

                with open("urls.json", "w") as f:
                    json.dump([shortened_url, users], f)

                return render_template("index.html", shortened_url=f"{request.url_root}{short_url}")
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
    
    
if __name__ == "__main__":
    with open("urls.json", "r") as f:
        data = json.load(f)
    app.run(debug=True, port=8000)
    
    