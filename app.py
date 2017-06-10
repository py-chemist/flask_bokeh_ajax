from flask import Flask, render_template, jsonify
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.models import ColumnDataSource
from bokeh.models import CustomJS, Slider, Select
from bokeh.layouts import widgetbox, column

resources = INLINE
js_resources = resources.render_js()
css_resources = resources.render_css()

app = Flask(__name__)


@app.route('/')
def home():
    x = [x*0.005 for x in range(0, 200)]
    y = x
    source = ColumnDataSource(data=dict(x=x, y=y))

    plot = figure(plot_width=400, plot_height=300)
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


if __name__ == "__main__":
    app.run(debug=True)
