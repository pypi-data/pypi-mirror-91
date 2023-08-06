from builtins import super, bytes

import ctypes

from six import string_types

from ..tecutil import _tecutil
from ..constant import *
from ..exception import *
from .. import macro, session, tecutil
from ..tecutil import Index, lock, lock_attributes, sv
from .grid import (GridLines, GridLines2D, MarkerGridLine, MarkerGridLine2D,
                   MinorGridLines, MinorGridLines2D, PolarAngleGridLines,
                   PolarAngleMarkerGridLine, PolarAngleMinorGridLines)
from .ticks import (RadialTicks, RadialTickLabels, TickLabels2D, TickLabels3D,
                    Ticks2D, Ticks3D)
from .title import (Axis2DTitle, DataAxis2DTitle, DataAxis3DTitle,
                    RadialAxisTitle)


class Axis(session.Style):
    def __init__(self, axes, name, **kwargs):
        self.axes = axes
        self.name, self._sv_name, self._sv_detail = Axis._sv_axis_detail(name)
        kw = axes._kw
        kw.update(**kwargs)
        super().__init__(axes._sv, self._sv_detail, **kw)

    @staticmethod
    def _sv_axis_detail(name):
        if isinstance(name, string_types):
            name = name.upper()
            svname = getattr(sv, name)
            svdetail = getattr(sv, name+'DETAIL')
        else:
            _tr = {sv.X: 'X', sv.Y: 'Y', sv.Z: 'Z', sv.R: 'R',
                   sv.THETA: 'THETA'}
            _tr_detail = {sv.X: sv.XDETAIL, sv.Y: sv.YDETAIL, sv.Z: sv.ZDETAIL,
                          sv.R: sv.RDETAIL, sv.THETA: sv.THETADETAIL}
            svdetail = _tr_detail[name]
            svname = name
            name = _tr[svname]
        return name, svname, svdetail

    def __eq__(self, that):
        return (isinstance(that, type(self)) and self.name == that.name and
                self.axes == that.axes)

    def __ne__(self, that):
        return not (self == that)

    @lock()
    def _view(self, action, consider_blanking=None):
        """Internal implementation for all view actions which take a single
        consider blanking parameter."""
        with self.axes.plot.frame.activated():
            with tecutil.ArgList() as arg_list:
                arg_list[sv.VIEWOP] = action
                arg_list[sv.AXIS] = ord(self.name[0])
                arg_list[sv.AXISNUM] = getattr(self, 'index', 0) + 1
                if consider_blanking:
                    arg_list[sv.CONSIDERBLANKING] = True
                if not _tecutil.ViewX(arg_list):
                    raise TecplotSystemError()

    @property
    def show(self):
        """`bool`: Enable drawing of this axis.

        Example usage::

            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.show = True
        """
        return self._get_style(bool, sv.SHOWAXIS)

    @show.setter
    def show(self, show):
        self._set_style(bool(show), sv.SHOWAXIS)

    @property
    def min(self):
        """`float`: Lower bound of this axis' range.

        Example usage::

            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.min = 0.0
        """
        return self._get_style(float, sv.RANGEMIN)

    @min.setter
    def min(self, value):
        # This is a work around for handling an uninitialized range
        # for the sketch axes. We set both min and max using a
        # macro which allows us to set the min and max individually.
        # Also, it prevents the range from being reset as the result
        # of uninitialized conditions in the engine with dynamically
        # created axis variables. (See TargetProcess request: 106803)
        fmt = '$!{} {}Detail {{ RangeMin = {} RangeMax = {} }}'
        cmd = fmt.format(self._sv[0], self.name, float(value), self.max)
        macro.execute_command(cmd)
        self._set_style(float(value), sv.RANGEMIN)

    @property
    def max(self):
        """`float`: Upper bound of this axis' range.

        Example usage::

            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.max = 1.0
        """
        return self._get_style(float, sv.RANGEMAX)

    @max.setter
    def max(self, value):
        # This is a work around for handling an uninitialized range
        # for the sketch axes. We set both min and max using a
        # macro which allows us to set the min and max individually.
        # Also, it prevents the range from being reset as the result
        # of uninitialized conditions in the engine with dynamically
        # created axis variables. (See TargetProcess request: 106803)
        fmt = '$!{} {}Detail {{ RangeMin = {} RangeMax = {} }}'
        cmd = fmt.format(self._sv[0], self.name, self.min, float(value))
        macro.execute_command(cmd)
        self._set_style(float(value), sv.RANGEMAX)

    @property
    def ticks(self):
        """`Ticks2D`: Axis major and minor ticks style control.

        Example usage::

            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.ticks.line_thickness = 0.8
        """
        return Ticks2D(self)

    @property
    def tick_labels(self):
        """`TickLabels2D`: Axis ticks labels style control.

        Example usage::

            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.tick_labels.show = False
        """
        return TickLabels2D(self)

    @property
    def grid_lines(self):
        """`GridLines2D`: Major grid lines style control.

        Major grid lines are attached to the locations of the major ticks. See
        `minor_grid_lines <XYLineAxis.minor_grid_lines>` for lines attached to
        minor ticks. Example usage::

            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.grid_lines.show = True
        """
        return GridLines2D(self)

    @property
    def minor_grid_lines(self):
        """`MinorGridLines2D`: Minor grid lines style control.

        Minor grid lines are attached to the locations of the minor ticks.
        Example usage::

            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.minor_grid_lines.show = True
        """
        return MinorGridLines2D(self)

    @property
    def title(self):
        """`str`: Axis title.

        This is the primary label for the axis and usually includes units::

            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.title.text = 'distance (m)'
        """
        return Axis2DTitle(self)

    @property
    def line(self):
        """`Cartesian2DAxisLine`: Axis line style control.

        Example usage::

            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.line.line_thickness = 0.6
        """
        return Cartesian2DAxisLine(self)

    @lock()
    def adjust_range_to_nice(self):
        """Rounds the axis range to the nearest major axis increment.

        This method resets the axis-line label values such that all
        currently displayed label values are set to have the smallest number
        of significant digits possible.

        Example usage::

            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.adjust_range_to_nice()
        """
        self._view(View.AxisMakeCurrentValuesNice)

    @property
    def marker_grid_line(self):
        """`MarkerGridLine2D`: Marker line to indicate a particular position along an axis.

        Example usage::

            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.marker_grid_line.show = True
            >>> axis.marker_grid_line.position = 0.5
        """
        return MarkerGridLine2D(self)

    def fit_range(self):
        """Set range of axis to variable minimum and maximum.

        .. note:: If the axis dependency is not `Independent`, then this action
            may also affect the range on another axis.

        Example usage::

            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.fit_range()
        """
        self._view(View.AxisFit)

    def fit_range_to_nice(self):
        """Set range of axis to nice values near variable minimum and maximum.

        This method resets the range to equal the minimum and maximum of the
        data being plotted, but makes the axis values "nice" by setting labels
        to have the smallest number of significant digits possible,

        .. note:: If the axis dependency is not independent then this method
            may also affect the range on another axis.

        Example usage::

            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.fit_range_to_nice()
        """
        self._view(View.AxisNiceFit)


class ReversibleAxis(Axis):
    @property
    def reverse(self):
        """`bool`: Reverse the direction of the axis scale.

        Example usage::

            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.reverse = True
        """
        return self._get_style(bool, sv.ISREVERSED)

    @reverse.setter
    def reverse(self, value):
        self._set_style(bool(value), sv.ISREVERSED)


class Cartesian2DAxis(Axis):
    @property
    def log_scale(self):
        """`bool`: Use logarithmic scale for this axis.

        Example usage::

            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> # or "plot.axes.r_axis" for the radial axis in polar plots
            >>> axis.log_scale = True
        """
        return self._get_style(CoordScale, sv.COORDSCALE) is CoordScale.Log

    @log_scale.setter
    def log_scale(self, value):
        cscale = CoordScale.Log if value else CoordScale.Linear
        self._set_style(cscale, sv.COORDSCALE)


class DataAxis(Axis):
    @property
    def title(self):
        """`str`: Axis title.

        This is the primary label for the axis and usually includes units::

            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.title.text = 'distance (m)'
        """
        return DataAxis2DTitle(self)


class FieldAxis(DataAxis):
    def fit_range(self, consider_blanking=True):
        """Set range of axis to variable minimum and maximum.

        .. note:: If the axis dependency is not `Independent`, then this action
            may also affect the range on another axis.

        Parameters:
            consider_blanking (`Boolean <bool>`, optional): If `True` and
                blanking is enabled, the resulting view excludes blanked cells
                at the edges of the plot. If `False`, then
                the resulting view will ignore blanked cells at the edges of the
                plot. (default: `True`)

        Example usage::

            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.fit_range()
        """
        self._view(View.AxisFit, consider_blanking)

    def fit_range_to_nice(self, consider_blanking=True):
        """Set range of axis to nice values near variable minimum and maximum.

        This method resets the range to equal the minimum and maximum of the
        data being plotted, but makes the axis values "nice" by setting labels
        to have the smallest number of significant digits possible,

        .. note:: If the axis dependency is not independent then this method
            may also affect the range on another axis.

        Parameters:
            consider_blanking (`Boolean <bool>`, optional): If `True` and
                blanking is enabled, the resulting view excludes blanked cells
                at the edges of the plot. If `False`, then
                the resulting view will ignore blanked cells at the edges of the
                plot. (default: `True`)

        Example usage::

            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.fit_range_to_nice()
        """
        self._view(View.AxisNiceFit, consider_blanking)

    @property
    def variable(self):
        """`Variable`: The `Variable` assigned to this axis.

        This is the spatial variable associated with this axis
        and is usually one of ``(X, Y, Z)``. Example usage:

        .. code-block:: python

            import tecplot as tp
            from tecplot.constant import PlotType

            fr = tp.active_frame()
            ds = fr.create_dataset('D', ['X', 'Y', 'Z', 'U', 'V'])
            axes = fr.plot(PlotType.Cartesian3D).axes

            # prints: ('X', 'Y')
            print(axes.x_axis.variable.name, axes.y_axis.variable.name)

            axes.x_axis.variable = ds.variable('U')
            axes.y_axis.variable = ds.variable('V')

            # prints: ('U', 'V)
            print(axes.x_axis.variable.name, axes.y_axis.variable.name)
        """
        ds = self.axes.plot.frame.dataset
        return ds.variable(self.variable_index)

    @variable.setter
    def variable(self, v):
        self.variable_index = v.index

    @property
    def variable_index(self):
        """`Index` (zero-based): Index of the `Variable` assigned to this axis.

        Example usage, interchanging the (x, y) axes::

            >>> v0 = plot.axes.x_axis.variable_index
            >>> v1 = plot.axes.y_axis.variable_index
            >>> plot.axes.x_axis.variable_index = v1
            >>> plot.axes.y_axis.variable_index = v0
        """
        return self._get_style(Index, sv.VARNUM)

    @variable_index.setter
    def variable_index(self, i):
        self._set_style(Index(i), sv.VARNUM)


class IndexedLineAxis(DataAxis, Cartesian2DAxis, ReversibleAxis):
    def __init__(self, axes, name, index):
        self.index = Index(index)
        super().__init__(axes, name, offset1=self.index)

    def __eq__(self, that):
        return (isinstance(that, type(self)) and self.index == that.index and
                self.name == that.name and self.axes == that.axes)

    def __ne__(self, that):
        return not (self == that)


class PolarLineAxis(DataAxis, ReversibleAxis):
    @property
    def line(self):
        """`AxisLine2D`: Axis line style control.

        Example usage::

            >>> plot.axes.r_axis.line.line_thickness = 0.6
            >>> plot.axes.theta_axis.line.line_thickness = 0.6
        """
        return AxisLine2D(self)

    @property
    def origin(self):
        """`float`: Value at the origin of the axis.

        Example usage::

            # value at center of plot equal to 10
            >>> plot.axes.r_axis.origin = 10
            # rotate theta axis 45 degrees clockwise
            >>> plot.axes.theta_axis.origin = 45
        """
        return self._get_style(float, sv.VALUEATORIGIN)

    @origin.setter
    def origin(self, value):
        self._set_style(float(value), sv.VALUEATORIGIN)

    @property
    def clip_data(self):
        """`bool`: Do not show data outside the axes area.

        Example usage::

            >>> plot.axes.clip_data = True
        """
        return self._get_style(bool, sv.CLIPDATA)

    @clip_data.setter
    def clip_data(self, value):
        self._set_style(bool(value), sv.CLIPDATA)


class Cartesian2DFieldAxis(FieldAxis, Cartesian2DAxis, ReversibleAxis):
    """X or Y axis for 2D field plots.

    .. code-block:: python
        :emphasize-lines: 18-33

        from os import path
        import tecplot as tp
        from tecplot.constant import PlotType, AxisMode, AxisTitleMode

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'HeatExchanger.plt')
        dataset = tp.data.load_tecplot(infile)

        frame = tp.active_frame()
        plot = frame.plot(PlotType.Cartesian2D)

        plot.show_contour = True

        plot.axes.axis_mode = AxisMode.Independent
        plot.axes.viewport.right = 75
        plot.axes.preserve_scale = False

        xaxis = plot.axes.x_axis
        xaxis.title.text = 'Longitudinal (m)'
        xaxis.title.title_mode = AxisTitleMode.UseText
        xaxis.min = 3.8
        xaxis.max = 5.3
        xaxis.grid_lines.show = True
        xaxis.grid_lines.draw_last = True

        yaxis = plot.axes.y_axis
        yaxis.title.text = 'Transverse (m)'
        yaxis.title.title_mode = AxisTitleMode.UseText
        yaxis.min = 2.8
        yaxis.max = 4.3
        yaxis.grid_lines.show = True
        yaxis.minor_grid_lines.show = True
        yaxis.minor_grid_lines.draw_last = True

        # ensure consistent output between interactive (connected) and batch
        plot.contour(0).levels.reset_to_nice()

        tp.export.save_png('axis_2d.png',600, supersample=3)

    ..  figure:: /_static/images/axis_2d.png
        :width: 300px
        :figwidth: 300px
    """


class Cartesian3DFieldAxis(FieldAxis):
    """X, Y or Z axis on 3D field plots.

    .. code-block:: python
        :emphasize-lines: 18,24-36

        from os import path
        import tecplot as tp
        from tecplot.constant import PlotType, Color, AxisLine3DAssignment

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'RainierElevation.lay')
        tp.load_layout(infile)

        frame = tp.active_frame()
        dataset = frame.dataset
        plot = frame.plot(PlotType.Cartesian3D)
        plot.activate()

        plot.show_contour = True

        plot.axes.grid_area.filled = False

        axes = [plot.axes.x_axis, plot.axes.y_axis, plot.axes.z_axis]
        assignments = [AxisLine3DAssignment.YMinZMax,
                       AxisLine3DAssignment.ZMaxXMin,
                       AxisLine3DAssignment.XMaxYMin]

        for ax, asgn in zip(axes, assignments):
            ax.show = True
            ax.grid_lines.show = False
            ax.title.show = False
            ax.line.show = False
            ax.line.edge_assignment = asgn

        plot.axes.z_axis.grid_lines.show = True
        plot.axes.y_axis.min=-2000
        plot.axes.y_axis.max=1000
        plot.axes.x_axis.min=-9500
        plot.axes.x_axis.max=-7200
        plot.axes.z_axis.min=0
        plot.axes.x_axis.scale_factor=1.9

        plot.view.width = 7830
        plot.view.alpha = 0
        plot.view.theta = -147.5
        plot.view.psi   = 70
        plot.view.position = (1975, 15620, 115930)

        tp.export.save_png('axis_3d.png', 600, supersample=3)

    ..  figure:: /_static/images/axis_3d.png
        :width: 300px
        :figwidth: 300px
    """

    @property
    def title(self):
        """`str`: Axis title.

        This is the primary label for the axis and usually includes units::

            >>> plot.axes.x_axis.title.text = 'distance (m)'
        """
        return DataAxis3DTitle(self)

    @property
    def line(self):
        """`AxisLine3D`: Axis line style control.

        Example usage::

            >>> plot.axes.x_axis.line.line_thickness = 0.6
        """
        return AxisLine3D(self)

    @property
    def ticks(self):
        """`Ticks3D`: Axis major and minor ticks style control.

        Example usage::

            >>> plot.axes.x_axis.ticks.line_thickness = 0.8
        """
        return Ticks3D(self)

    @property
    def tick_labels(self):
        """`TickLabels3D`: Axis ticks labels style control.

        Example usage::

            >>> plot.axes.x_axis.tick_labels.show = False
        """
        return TickLabels3D(self)

    @property
    def scale_factor(self):
        """`float`: Factor used for axis scaling.

        This will automatically scale the other axes if axis mode dependent. Setting the axis mode to independent allows each axis to have their own scale factor::

            >>> from tecplot.constant import AxisMode
            >>> plot.axes.axis_mode = AxisMode.Independent
            >>> plot.axes.x_axis.scale_factor = 1
            >>> plot.axes.y_axis.scale_factor = 2
            >>> plot.axes.z_axis.scale_factor = 3
        """
        style = session.Style(sv.GLOBALTHREED, sv.AXISSCALEFACT, **self._kw)
        return style._get_style(float, self._sv_name)

    @scale_factor.setter
    def scale_factor(self, value):
        style = session.Style(sv.GLOBALTHREED, sv.AXISSCALEFACT, **self._kw)
        style._set_style(float(value), self._sv_name)

    @property
    def grid_lines(self):
        """`GridLines`: Major grid lines style control.

        Major grid lines are attached to the locations of the major ticks. See
        `minor_grid_lines <Cartesian3DFieldAxis.minor_grid_lines>` for lines
        attached to minor ticks. Example usage::

            >>> plot.axes.x_axis.grid_lines.show = True
        """
        return GridLines(self)

    @property
    def minor_grid_lines(self):
        """`MinorGridLines`: Minor grid lines style control.

        Minor grid lines are attached to the locations of the minor ticks.
        Example usage::

            >>> plot.axes.x_axis.minor_grid_lines.show = True
        """
        return MinorGridLines(self)

    @property
    def marker_grid_line(self):
        """`MarkerGridLine`: Marker line to indicate a particular position along an axis.

        Example usage::

            >>> plot.axes.x_axis.marker_grid_line.show = True
            >>> plot.axes.x_axis.marker_grid_line.position = 0.5
        """
        return MarkerGridLine(self)


class PolarAngleLineAxis(PolarLineAxis):
    """Theta axis for polar plots.

    This example manipulates both the theta and radial axes to produce a star
    plot. Custom labels are created for each data point:

    .. code-block:: python

        import numpy as np
        import tecplot as tp
        from tecplot.constant import PlotType, ThetaMode, NumberFormat, AxisAlignment

        np.random.seed(2)
        npoints = 7
        theta = np.linspace(0, npoints, npoints+1)

        frame = tp.active_frame()
        dataset = frame.create_dataset('Data', ['Magnitude', 'Property'])

        for i in range(3):
            r = list(np.random.uniform(0.01, 0.99, npoints))
            r.append(r[0])
            zone = dataset.add_ordered_zone('Zone {}'.format(i), (npoints+1,))
            zone.values('Magnitude')[:] = r
            zone.values('Property')[:] = theta

        plot = frame.plot(PlotType.PolarLine)
        plot.activate()
        plot.delete_linemaps()

        for i, zone in enumerate(dataset.zones()):
            lmap = plot.add_linemap('Linemap {}'.format(i), zone,
                                    dataset.variable('Magnitude'),
                                    dataset.variable('Property'))
            lmap.line.line_thickness = 0.8

        r_axis = plot.axes.r_axis
        r_axis.max = 1
        r_axis.line.show = False
        r_axis.title.position = 85
        r_axis.line.alignment = AxisAlignment.WithOpposingAxisValue
        r_axis.line.opposing_axis_value = 1

        theta_axis = plot.axes.theta_axis
        theta_axis.origin = 1
        theta_axis.mode = ThetaMode.Arbitrary
        theta_axis.min = 0
        theta_axis.max = theta.max()
        theta_axis.period = npoints
        theta_axis.ticks.auto_spacing = False
        theta_axis.ticks.spacing = 1
        theta_axis.ticks.minor_num_ticks = 0
        theta_axis.title.show = False

        theta_labels = theta_axis.tick_labels.format
        theta_labels.format_type = NumberFormat.CustomLabel
        theta_labels.add_custom_labels('A', 'B', 'C', 'D', 'E', 'F', 'G')
        theta_labels.custom_labels_index = 0

        plot.view.fit()

        tp.export.save_png('star_plot.png', 600, supersample=3)

    ..  figure:: /_static/images/star_plot.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, axes):
        super().__init__(axes, sv.THETA)

    @property
    def grid_lines(self):
        """`PolarAngleGridLines`: Theta angle major grid lines.

        Example usage::

            >>> plot.axes.theta_axis.grid_lines.show = True
        """
        return PolarAngleGridLines(self)

    @property
    def minor_grid_lines(self):
        """`PolarAngleMinorGridLines`: Theta angle minor grid lines.

        Example usage::

            >>> plot.axes.theta_axis.minor_grid_lines.show = True
        """
        return PolarAngleMinorGridLines(self)

    @property
    def marker_grid_line(self):
        """`PolarAngleMarkerGridLine`: Theta angle marker grid line.

        Example usage::

            >>> plot.axes.theta_axis.marker_grid_line.show = True
        """
        return PolarAngleMarkerGridLine(self)

    @property
    def mode(self):
        """`ThetaMode`: Units or scale used for the theta axis.

        Possible values: `ThetaMode.Degrees`, `ThetaMode.Radians`,
        `ThetaMode.Arbitrary`.

        Example usage::

            >>> from tecplot.constant import ThetaMode
            >>> plot.axes.theta_axis.mode = ThetaMode.Radians
        """
        return self.axes._get_style(ThetaMode, sv.THETAMODE)

    @mode.setter
    def mode(self, value):
        self.axes._set_style(ThetaMode(value), sv.THETAMODE)

    @property
    def period(self):
        """`float`: Number of (min, max) cycles to include in 360 degrees.

        Example usage::

            >>> plot.axes.theta_axis.period = 2
        """
        return self.axes._get_style(float, sv.THETAPERIOD)

    @period.setter
    def period(self, value):
        self.axes._set_style(float(value), sv.THETAPERIOD)

    @lock()
    def set_range_to_entire_circle(self):
        """Set theta range to entire circle.

        Example usage::

            >>> plot.axes.theta_axis.set_range_to_entire_circle()
        """
        self._view(View.AxisResetToEntireCircle)


class RadialLineAxis(PolarLineAxis, Cartesian2DAxis):
    """The R axis for polar plots

    See the example shown for the `theta axis <PolarAngleLineAxis>`.
    """
    def __init__(self, axes):
        super().__init__(axes, sv.R)

    @property
    def title(self):
        """`str`: Axis title.

        This is the primary label for the axis and usually includes units::

            >>> plot.axes.r_axis.title.text = 'distance (m)'
        """
        return RadialAxisTitle(self)

    @property
    def line(self):
        """`RadialAxisLine2D`: Radial axis line style control.

        Example usage::

            >>> plot.axes.r_axis.line.line_thickness = 0.6
        """
        return RadialAxisLine2D(self)

    @property
    def ticks(self):
        """`RadialTicks`: Axis major and minor ticks style control.

        Example usage::

            >>> plot.axes.r_axis.ticks.line_thickness = 0.8
        """
        return RadialTicks(self)

    @property
    def tick_labels(self):
        """`RadialTickLabels`: Axis ticks labels style control.

        Example usage::

            >>> plot.axes.r_axis.tick_labels.show = False
        """
        return RadialTickLabels(self)


class SketchAxis(Cartesian2DAxis):
    """X or Y axis for sketch plots.

    .. code-block:: python
        :emphasize-lines: 11-18

        import tecplot as tp
        from tecplot.constant import PlotType

        plot = tp.active_frame().plot(PlotType.Sketch)

        viewport = plot.axes.viewport
        viewport.left = 10
        viewport.right = 90
        viewport.bottom = 10

        xaxis = plot.axes.x_axis
        xaxis.show = True
        xaxis.min = 0
        xaxis.max = 360
        xaxis.title.text = 'Angle (Degrees)'

        xaxis.ticks.auto_spacing = False
        xaxis.ticks.spacing = 60

        tp.export.save_png('axis_sketch.png', 600, supersample=3)

    ..  figure:: /_static/images/axis_sketch.png
        :width: 300px
        :figwidth: 300px
    """


class XYLineAxis(IndexedLineAxis):
    """X or Y axis for line plots.

    .. code-block:: python
        :emphasize-lines: 18-22,24-25,27-28

        from os import path
        import tecplot as tp
        from tecplot.constant import PlotType

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'Rainfall.dat')
        dataset = tp.data.load_tecplot(infile)

        plot = tp.active_frame().plot(PlotType.XYLine)
        plot.activate()

        for i in range(2):
            lmap = plot.linemap(i)
            lmap.show = True
            lmap.line.line_thickness = 0.6
            lmap.y_axis_index = i

            yax = plot.axes.y_axis(i)
            yax.line.color = lmap.line.color
            yax.title.color = lmap.line.color
            yax.tick_labels.color = lmap.line.color
            yax.line.line_thickness = 0.6
            if i == 0:
                yax.grid_lines.show = True
                yax.grid_lines.color = lmap.line.color
            elif i == 1:
                yax.minor_grid_lines.show = True
                yax.minor_grid_lines.color = lmap.line.color

        tp.export.save_png('axis_line.png', 600, supersample=3)

    ..  figure:: /_static/images/axis_line.png
        :width: 300px
        :figwidth: 300px
    """


class AxisLine(session.Style):
    def __init__(self, axis):
        self.axis = axis
        super().__init__(axis._sv, sv.AXISLINE, **axis._kw)

    @property
    def show(self):
        """`bool`: Draw the primary axis line on the plot.

        Example usage::

            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.line.show = False
        """
        return self._get_style(bool, sv.SHOW)

    @show.setter
    def show(self, show):
        self._set_style(bool(show), sv.SHOW)

    @property
    def color(self):
        """`Color`: Color of the axis line.

        Example usage::

            >>> from tecplot.constant import Color
            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.line.color = Color.Blue
        """
        return self._get_style(Color, sv.COLOR)

    @color.setter
    def color(self, value):
        self._set_style(Color(value), sv.COLOR)

    @property
    def line_thickness(self):
        """`float`: Width of the axis line to be drawn.

        Example usage::

            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.line.line_thickness = 0.5
        """
        return self._get_style(float, sv.LINETHICKNESS)

    @line_thickness.setter
    def line_thickness(self, value):
        self._set_style(float(value), sv.LINETHICKNESS)


class AxisLine2D(AxisLine):
    """Graduated axis line for 2D plots.

    Cartesian *(x, y)* plots use an extension of this class
    (`Cartesian2DAxisLine`). Polar plots use this class directly:

    .. code-block:: python

        import numpy as np
        import tecplot as tp
        from tecplot.constant import PlotType, ThetaMode

        npoints = 300
        r = np.linspace(0, 2000, npoints)
        theta = np.linspace(0, 10, npoints)

        frame = tp.active_frame()
        dataset = frame.create_dataset('Data', ['R', 'Theta'])
        zone = dataset.add_ordered_zone('Zone', (300,))
        zone.values('R')[:] = r
        zone.values('Theta')[:] = theta
        plot = frame.plot(PlotType.PolarLine)
        plot.activate()

        plot.delete_linemaps()
        lmap = plot.add_linemap('Linemap', zone, dataset.variable('R'),
                                dataset.variable('Theta'))
        lmap.line.line_thickness = 0.8

        r_axis = plot.axes.r_axis
        r_axis.max = np.max(r)
        r_axis.tick_labels.angle = 45
        r_axis.tick_labels.font.size *= 2

        theta_axis = plot.axes.theta_axis
        theta_axis.mode = ThetaMode.Radians
        theta_axis.tick_labels.font.size *= 2

        plot.view.fit()

        tp.export.save_png('axis_line_2d.png', 600, supersample=3)

    ..  figure:: /_static/images/axis_line_2d.png
        :width: 300px
        :figwidth: 300px
    """

    @property
    def offset(self):
        """`float` (percent of frame height): Axis line placement with respect to the grid border.

        This is the offset from the grid border-aligned position dictated by
        properties such as `AxisLine2D.alignment`. The example moves the axis
        line into the plot by 5% of the frame height::

            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.line.offset = -5
        """
        return self._get_style(float, sv.OFFSET)

    @offset.setter
    def offset(self, value):
        self._set_style(float(value), sv.OFFSET)

    @property
    def opposing_axis_value(self):
        """`float`: Axis line placement with respect to the opposing axis.

        The axis alignment must be set to `AxisAlignment.WithOpposingAxisValue`
        to make this property relevant::

            >>> from tecplot.constant import AxisAlignment
            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.line.alignment = AxisAlignment.WithOpposingAxisValue
            >>> axis.line.opposing_axis_value = 0.5
        """
        return self._get_style(float, sv.OPPOSINGAXISVALUE)

    @opposing_axis_value.setter
    def opposing_axis_value(self, value):
        self._set_style(float(value), sv.OPPOSINGAXISVALUE)

    @property
    def alignment(self):
        """`AxisAlignment`: Axis line placement.

        Possible values: `WithViewport`, `WithOpposingAxisValue`,
        `WithGridMin`, `WithGridMax`, `WithGridAreaTop`, `WithGridAreaBottom`,
        `WithGridAreaLeft` or `WithGridAreaRight`.

        Not all values will be available for every plot type. Example usage::

            >>> from tecplot.constant import AxisAlignment
            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.line.alignment = AxisAlignment.WithGridMin
        """
        return self._get_style(AxisAlignment, sv.AXISALIGNMENT)

    @alignment.setter
    def alignment(self, value):
        self._set_style(AxisAlignment(value), sv.AXISALIGNMENT)


class Cartesian2DAxisLine(AxisLine2D):
    """Axis line for 2D field plots.

    .. code-block:: python
        :emphasize-lines: 19-22

        from os import path
        import tecplot as tp
        from tecplot.constant import PlotType, Color, AxisAlignment

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'CircularContour.plt')
        dataset = tp.data.load_tecplot(infile)

        plot = tp.active_frame().plot(PlotType.Cartesian2D)
        plot.activate()

        plot.show_contour = True
        plot.contour(0).colormap_name = 'Sequential - Yellow/Green/Blue'

        plot.axes.preserve_scale = True
        plot.axes.x_axis.fit_range()

        for ax in plot.axes:
            line = ax.line
            line.color = Color.DeepRed
            line.alignment = AxisAlignment.WithOpposingAxisValue
            line.opposing_axis_value = 0
            ax.title.position = 85

        plot.contour(0).levels.reset_to_nice()

        tp.export.save_png('axis_line_cartesian2d.png', 600, supersample=3)

    ..  figure:: /_static/images/axis_line_cartesian2d.png
        :width: 300px
        :figwidth: 300px
    """

    @property
    def position(self):
        """`float`: Axis line placement with respect to the viewport.

        The axis alignment must be set to `AxisAlignment.WithViewport`
        to make this property relevant::

            >>> from tecplot.constant import AxisAlignment
            >>> # get axis via "plot.axes.x_axis(0)" for line plots
            >>> # or "plot.axes.x_axis" for field or sketch plots
            >>> axis.line.alignment = AxisAlignment.WithViewport
            >>> axis.line.position = 0.5
        """
        return self._get_style(float, sv.POSITION)

    @position.setter
    def position(self, value):
        self._set_style(float(value), sv.POSITION)


class AxisLine3D(AxisLine):
    """X, Y or Z axis for 3D field plots.

    This represents the line along which ticks and labels are drawn. The color
    affects the line itself and the associated tick marks but not labels or
    axis titles:

    .. code-block:: python

        from os import path
        import tecplot as tp
        from tecplot.constant import PlotType, Color

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'Sphere.lpk')
        dataset = tp.load_layout(infile)

        frame = tp.active_frame()
        plot = frame.plot()

        plot.show_mesh = False
        plot.axes.grid_area.fill_color = Color.Grey

        for ax in [plot.axes.x_axis, plot.axes.y_axis, plot.axes.z_axis]:
            ax.show = True
            ax.grid_lines.show = False
            ax.line.color = Color.Cyan
            ax.line.line_thickness = 0.2
            ax.line.show_on_opposite_edge = True

        plot.view.fit()

        tp.export.save_png('axis_line_3d.png', 600, supersample=3)

    ..  figure:: /_static/images/axis_line_3d.png
        :width: 300px
        :figwidth: 300px
    """

    @property
    def show_on_opposite_edge(self):
        """`bool`: Draw axis line on opposite edge of axes box.

        Example usage::

            >>> plot.axes.x_axis.line.show_on_opposite_edge = True
        """
        return self._get_style(bool, sv.SHOWOPPOSITEEDGE)

    @show_on_opposite_edge.setter
    def show_on_opposite_edge(self, value):
        self._set_style(bool(value), sv.SHOWOPPOSITEEDGE)

    @property
    def edge_assignment(self):
        """`AxisLine3DAssignment` or `None`: Edge to use when drawing the primary axis line.

        Possible values: `AxisLine3DAssignment.Automatic` (aliased to `None`),
        `YMinZMin`, `YMaxZMin`, `YMinZMax`, `YMaxZMax`.

        Example usage::

            >>> from tecplot.constant import AxisLine3DAssignment
            >>> axis.line.edge_assignment = AxisLine3DAssignment.YMinZMin
        """
        style = session.Style(**self._kw)
        auto_reset = style._get_style(bool, sv.THREEDAXIS, sv.EDGEAUTORESET)
        if auto_reset:
            return AxisLine3DAssignment.Automatic
        else:
            return self._get_style(AxisLine3DAssignment, sv.EDGE)

    @edge_assignment.setter
    def edge_assignment(self, value):
        style = session.Style(**self._kw)
        if value in (None, AxisLine3DAssignment.Automatic):
            style._set_style(True, sv.THREEDAXIS, sv.EDGEAUTORESET)
        else:
            style._set_style(False, sv.THREEDAXIS, sv.EDGEAUTORESET)
            self._set_style(AxisLine3DAssignment(value), sv.EDGE)


class RadialAxisLine2D(AxisLine2D):
    """Radial axis line for polar plots.

    .. code-block:: python
        :emphasize-lines: 26-27

        import numpy as np
        import tecplot as tp
        from tecplot.constant import PlotType, Color

        npoints = 300
        r = np.linspace(0, 2000, npoints)
        theta = np.linspace(0, 700, npoints)

        frame = tp.active_frame()
        dataset = frame.create_dataset('Data', ['R', 'Theta'])
        zone = dataset.add_ordered_zone('Zone', (300,))
        zone.values('R')[:] = r
        zone.values('Theta')[:] = theta

        plot = frame.plot(PlotType.PolarLine)
        plot.activate()

        plot.axes.r_axis.max = np.max(r)

        plot.delete_linemaps()
        lmap = plot.add_linemap('Linemap', zone, dataset.variable('R'),
                                dataset.variable('Theta'))
        lmap.line.line_thickness = 0.8

        raxis = plot.axes.r_axis
        raxis.line.show_both_directions = True
        raxis.line.show_perpendicular = True

        plot.view.fit()

        tp.export.save_png('axis_line_radial.png', 600, supersample=3)

    ..  figure:: /_static/images/axis_line_radial.png
        :width: 300px
        :figwidth: 300px
    """

    @property
    def show_both_directions(self):
        """`bool`: Mirror the radial axis 180 degrees from the primary line.

        If `RadialAxisLine2D.show_perpendicular` is `True`, this will mirror
        that axis line as well resulting in four axis lines, 90 degrees apart.
        Example usage::

            >>> r_axis.line.show_both_directions = True
        """
        return self._get_style(bool, sv.SHOWBOTHDIRECTIONS)

    @show_both_directions.setter
    def show_both_directions(self, value):
        self._set_style(bool(value), sv.SHOWBOTHDIRECTIONS)

    @property
    def show_perpendicular(self):
        """`bool`: Mirror the radial axis 90 degrees from the primary line.

        Example usage::

            >>> r_axis.line.show_perpendicular = True
        """
        return self._get_style(bool, sv.SHOWPERPENDICULAR)

    @show_perpendicular.setter
    def show_perpendicular(self, value):
        self._set_style(bool(value), sv.SHOWPERPENDICULAR)

    @property
    def alignment(self):
        """`AxisAlignment`: Axis line placement.

        Possible values: `WithOpposingAxisValue`, `WithGridMin`, `WithGridMax`,
        `WithSpecificAngle`, `WithGridAreaTop`, `WithGridAreaBottom`,
        `WithGridAreaLeft` or `WithGridAreaRight`.

        Not all values will be available for every plot type. Example usage::

            >>> from tecplot.constant import AxisAlignment
            >>> plot.r_axis.line.alignment = AxisAlignment.WithOpposingAxisValue
            >>> plot.r_axis.line.opposing_axis_value = 45
        """
        return self._get_style(AxisAlignment, sv.AXISALIGNMENT)

    @alignment.setter
    def alignment(self, value):
        self._set_style(AxisAlignment(value), sv.AXISALIGNMENT)

    @property
    def angle(self):
        """`float`: Specific angle to place the radial axis line.

        The alignment must be set to `AxisAlignment.WithSpecificAngle`::

            >>> from tecplot.constant import AxisAlignment
            >>> plot.r_axis.line.alignment = AxisAlignment.WithSpecificAngle
            >>> plot.r_axis.line.angle = 45
        """
        return self._get_style(float, sv.ANGLE)

    @angle.setter
    def angle(self, value):
        self._set_style(float(value), sv.ANGLE)
