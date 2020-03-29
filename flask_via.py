from flask import Flask
from flask import redirect, url_for
import webbrowser
from threading import Timer
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

# @app.route('/hello')
# def hello_world():
# 	return 'Hello, World!'

@app.route('/edit')
def hello_world():
	plt.figure()
	plt.imshow(np.random.rand(10,10))
	plt.show()
	return 'Hello, edit'

@app.route('/')
def home():
	return redirect(url_for('static', filename='via.html'))

def open_via_page(link='http://127.0.0.1:5000'):
	webbrowser.open_new(link)

import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

if __name__ == '__main__':
	Timer(1, open_via_page).start();
	app.run()