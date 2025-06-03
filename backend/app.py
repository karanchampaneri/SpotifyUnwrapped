from flask import Flask, request, jsonify #imports flask and tools for routing, handling data, and retorning json responses

app = Flask(__name__) #create a Flask application instance

# A sample API route
@app.route('/') # -> A simple homepage route, When you visit localhost:5000, this function will be called
def home():
    return "Welcome to the Flask App!"

@app.route('/roast', methods=['POST']) # -> This listens for POST requests at /roast. It expects JSON data and sends a roast back.
def roast():
    user_data = request.json
    #for now just echo the input back
    return jsonify({
        "roast" : f"This is a sample roast for: {user_data}"
    })


if __name__ == '__main__':
    app.run(debug=True)

