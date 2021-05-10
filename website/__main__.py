# flask_s3_uploads/__init__.py
import tweepy as tw
from flask import Flask,request ,render_template,redirect,url_for,flash
from .twitter_searcher import twitter_search
import pygal
app = Flask(__name__, template_folder='templates')

#Flask has different decorators to handle http requests. Http protocol is the basis for data communication in the World Wide Web.



@app.route("/dashboard/", methods=['GET'])
def dashboard():
        df = request.args.getlist('df')
        barChart = pygal.HorizontalBar()
        for i in df:
            res = i.strip('][').split(', ')

            barChart.add(res[0], int(res[1]))
            print(res[0],res[1])

        graph_data = barChart.render_data_uri()
        return render_template("dashboard.html", graph_data=graph_data)






@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = request.form['searchtext']
        usr = twitter_search(search_string = user,item_cnt=1000)
        return redirect(url_for("dashboard",df=usr))
    else:
        return render_template("index.html")



if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
