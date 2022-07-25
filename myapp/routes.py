from myapp import app

@app.route("/")
@app.route("/index")
def index():
    return "Hello World!"


@app.route("/post")
def post():
    return """
        <!DOCTYPE html>
        <html>
        <head>
        <title>Post page</title>
        </head>
        <body>
        <h1>Post page</h1>
        <p>This is sample post</p>
        </body>
        </html>
    """