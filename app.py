from datetime import datetime
from flask import Flask,render_template,request
import newsapi 
from newsapi import NewsApiClient
import pickle
import numpy as np
app=Flask(__name__)

model=pickle.load(open('model.pkl','rb'))
@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/news', methods=["POST","GET"])
def news():
    import datetime
    Previous_Date = datetime.datetime.today() - datetime.timedelta(days=2)
    print (Previous_Date)
    Previous_Date_1=datetime.datetime.today()- datetime.timedelta(days=1)
    newsapi= NewsApiClient(api_key="d00c900d0b0d4c038700b4d4901ad795")
    covid=newsapi.get_everything(q="covid", sources="the-times-of-india",
    domains='timesofindia.com', 
    from_param=Previous_Date, to=Previous_Date_1)
    articles=covid['articles']

    desc=[]
    news=[]
    img=[]
    url=[]

    for i in range(min(len(articles),10)):
        myarticles=articles[i]
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        url.append(myarticles['url'])

    mylist = zip(news, desc, img, url)
    return render_template("news.html",context=mylist)

@app.route('/goback', methods=["POST","GET"])
def goback():
    return render_template("index.html")

@app.route('/contact', methods=["POST","GET"])
def contact():
    return render_template("contact.html")

@app.route('/give', methods=["POST", "GET"])
def give():
    return render_template("give.html")

@app.route('/predict',methods=["POST","GET"])
def predict():

    features_list=[]
    # age=request.form.get("Age")
    # print(age)
    for x in request.form.values():
        features_list.append(int(x))
    fin=[np.array(features_list)]
    prediction=model.predict_proba(fin)
    # print(prediction)
    out='{0:{1}f}'.format(prediction[0][1],2)
    # r = requests.get('https://gnews.io/api/v4/search?q=covid19 india&token=932199b4f972e50275048ce13054f085')
    # print(r.json())
    print((out))
    if(out<str(0.5)):
        return render_template("predict.html",prediction="You are Safe! Probability of covid is less than 50%")
    else:
        return render_template("predict.html",prediction="Your probability of covid is "+out)


if(__name__=='__main__'):
    app.run()