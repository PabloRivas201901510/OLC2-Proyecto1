from flask import Flask, redirect, url_for, render_template, request, jsonify
from grammar import parse, getdotTablaSimbolos, generardotErrores, getDot
import base64
import graphviz

app = Flask(__name__)

tmp_val=''


@app.route("/")# de esta forma le indicamos la ruta para acceder a esta pagina. 'Decoramos' la funcion. 
def home():
    return render_template('index.html')

@app.route("/analyze", methods=["POST","GET"])
def analyze():
    if request.method == "POST":
        inpt = request.form["inpt"]
        global tmp_val
        tmp_val=inpt
        return redirect(url_for("output"))
    else:
        f = open("./entrada.txt", "r")
        entrada = f.read()
        return render_template('analyze.html', initial="")

@app.route('/output')
def output():
    global tmp_val
    result = parse(tmp_val)
    global ast
    ast = result
    return render_template('output.html', input=result.getConsola())

@app.route('/reports')
def reports():
    return render_template('reports.html')


@app.route('/reports/symbol-report')
def report_symbol():
    dot = getdotTablaSimbolos(ast)
    dig = graphviz.Source(dot)
    chart_output = dig.pipe(format='svg')
    chart_output = base64.b64encode(chart_output).decode('utf-8')
    return render_template('reports.html', chart=chart_output)

@app.route('/reports/error-report')
def report_error():
    dot = generardotErrores()
    dig = graphviz.Source(dot)
    chart_output = dig.pipe(format='svg')
    chart_output = base64.b64encode(chart_output).decode('utf-8')
    return render_template('reports.html', chart=chart_output)

@app.route('/reports/tree-report')
def report_tree():
    dot = getDot()
    dig = graphviz.Source(dot)
    chart_output = dig.pipe(format='svg')
    chart_output = base64.b64encode(chart_output).decode('utf-8')
    return render_template('reports.html', chart=chart_output)







if __name__ == "__main__":
    app.run(debug=True, port = 3000, host = 'localhost')#para que se actualice al detectar cambios


