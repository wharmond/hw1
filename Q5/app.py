from flask import Flask,render_template, request,json
app = Flask(__name__)

@app.route("/")
def hello():
    #return("hello world!")
    return(render_template('hello.html'))

@app.route("/signUp")
def signUp():
    return(render_template('signUp.html'))

@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user =  request.form['username'];
    password = request.form['password'];
    if ((len(password)>7) and (any(c.isdigit() for c in password)) and (any(c.isupper() for c in password))):
                return json.dumps({'status':'OK','user':user,'pass':password});
    else:
        return json.dumps({'status':'BAD','user':user,'pass':[1,3]});
        
if __name__ == "__main__":
    app.run()