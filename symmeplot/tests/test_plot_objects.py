import pytest
from sympy.physics.mechanics import ReferenceFrame, Point
from sympy import symbols
from symmeplot import PlotPoint, PlotVector, PlotFrame
from symmeplot.tests.utilities import mpl3d_image_comparison
from matplotlib.testing.decorators import check_figures_equal, cleanup
from matplotlib.pyplot import subplots
from symmeplot.tests.utilities import equalize_axis_limits


class TestPlotPoint:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.l = symbols('l:3')
        self.subs_zero = {li: 0 for li in self.l}
        self.subs_test = {self.l[0]: 0.2, self.l[1]: 0.6, self.l[2]: 0.3}
        self.N, self.O = ReferenceFrame('N'), Point('O')
        self.P1 = Point('P1')
        self.P1.set_pos(self.O, (self.l[0] * self.N.x + self.l[1] * self.N.y +
                                 self.l[2] * self.N.z))

    def create_basic_plot_point(self, fig_test):
        ax_test = fig_test.add_subplot(projection='3d')
        P1_plot = PlotPoint(self.N, self.O, self.P1, color='k')
        P1_plot.evalf(subs=self.subs_zero)
        P1_plot.plot(ax_test)
        return ax_test, P1_plot

    @check_figures_equal(extensions=['png'])
    def test_plot_point_basic(self, fig_test, fig_ref):
        ax_ref = fig_ref.add_subplot(projection='3d')
        ax_ref.plot([0], [0], [0], color='k', marker='o')
        ax_test, P1_plot = self.create_basic_plot_point(fig_test)
        equalize_axis_limits(ax_test, ax_ref)

    @check_figures_equal(extensions=['png'])
    def test_plot_point_update(self, fig_test, fig_ref):
        ax_ref = fig_ref.add_subplot(projection='3d')
        ax_ref.plot([0.2], [0.6], [0.3], color='k', marker='o')
        ax_test, P1_plot = self.create_basic_plot_point(fig_test)
        P1_plot.evalf(subs=self.subs_test)
        P1_plot.update()
        equalize_axis_limits(ax_test, ax_ref)


class TestPlotVector:
    @pytest.fixture()
    def setup_values(self):
        self.l = symbols('l:6')
        self.subs1 = {self.l[0]: 1.0, self.l[1]: 0, self.l[2]: 0,
                      self.l[3]: -0.3, self.l[4]: 0.7, self.l[5]: 0.2}
        self.subs2 = {self.l[0]: 0.2, self.l[1]: 0.6, self.l[2]: 0.3,
                      self.l[3]: 0.5, self.l[4]: -0.3, self.l[5]: 0.6}
        self.N, self.O = ReferenceFrame('N'), Point('O')
        self.O_v = self.O.locatenew('O_v', (self.l[0] * self.N.x + self.l[1] *
                                            self.N.y + self.l[2] * self.N.z))
        self.v = (self.l[3] * self.N.x + self.l[4] * self.N.y +
                  self.l[5] * self.N.z)

    @pytest.fixture()
    def setup_basic_arrow(self, setup_values):
        self.fig, self.ax = subplots(subplot_kw={'projection': '3d'})
        self.plot_vector = PlotVector(self.N, self.O, self.v, self.O_v)
        self.plot_vector.evalf(subs=self.subs1)
        self.plot_vector.plot(self.ax)

    @cleanup
    @mpl3d_image_comparison(['plot_vector_basic_arrow.png'])
    def test_plot_vector_basic_arrow(self, setup_basic_arrow):
        pass

    @cleanup
    @mpl3d_image_comparison(['plot_vector_update_arrow.png'])
    def test_plot_vector_update_arrow(self, setup_basic_arrow):
        self.plot_vector.evalf(subs=self.subs2)
        self.plot_vector.update()


class TestPlotFrame:
    @pytest.fixture()
    def setup_values(self):
        self.l, self.q = symbols('l:3'), symbols('q')
        self.subs_zero = {self.l[0]: 0, self.l[1]: 0, self.l[2]: 0, self.q: -1}
        self.subs_move = {self.l[0]: 0.2, self.l[1]: 0.6, self.l[2]: 0.3,
                          self.q: 2.3}
        self.N, self.O = ReferenceFrame('N'), Point('O')
        self.A = ReferenceFrame('A')
        self.A.orient_axis(self.N, self.N.z, self.q)
        self.A_o = self.O.locatenew('A_o', (self.l[0] * self.N.x + self.l[1] *
                                            self.N.y + self.l[2] * self.N.z))

    @pytest.fixture()
    def setup_basic_frame(self, setup_values):
        self.fig, self.ax = subplots(subplot_kw={'projection': '3d'})
        self.N_plot = PlotFrame(self.N, self.O, self.N, self.O)
        self.A_plot = PlotFrame(self.N, self.O, self.A, self.A_o,
                                scale=0.5, ls='--')
        self.N_plot.evalf()
        self.A_plot.evalf(subs=self.subs_zero)
        self.N_plot.plot(self.ax)
        self.A_plot.plot(self.ax)

    @cleanup
    @mpl3d_image_comparison(['plot_frame_basic.png'])
    def test_plot_vector_basic_arrow(self, setup_basic_frame):
        pass

    @cleanup
    @mpl3d_image_comparison(['plot_frame_update.png'])
    def test_plot_vector_update_arrow(self, setup_basic_frame):
        self.A_plot.evalf(subs=self.subs_move)
        self.A_plot.update()
