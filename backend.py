

# print("demo")
import random
import string


from flask import Flask, render_template, redirect, request

app = Flask(__name__)
shortened_url = {} 


def generate_short_URL(length = 6):
    letters = string.ascii_letters + string.digits
    short_url=  ''.join(random.choice(letters) for _ in range(length))
    return short_url



@app.route("/", methods=["GET","POST"])

def index():
    
    if request.method == "POST":
        print("Received POST request")
        long_url = request.form['long_url']
        short_url = generate_short_URL()

        while short_url in shortened_url:
            short_url = generate_short_URL()

        shortened_url[short_url] = long_url
        print("Updated shortened_url:", shortened_url)
        return render_template("index.html", shortened_url=f"{request.url_root}{short_url}")
    
    print("Rendering index.html")
    return render_template("index.html")



@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = shortened_url.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404
    
    
if __name__=="__main__":
    app.run(debug=True)
    


