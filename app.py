import pickle
from flask import Flask
import mysql.connector as mysql
from flask import render_template,request,redirect

app = Flask('urlFinder')

connections = mysql.connect(user='root'
                            ,database='url_project',
                            host='localhost')

def makeTokens(f):
    tkns_BySlash = str(f.encode('utf-8')).split('/')	# make tokens after splitting by slash
    total_Tokens = []
    for i in tkns_BySlash:
        tokens = str(i).split('-')	# make tokens after splitting by dash
        tkns_ByDot = []
        for j in range(0,len(tokens)):
            temp_Tokens = str(tokens[j]).split('.')	# make tokens after splitting by dot
            tkns_ByDot = tkns_ByDot + temp_Tokens
        total_Tokens = total_Tokens + tokens + tkns_ByDot
    total_Tokens = list(set(total_Tokens))	#remove redundant tokens
    if 'com' in total_Tokens:
        total_Tokens.remove('com')	#removing .com since it occurs a lot of times and it should not be included in our features
    return total_Tokens

@app.get('/')
def home():
    return render_template('home.html')

@app.get('/signUp')
def signUp():
    return render_template('signUp.html')

@app.post('/signUp')
def create_user():
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    email = request.form.get("email")
    password = request.form.get("password")
        
    cursor = connections.cursor()
    cursor.execute(f"INSERT INTO `users`(`first_name`, `last_name`, `email`,`password`) VALUES ('{firstname}','{lastname}','{email}','{password}');")
    connections.commit()
    cursor.close()
    return redirect('/search')

@app.get('/signIn')
def signIn():
    return render_template('signIn.html')

@app.post('/signIn')
def verify_user():
    email = request.form.get("Eemail")
    password = request.form.get("Epassword")
    cursor = connections.cursor()
    cursor.execute(f"SELECT `email` FROM `users` WHERE email = '{email}' AND password = '{password}';")
    data = ''
    user = cursor.fetchall()
    connections.commit()
    cursor.close()
    if not user:
        return render_template('/signIn.html',TOGGLE='EMAIL OR PASSWORD IS WRONG, PLEASE CHECK') 
    else:
        return render_template('/searchBox.html')

@app.get('/search')
def search_page():
    return render_template('searchBoxv2.html')


@app.post('/search')
def url_ins():
    url = request.form.get('inp')

    with open('ensemble_model.pkl', 'rb') as model_file:
        ensemble = pickle.load(model_file)

# # Load the fitted TF-IDF vectorizer
    with open('tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)

# # Example URL for prediction
    new_url = []
    new_url.append(url)

# # Transform the new URL using the loaded vectorizer
    X_predict = vectorizer.transform(new_url)

# # Make predictions using the loaded model
    predictions = ensemble.predict(X_predict)

# Print the predictions
    # if predictions[0] == 'bad':
    #     return 'bad'
    # else:
    #     return 'good'
    if predictions[0] == 'bad':
        return render_template('searchBoxv2.html',A=str(0))
    else:
        return render_template('searchBoxv2.html',A=str(1))
    
    
app.run(debug=True)