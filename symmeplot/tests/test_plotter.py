from matplotlib.pyplot import subplots
from sympy.physics.mechanics import Point, ReferenceFrame, dynamicsymbols

from symmeplot import PlotFrame, PlotPoint, PlotVector, SymMePlotter
from symmeplot.tests.utilities import compare_values, mpl3d_image_comparison


@mpl3d_image_comparison(["basic_example.png"])
def test_basic_example():
    N = ReferenceFrame("N")
    A = ReferenceFrame("A")
    q = dynamicsymbols("q")
    A.orient_axis(N, N.z, q)
    N0 = Point("N_0")
    v = 0.2 * N.x + 0.2 * N.y + 0.7 * N.z
    A0 = N0.locatenew("A_0", v)
    fig, ax = subplots(subplot_kw={"projection": "3d"})
    plotter = SymMePlotter(ax, N, N0, scale=0.5)
    plotter.add_vector(v)
    plotter.add_frame(A, A0, ls="--")
    plotter.add_point(A0, color="g")
    plotter.evalf(subs={q: 0.5})
    plotter.plot()
    plotter.lambdify_system((q,))
    for i in range(10, 0, -1):
        qi = 1 / i
        plotter.evalf(subs={q: qi})
        vals = plotter.values
        plotter.evaluate_system(qi)
        compare_values(vals, plotter.values)
    assert isinstance(plotter.get_plot_object(A0), PlotPoint)
    assert plotter.get_plot_object("A_0") == plotter.get_plot_object(A0)
    assert isinstance(plotter.get_plot_object(v), PlotVector)
    assert isinstance(plotter.get_plot_object(A), PlotFrame)
    assert isinstance(plotter.get_plot_object(0.5 * N.x), PlotVector)
