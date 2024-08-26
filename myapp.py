
def app(environ, start_response):
        data = b"This is the home page\n"
        start_response("200 OK", [
            ("Content-Type", "text/plain"),
            ("Content-Length", str(len(data)))
        ])
        return iter([data])