from microdot import Microdot
import numpy as np
# Want to time the execution time
import time
from md_utils import FigManager, encode_figure

app = Microdot()
fig_mgr = FigManager()

@app.route('/')
async def index(request):
    return '''
        <body>
            <div>
                <h1>Testing Homepage</h1>
            </div>
            <div>
                <a href="/fig-render">Click here to go to the figure rendering page</a>
            </div>
        </body>
''', {'Content-Type': 'text/html'}

@app.route('/fig-render')
async def fig_render(request):
    t = start_t = time.time()
    arr_1 = np.arange(20000)
    arr_2 = np.arange(20000) + 1000
    arr_init_time = time.time() - t
    t = time.time()
    fig, ax = fig_mgr()
    ax.plot(arr_1 / arr_2)
    html_img = encode_figure(fig, ax)
    image_render_time = time.time() - t
    t = time.time()
    # Make sure the array is formatted to print nicely
    return f'''<body>
                <div>
                    <h1>Figure Page</h1>
                    <h2>Total execution time was %.3f</h2>
                    <a href="/">Click here to go back to the homepage</a><br /><br />
                    Initialising arrays took {arr_init_time} seconds<br />
                    Rendering image took {image_render_time} seconds<br />
                    Processing HTML took: %.5f seconds
                </div> <br />

                <div>
                    {html_img}
                </div> <br />

                <div>
                    {"<br />".join([np.array2string(row) for row in (arr_1 / arr_2).reshape(-1, 5)])}
                </div>
            </body>''' % (time.time() - start_t, time.time() - t), {'Content-Type': 'text/html'}

app.run(debug=True)