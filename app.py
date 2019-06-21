import requests
import pandas 
import quandl
import simplejson as json
from bokeh.plotting import figure
from bokeh.palettes import Spectral11
from bokeh.embed import components 
from flask import Flask,render_template,request,redirect,session

app = Flask(__name__)

app.vars={}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/about')
def about():
    return 'The about page'

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/print', methods=['POST'])
def print_input():
    return render_template('print.html',stock=request.form['ticker2'] )
    
@app.route('/plot', methods=['POST'])
def graph():

        app.vars['ticker'] = request.form['ticker']
        
	#quandl.ApiConfig.api_key = "-kWt3pxKqsM8kzTKA-AY"
	
	## Old Way
        api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json?api_key=-kWt3pxKqsM8kzTKA-AY' % app.vars['ticker']
        session = requests.Session()
        session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
        raw_data = session.get(api_url)
        a = raw_data.json()

	## New Way
	#df = quandl.get("WIKI/%s" %app.vars['ticker'], rows=20)
        
        df = pandas.DataFrame(a['data'], columns=a['column_names'])

        df['Date'] = pandas.to_datetime(df['Date'])
        df = df.head(30)
        p = figure(title='The Stock prices for %s over the most recent 30 days' % app.vars['ticker'],
            x_axis_label='date',
            x_axis_type='datetime')
        
        if request.form.get('Close'):
            p.line(x=df['Date'].values, y=df['Close'].values,line_width=2, line_color= "purple",legend='Closing Price')
        #if request.form.get('Adj. Close'):
            #p.circle(x=df['Date'].values, y=df['Adj. Close'].values,line_width=2, line_color="red", legend='Adj. Close')
        #if request.form.get('Open'):
            #p.line(x=df['Date'].values, y=df['Open'].values,line_width=2, line_color="black", legend='Open')
        #if request.form.get('Adj. Open'):
            #p.circle(x=df['Date'].values, y=df['Adj. Open'].values,line_width=2, line_color="brown", legend='Adj. Open')

	
        script, div = components(p)
        return render_template('plot.html', script=script, div=div)


if __name__ == '__main__':
    app.run(port=23456,debug=True)
