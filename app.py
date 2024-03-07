from flask import Flask, render_template, url_for, after_this_request, jsonify, make_response
import os
import random
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['figure.figsize'] = (14, 10)
import matplotlib.pyplot as plt
import numpy as np
import time
import os
import seaborn as sns
current_directory = os.getcwd()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def poly(x, y, equation):
    term_split = equation.split("+")
    a = int(term_split[0].split("x")[0])
    n = int(term_split[0].split("x")[1][1:])
    b = int(term_split[1].split("y")[0])
    m = int(term_split[1].split("y")[1][1:])
    return a*x**n + b*y**m

@app.route("/plot_3d_contour/<int(signed=True):bound_min>/<int(signed=True):bound_max>/<path:equation>")
def plot_3d_contour(bound_min, bound_max, equation):
    image_file = os.path.join(current_directory, 'static', "plot_3d_contour.png")

    x = np.linspace(bound_min, bound_max, 100)
    y = np.linspace(bound_min, bound_max, 100)
    X, Y = np.meshgrid(x, y)
    Z = poly(X, Y, equation)

    plt.figure()
    ax = plt.axes(projection='3d')
    ax.contour3D(X, Y, Z, 50, cmap='coolwarm')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z');
    ax.view_init(25, 35)
    plt.savefig(image_file)
    plt.close()

    image_url = url_for('static', filename="plot_3d_contour.png")
    return render_template("contour.html", url=image_url)

@app.route("/plot_3d_contour/", defaults={'path': ''})
@app.route('/plot_3d_contour/<path:path>')
def catch_contour(path):
    response = jsonify({'error': 'The URL must follow the pattern /plot_3d_contour/int:min_xy/int:max_xy/Ax^n+By^m'})
    return make_response(response, 404)

@app.route("/plot_3d_surface/<int(signed=True):bound_min>/<int(signed=True):bound_max>/<path:equation>")
def plot_3d_surface(bound_min, bound_max, equation):
    image_file = os.path.join(current_directory, 'static', "plot_3d_surface.png")

    x = np.linspace(bound_min, bound_max, 200)
    y = np.linspace(bound_min, bound_max, 200)
    X, Y = np.meshgrid(x, y)
    Z = poly(X, Y, equation)

    plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z');
    ax.view_init(25, 35)
    plt.savefig(image_file)
    plt.close()

    image_url = url_for('static', filename="plot_3d_surface.png")
    return render_template("surface.html", url=image_url)

@app.route("/plot_3d_surface/", defaults={'path': ''})
@app.route('/plot_3d_surface/<path:path>')
def catch_surface(path):
    response = jsonify({'error': 'The URL must follow the pattern /plot_3d_surface/int:min_xy/int:max_xy/Ax^n+By^m'})
    return make_response(response, 404)

@app.route("/plot_kde/<string:color>/<path:data>")
def plot_kde(color, data):
    image_file = os.path.join(current_directory, 'static', "plot_kde.png")
    color = color.lower()
    data = np.array(data.split(","), dtype=np.int32)
    try:
        sns.kdeplot(data, color=color, fill=True)
    except ValueError as e:
        return make_response(jsonify({'error': 'Invalid Color'}), 404)
    plt.savefig(image_file)
    plt.close()
    image_url = url_for('static', filename="plot_kde.png")
    return render_template("kde.html", url=image_url)

@app.route("/plot_kde/", defaults={'path': ''})
@app.route('/plot_kde/<path:path>')
def catch_kde(path):
    response = jsonify({'error': 'The URL must follow the pattern /plot_kde/string:color/a,b,c,d,e,a,b,e,f,c,etc.'})
    return make_response(response, 404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))