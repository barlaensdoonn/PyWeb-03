"""
PYTHON WEB CALCULATOR
run this script and point your browser
at localhost:8080 for usage instructions
"""

# main instructions displayed at server root
response_body = """<html>
<head>
<title>Python Web Calculator Instructions</title>
</head>
<body>
<h1>Welcome to the Python Web Calculator!</h1>
<h2>
--- USAGE ---
</h2>
<h3>
http://localhost:8080/[function]/[#]/[#]
</h3>
<h4>
[function] should be one of:
<ul>
<li>add</li>
<li>subtract</li>
<li>multiply</li>
<li>divide</li>
</ul>
</h4>
<h4>
the # fields correspond to the numbers to operate on
</h4>
<p>for example, http://localhost:8080/subtract/3/15 will yield -12</p>
</body>
</html>"""


def add(*args):
    """ Returns a string with the sum of the arguments """

    result = int(args[0]) + int(args[1])
    return str(result)


def subtract(*args):
    """ returns a string with the difference of the arguments """

    difference = int(args[0]) - int(args[1])
    return str(difference)


def multiply(*args):
    """returns a string with the product of the arguments """

    product = int(args[0]) * int(args[1])
    return str(product)


def divide(*args):
    """ returns a string with the quotient of the arguments """

    quotient = int(args[0]) / int(args[1])
    return str(quotient)


def resolve_path(path):
    """
    Returns 2 values based on the path entered into the browser:
    1) func_name - the math operation to execute
    2) args - the 2 numbers to use for the math operation
    """

    args = path.strip("/").split("/")

    func_name = args.pop(0)

    func = {
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide,
    }.get(func_name)

    return func, args


def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    """
    Main function to parse the path input into the browser,
    call the appropriate function (add, subtract, multiply, or divide),
    and handle any errors, including division by zero
    """

    # initiate headers
    headers = [('Content-type', 'text/html')]
    try:
        # get the specified path
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError

        if path == "/":
            # if we are at root, display instructions
            body = response_body

        else:
            # parse the path to pull out referenced function
            func, args = resolve_path(path)
            body = func(*args)

        # send a 200 OK either way
        status = "200 OK"

    # TODO: add specific exception for wrong number of arguments
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1>Division by zero is impossible</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"

    # fill out start_response and return the body in BYTE encoding
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
