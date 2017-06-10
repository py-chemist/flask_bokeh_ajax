from flask import Flask, render_template, jsonify, request, url_for
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.models import ColumnDataSource
from bokeh.models import CustomJS, Slider, Select
from bokeh.layouts import widgetbox, column
import json

resources = INLINE
js_resources = resources.render_js()
css_resources = resources.render_css()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def home():
    x = [x*0.005 for x in range(0, 200)]
    y = x
    source = ColumnDataSource(data=dict(x=x, y=y))

    plot = figure(plot_width=300, plot_height=250)
    plot.line('x', 'y',  line_width=3, source=source, line_alpha=0.6)

    callback = CustomJS(args=dict(source=source), code="""
        var data = source.data;
        var f = cb_obj.value
        x = data['x']
        y = data['y']
        for (i = 0; i < x.length; i++) {
            y[i] = Math.pow(x[i], f)
        }
        source.trigger('change');
    """)

    slider = Slider(start=0.1, end=4, value=1, step=.1, title="power")
    slider.js_on_change('value', callback)

    layout = column(slider, plot)
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    script, div = components(layout, INLINE)
    return render_template('bokeh.html',
                           plot_script=script,
                           plot_div=div,
                           js_resources=js_resources,
                           css_resources=css_resources)


my_data = {'one': [1, 3, 5],
           'two': [2, 7, 5],
           'three': [8, 3, 6]}


@app.route('/new_option', methods=['POST'])
def new_option():
    json.dumps(request.form)
    option = request.form['value']
    return jsonify(option=my_data[option])


@app.route('/ajax', methods=["GET", "POST"])
def ajax():
    x = [1, 2, 3]
    source = ColumnDataSource(data=dict(x=x, y=my_data['one']))
    plot = figure(height=250, width=300)
    plot.line('x', 'y', source=source, line_width=3, line_alpha=0.8)
    callback = CustomJS(args=dict(source=source), code="""
    var selected_value = cb_obj.value;
    var plot_data = source.data;
    jQuery.ajax({
        type: 'POST',
        url: '/new_option',
        data: {"value": selected_value},
        dataType: 'json',
        success: function (response) {
            plot_data['y'] = response["option"];
            source.trigger('change');
        },
        error: function() {
            alert("An error occured!");
        }
    });
    """)

    select = Select(value='one',
                    options=list(my_data.keys()),
                    callback=callback)

    layout = column(widgetbox(select, width=100), plot)
    script, div = components(layout)
    return jsonify(script=script,
                   div=div,
                   js_resources=INLINE.render_js(),
                   css_resources=INLINE.render_css())


if __name__ == "__main__":
    app.run(debug=True)
