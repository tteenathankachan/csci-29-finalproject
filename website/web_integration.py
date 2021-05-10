from flask import Flask,request ,render_template,redirect,url_for,flash
from twitter_search_lib import twitter_search
import pygal

app = Flask(__name__, template_folder='templates')

#@app.route("/dashboard/", methods=['GET'])
def dashboard():
    """Flask function to build /dashboard using @app.route decorator

    Parameters
    ----------
    method : GET
        Recieved the data , deserialize the data and pass to pygal for coverting into bar plots

    Returns
    -------
        Data rendered to the dashboard.html
    """
    df = request.args.getlist('df')
    barChart = pygal.HorizontalBar()
    for i in df:
        res = i.strip('][').split(', ')

        barChart.add(res[0], int(res[1]))
        print(res[0], res[1])

    graph_data = barChart.render_data_uri()
    return render_template("dashboard.html", graph_data=graph_data)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Flask function to build / Home using @app.route decorator

    Parameters
    ----------
    method : GET/POST
       Fetch the data from the screen using the POST methods from the index.html form on the submit action and pass the data to twitter_search module
       The bodules seraches twitter for the text and retrun top 10 topics being discussed for the specifed topics

    Returns
    -------
        Data rendered to the home page
    """
    if request.method == 'POST':
        user = request.form['searchtext']
        usr = twitter_search(search_string = user,item_cnt=1000)
        return redirect(url_for("dashboard",df=usr))
    else:
        return render_template("index.html")