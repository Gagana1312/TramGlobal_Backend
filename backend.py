

# print("demo")
import random
import string


from flask import Flask, render_template, redirect, request

app = Flask(__name__)
shorten_url = {}



def generate_short_URL(length = 8):
    letters = string.ascii_letters + string.digits
    short_url=  ''.join(random.choice(letters) for _ in range(length))
    return short_url



@app.route('/', methods=['GET','POST'])


def index():
    if request.method =='POST':
        long_url =request.form['long-url']
        short_url =generate_short_URL()
        while short_url in shorten_url:
            short_url = generate_short_URL()
        shorten_url[short_url] = long_url
        return f"Shortened URL :{request.url_root}{short_url}"
    return render_template("index.html")

@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = shorten_url.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found",404
    
    
if __name__=="__main__":
    app.run(debug=True)
    


