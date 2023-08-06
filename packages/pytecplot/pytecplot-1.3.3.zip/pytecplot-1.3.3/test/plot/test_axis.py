import numpy as np
import os
import random
import sys
import tempfile
import unittest

from os import path
from unittest.mock import patch, Mock

from test import patch_tecutil, skip_if_sdk_version_before

import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *
from tecplot.plot import *
from tecplot.tecutil import sv, _tecutil, _tecutil_connector

from ..sample_data import sample_data


class TestAxis(object):
    def test__sv_axis_detail(self):
        name, svname, svdetail = tp.plot.axis.Axis._sv_axis_detail('X')
        self.assertEqual(name, 'X')
        self.assertEqual(svname, sv.X)
        self.assertEqual(svdetail, sv.XDETAIL)
        saved = sv.X
        sv.X = 1
        try:
            name, svname, svdetail = tp.plot.axis.Axis._sv_axis_detail(sv.X)
            self.assertEqual(name, 'X')
            self.assertEqual(svname, sv.X)
            self.assertEqual(svdetail, sv.XDETAIL)
        finally:
            sv.X = saved

    def test_show(self):
        for axis in self.axes:
            for val in [True,False,True]:
                axis.show = val
                self.assertEqual(axis.show, val)
    def test_eq(self):
        self.assertTrue(self.axes[0] == tp.active_frame().plot().axes.x_axis)
        self.assertFalse(self.axes[0] == self.axes[1])
        self.assertFalse(self.axes[0] != tp.active_frame().plot().axes.x_axis)
        self.assertTrue(self.axes[0] != self.axes[1])

    def test_subclasses(self):
        for axis in self.axes:
            self.assertIsInstance(axis, SketchAxis)
            self.assertIsInstance(axis.ticks, Ticks2D)
            self.assertIsInstance(axis.tick_labels, TickLabels2D)
            self.assertIsInstance(axis.grid_lines, GridLines2D)
            self.assertIsInstance(axis.minor_grid_lines, MinorGridLines2D)
            self.assertIsInstance(axis.marker_grid_line, MarkerGridLine2D)
            self.assertIsInstance(axis.title, Axis2DTitle)
            self.assertIsInstance(axis.line, Cartesian2DAxisLine)

    def test_fit_range(self):
        for axis in self.axes:
            axis.fit_range_to_nice()
            axis.fit_range()
            axis.adjust_range_to_nice()

            with patch_tecutil('ViewX', return_value=False):
                with self.assertRaises(TecplotSystemError):
                    axis.fit_range()
            with patch_tecutil('ViewX', return_value=False):
                with self.assertRaises(TecplotSystemError):
                    axis.fit_range_to_nice()
            with patch_tecutil('ViewX', return_value=False):
                with self.assertRaises(TecplotSystemError):
                    axis.adjust_range_to_nice()

            axis.fit_range()
            a, b = axis.min, axis.max
            axis.min = a - 10
            axis.max = b + 15
            axis.fit_range()
            self.assertAlmostEqual(axis.min, a, delta=0.5)
            self.assertAlmostEqual(axis.max, b, delta=0.5)

            axis.fit_range_to_nice()
            a, b = axis.min, axis.max
            axis.min = a - 10
            axis.max = b + 15
            axis.fit_range_to_nice()
            self.assertAlmostEqual(axis.min, a, delta=0.5)
            self.assertAlmostEqual(axis.max, b, delta=0.5)

            axis.fit_range()
            axis.adjust_range_to_nice()
            a, b = axis.min, axis.max
            axis.min = a - 10
            axis.max = b + 15
            axis.fit_range()
            axis.adjust_range_to_nice()
            self.assertAlmostEqual(axis.min, a, delta=0.5)
            self.assertAlmostEqual(axis.max, b, delta=0.5)
            axis.adjust_range_to_nice()
            self.assertAlmostEqual(axis.min, a, delta=0.5)
            self.assertAlmostEqual(axis.max, b, delta=0.5)

    def test_minmax(self):
        for axis in self.axes:
            axis.min = -1000
            self.assertAlmostEqual(axis.min, -1000)
            axis.max = 1000
            self.assertAlmostEqual(axis.max, 1000)

            axis.min = 0
            self.assertAlmostEqual(axis.min, 0)
            axis.max = 1
            self.assertAlmostEqual(axis.max, 1)

            with self.assertRaises((ValueError, TypeError, TecplotSystemError)):
                axis.min = 'badvalue'
            with self.assertRaises((ValueError, TypeError, TecplotSystemError)):
                axis.max = 'badvalue'

    def test_minmax_outside_range(self):
        for axis in self.axes:
            axis.min = -10
            axis.max = 10
            self.assertAlmostEqual(axis.min, -10)
            self.assertAlmostEqual(axis.max, 10)

            axis.min = 20
            self.assertAlmostEqual(axis.min, 20)
            self.assertAlmostEqual(axis.max, 40)

            axis.max = 10
            self.assertAlmostEqual(axis.min, -10)
            self.assertAlmostEqual(axis.max, 10)

            axis.min = axis.max
            self.assertAlmostEqual(axis.min, 10)
            self.assertAlmostEqual(axis.max, 30)

            axis.max = axis.min
            self.assertAlmostEqual(axis.min, -10)
            self.assertAlmostEqual(axis.max, 10)


class TestSketchAxis(unittest.TestCase, TestAxis):
    def setUp(self):
        tp.new_layout()
        fr = tp.active_frame()
        fr.activate()
        ds = fr.dataset
        xvar = ds.add_variable('X')
        z = ds.add_ordered_zone('Zone', (2,))
        xx = np.linspace(-1,1,2)
        z.values('X')[:] = xx
        plot = fr.plot(PlotType.Sketch)
        plot.activate()
        plot.axes.axis_mode = AxisMode.Independent
        self.axes = [plot.axes.x_axis, plot.axes.y_axis]

    def test_minmax_connected(self):
        with patch.object(tp.plot.axis.session, 'connected',
                          Mock(return_value=True)):
            for axis in self.axes:
                axis.min = -1000
                self.assertAlmostEqual(axis.min, -1000)
                axis.max = 1000
                self.assertAlmostEqual(axis.max, 1000)

                axis.min = 0
                self.assertAlmostEqual(axis.min, 0)
                axis.max = 1
                self.assertAlmostEqual(axis.max, 1)

                with self.assertRaises((ValueError, TypeError,
                                        TecplotSystemError)):
                    axis.min = 'badvalue'
                with self.assertRaises((ValueError, TypeError,
                                        TecplotSystemError)):
                    axis.max = 'badvalue'

    ''' DEBUGGING CODE FOR SKETCH MIN/MAX SETTING
    def test_minmax(self):
        def set_limit(axis, limit, value):
            setattr(axis, limit, value)
            #fmt = '$!SketchAxis {}Detail {{ Range{} = {} }}'
            #cmd = fmt.format(axis.name, limit.capitalize(), value)
            #tp.macro.execute_command(cmd)

        for axis in self.axes:
            set_limit(axis, 'min', -1000)
            self.assertAlmostEqual(axis.min, -1000)
            set_limit(axis, 'max', 1000)
            self.assertAlmostEqual(axis.max, 1000)

            set_limit(axis, 'min', 0)
            self.assertAlmostEqual(axis.min, 0)
            set_limit(axis, 'max', 1)
            self.assertAlmostEqual(axis.max, 1)

            with self.assertRaises(ValueError):
                set_limit(axis, 'min', 'badvalue')
            with self.assertRaises(ValueError):
                set_limit(axis, 'max', 'badvalue')

    def test_minmax_outside_range(self):
        def set_limit(axis, limit, value):
            cmd = '$!SketchAxis {}Detail{{Range{} = {}}}'
            tp.macro.execute_command(cmd.format(axis.name, limit.capitalize(), value))

        for axis in self.axes:
            set_limit(axis, 'min', -10)
            set_limit(axis, 'max', 10)
            self.assertAlmostEqual(axis.min, -10)
            self.assertAlmostEqual(axis.max, 10)

            set_limit(axis, 'min', 10)
            self.assertAlmostEqual(axis.min, 20)
            self.assertAlmostEqual(axis.max, 40)

            set_limit(axis, 'max', 10)
            self.assertAlmostEqual(axis.min, -10)
            self.assertAlmostEqual(axis.max, 10)

            set_limit(axis, 'min', axis.max)
            self.assertAlmostEqual(axis.min, 10)
            self.assertAlmostEqual(axis.max, 30)

            set_limit(axis, 'max', axis.min)
            self.assertAlmostEqual(axis.min, -10)
            self.assertAlmostEqual(axis.max, 10)

        def setprop(axis, attr, value):
            for _ in range(1000):
                setattr(axis, attr, value)
                if abs(getattr(axis, attr) - value) < 1e-5:
                    break

        try:
            if tp.session.connected():
                if _tecutil_connector.client.tuserver_version > 5:
                    _tecutil_connector.client.processing_mode = \
                        TecUtilServerProcessingMode.Single

            plot = self.axes[0].axes.plot

            for axis in self.axes:

                if tp.sdk_version_info < (2017, 3):
                    msg = None
                else:
                    if plot.frame.has_dataset:
                        ds = plot.frame.dataset
                    else:
                        ds = None
                    msg = str([str(x) for x in [plot, axis, axis._sv, ds]])

                setprop(axis, 'min', -200)
                setprop(axis, 'max', 200)
                for val in [-100,-1,-0.5,0,0.5,1,100]:
                    setprop(axis, 'min', val)
                    self.assertAlmostEqual(axis.min, val, msg=msg)
                    setprop(axis, 'max', val)
                    self.assertAlmostEqual(axis.max, val, msg=msg)

                setprop(axis, 'min', -1)
                setprop(axis, 'max', 1)
                setprop(axis, 'min', 3) # shifts axis range from [-1,1] to [3,5]
                self.assertAlmostEqual(axis.min, 3, msg=msg)
                self.assertAlmostEqual(axis.max, 5, msg=msg)

                with self.assertRaises(ValueError):
                    axis.min = 'badvalue'
                with self.assertRaises(ValueError):
                    axis.max = 'badvalue'

        finally:
            if tp.session.connected():
                if _tecutil_connector.client.tuserver_version > 5:
                    _tecutil_connector.client.processing_mode = \
                        TecUtilServerProcessingMode.Unspecified
    '''

class TestCartesian2DAxis(object):
    def test_reverse(self):
        for axis in self.axes:
            for val in [True,False,True]:
                axis.reverse = val
                self.assertEqual(axis.reverse, val)

    def test_subclasses(self):
        for axis in self.axes:
            self.assertIsInstance(axis, Cartesian2DFieldAxis)
            self.assertIsInstance(axis.ticks, Ticks2D)
            self.assertIsInstance(axis.tick_labels, TickLabels2D)
            self.assertIsInstance(axis.grid_lines, GridLines2D)
            self.assertIsInstance(axis.minor_grid_lines, MinorGridLines2D)
            self.assertIsInstance(axis.marker_grid_line, MarkerGridLine2D)
            self.assertIsInstance(axis.title, DataAxis2DTitle)
            self.assertIsInstance(axis.line, Cartesian2DAxisLine)


class TestFieldAxis(object):
    def test_variable(self):
        ds = self.axes[0].axes.plot.frame.dataset
        for axis in self.axes:
            for i in [0,1,3]:
                axis.variable_index = i
                self.assertEqual(axis.variable_index, i)
                self.assertEqual(axis.variable, ds.variable(i))
            for i in [0,1,3]:
                axis.variable = ds.variable(i)
                self.assertEqual(axis.variable_index, i)
                self.assertEqual(axis.variable, ds.variable(i))

    def test_fit_range_with_blanking(self):
        self.axes[0].fit_range(True)

    def test_minmax_with_new_axis_variable(self):
        fr = tp.active_frame()
        plot = fr.plot()
        dataset = fr.dataset
        tp.data.operate.execute_equation('{a}={X}')
        plot.axes.x_axis.variable = dataset.variable('a')
        plot.axes.x_axis.max = 2.0
        self.assertAlmostEqual(plot.axes.x_axis.max, 2.0)
        plot.axes.x_axis.max = 4.0
        self.assertAlmostEqual(plot.axes.x_axis.max, 4.0)

        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as ftmp:
            ftmp.close()
            try:
                tp.export.save_png(ftmp.name, 10, supersample=1)
            finally:
                os.remove(ftmp.name)

        self.assertAlmostEqual(plot.axes.x_axis.max, 4.0)


class TestCartesian2DFieldAxis(unittest.TestCase, TestCartesian2DAxis,
                               TestFieldAxis, TestAxis):
    def setUp(self):
        tp.new_layout()
        self.filename,ds = sample_data('3x3x3_p')
        fr = tp.active_frame()
        fr.activate()
        plot = fr.plot(PlotType.Cartesian2D)
        plot.activate()
        self.axes = [plot.axes.x_axis, plot.axes.y_axis]

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)


class TestCartesian3DFieldAxis(unittest.TestCase, TestFieldAxis, TestAxis):
    def setUp(self):
        tp.new_layout()
        self.filename,ds = sample_data('3x3x3_p')
        fr = tp.active_frame()
        fr.activate()
        plot = fr.plot(PlotType.Cartesian3D)
        plot.activate()
        self.axes = [plot.axes.x_axis, plot.axes.y_axis, plot.axes.z_axis]

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_subclasses(self):
        for axis in self.axes:
            self.assertIsInstance(axis, Cartesian3DFieldAxis)
            self.assertIsInstance(axis.ticks, Ticks3D)
            self.assertIsInstance(axis.tick_labels, TickLabels3D)
            self.assertIsInstance(axis.grid_lines, GridLines)
            self.assertIsInstance(axis.minor_grid_lines, MinorGridLines)
            self.assertIsInstance(axis.marker_grid_line, MarkerGridLine)
            self.assertIsInstance(axis.title, DataAxis3DTitle)
            self.assertIsInstance(axis.line, AxisLine3D)

    def test_scale_factor(self):
        for axis in self.axes:
            for val in [-100,-1,-0.5,0,0.5,1,100]:
                axis.scale_factor = val
                self.assertAlmostEqual(axis.scale_factor, val)
            with self.assertRaises(ValueError):
                axis.scale_factor = 'badvalue'
            with self.assertRaises(ValueError):
                axis.scale_factor = 'badvalue'


class TestXYLineAxis(unittest.TestCase, TestCartesian2DAxis, TestAxis):
    def setUp(self):
        tp.new_layout()
        self.filename,ds = sample_data('xylines_poly')
        fr = tp.active_frame()
        fr.activate()
        plot = fr.plot(PlotType.XYLine)
        plot.activate()
        self.axes = [
            plot.axes.x_axis(0),
            plot.axes.y_axis(0),
            plot.axes.x_axis(4),
            plot.axes.y_axis(4)]

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    @skip_if_sdk_version_before(2018, 1)
    def test_log_scale(self):
        for axis in self.axes:
            for val in [True,False,True]:
                axis.log_scale = val
                self.assertEqual(axis.log_scale, val)

    def test_eq(self):
        self.assertTrue(self.axes[0] == tp.active_frame().plot().axes.x_axis(0))
        self.assertFalse(self.axes[0] == self.axes[1])
        self.assertFalse(self.axes[0] != tp.active_frame().plot().axes.x_axis(0))
        self.assertTrue(self.axes[0] != self.axes[1])

    def test_subclasses(self):
        for axis in self.axes:
            self.assertIsInstance(axis, XYLineAxis)
            self.assertIsInstance(axis.ticks, Ticks2D)
            self.assertIsInstance(axis.tick_labels, TickLabels2D)
            self.assertIsInstance(axis.grid_lines, GridLines2D)
            self.assertIsInstance(axis.minor_grid_lines, MinorGridLines2D)
            self.assertIsInstance(axis.marker_grid_line, MarkerGridLine2D)
            self.assertIsInstance(axis.title, Axis2DTitle)
            self.assertIsInstance(axis.line, Cartesian2DAxisLine)


class TestPolarLineAxis(object):
    def test_show(self):
        for val in [True,False,True]:
            self.axis.show = val
            self.assertEqual(self.axis.show, val)

    def test_theta_line(self):
        self.assertIsInstance(self.axis.axes.theta_axis.line, AxisLine2D)

    def test_minmax(self):
        for val in [-100,-1,-0.5,0,0.5,1,100]:
            self.axis.min = val
            self.assertAlmostEqual(self.axis.min, val)
            self.axis.max = val
            self.assertAlmostEqual(self.axis.max, val)
        with self.assertRaises(ValueError):
            self.axis.min = 'badvalue'
        with self.assertRaises(ValueError):
            self.axis.max = 'badvalue'

    def test_origin(self):
        for val in [-100,-1,-0.5,0,0.5,1,100]:
            self.axis.origin = val
            self.assertAlmostEqual(self.axis.origin, val)
        with self.assertRaises(ValueError):
            self.axis.origin = 'badvalue'

    def test_clip_data(self):
        for val in [True, False, True]:
            self.axis.clip_data = val
            self.assertEqual(self.axis.clip_data, val)


class TestRadialLineAxis(TestPolarLineAxis, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename,ds = sample_data('xylines_poly')
        fr = tp.active_frame()
        fr.activate()
        plot = fr.plot(PlotType.PolarLine)
        plot.activate()
        self.axis = plot.axes.r_axis

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_subclasses(self):
        self.assertIsInstance(self.axis, RadialLineAxis)
        self.assertIsInstance(self.axis.ticks, Ticks2D)
        self.assertIsInstance(self.axis.tick_labels, TickLabels2D)
        self.assertIsInstance(self.axis.grid_lines, GridLines2D)
        self.assertIsInstance(self.axis.minor_grid_lines, MinorGridLines2D)
        self.assertIsInstance(self.axis.marker_grid_line, MarkerGridLine2D)
        self.assertIsInstance(self.axis.title, RadialAxisTitle)
        self.assertIsInstance(self.axis.line, AxisLine2D)


class TestPolarAngleAxis(TestPolarLineAxis, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename,ds = sample_data('xylines_poly')
        fr = tp.active_frame()
        fr.activate()
        plot = fr.plot(PlotType.PolarLine)
        plot.activate()
        self.axis = plot.axes.theta_axis

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_grid_types(self):
        self.assertIsInstance(self.axis.grid_lines, PolarAngleGridLines)
        self.assertIsInstance(self.axis.minor_grid_lines,
                              PolarAngleMinorGridLines)
        self.assertIsInstance(self.axis.marker_grid_line,
                              PolarAngleMarkerGridLine)

    def test_mode(self):
        for mode in [ThetaMode.Degrees, ThetaMode.Radians, ThetaMode.Degrees]:
            self.axis.mode = mode
            self.assertEqual(self.axis.mode, mode)
        with self.assertRaises(ValueError):
            self.axis.mode = 0.5

    def test_period(self):
        for val in [0.5,1,100]:
            self.axis.period = val
            self.assertAlmostEqual(self.axis.period, val)
        with self.assertRaises(ValueError):
            self.axis.period = 'badvalue'
        with self.assertRaises(TecplotSystemError):
            self.axis.period = -1
        with self.assertRaises(TecplotSystemError):
            self.axis.period = 0

    def test_set_range_to_entire_circle(self):
        self.axis.mode = ThetaMode.Degrees
        self.axis.min = 0
        self.axis.max = 10
        self.axis.set_range_to_entire_circle()
        self.assertAlmostEqual(self.axis.min, 0)
        self.assertAlmostEqual(self.axis.max, 360)
        with patch_tecutil('ViewX', return_value=False):
            with self.assertRaises(TecplotSystemError):
                self.axis.set_range_to_entire_circle()


class TestAxisLine(object):
    def test_show(self):
        for val in [True,False,True]:
            self.line.show = val
            self.assertEqual(self.line.show, val)

    def test_color(self):
        for val in [Color.Blue, Color.Red, Color.Black]:
            self.line.color = val
            self.assertEqual(self.line.color, val)
        with self.assertRaises(ValueError):
            self.line.color = 0.5

    def test_line_thickness(self):
        for val in [0.5,1,100]:
            self.line.line_thickness = val
            self.assertAlmostEqual(self.line.line_thickness, val)
        with self.assertRaises(ValueError):
            self.line.line_thickness = 'badvalue'
        with self.assertRaises(TecplotSystemError):
            self.line.line_thickness = 0
        with self.assertRaises(TecplotSystemError):
            self.line.line_thickness = -1


class TestAxisLine2D(TestAxisLine, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename,ds = sample_data('xylines_poly')
        fr = tp.active_frame()
        fr.activate()
        plot = fr.plot(PlotType.XYLine)
        plot.activate()
        self.line = plot.axes.x_axis(0).line

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_offset(self):
        for val in [-100,-1,-0.5,0,0.5,1,100]:
            self.line.offset = val
            self.assertAlmostEqual(self.line.offset, val)
        with self.assertRaises(ValueError):
            self.line.offset = 'badvalue'

    def test_opposing_axis_value(self):
        for val in [True,False,True]:
            self.line.opposing_axis_value = val
            self.assertEqual(self.line.opposing_axis_value, val)

    def test_alignment(self):
        for val in [AxisAlignment.WithViewport,
                    AxisAlignment.WithOpposingAxisValue,
                    AxisAlignment.WithGridMin]:
            self.line.alignment = val
            self.assertEqual(self.line.alignment, val)
        with self.assertRaises(ValueError):
            self.line.alignment = 'badvalue'


class TestCartesian2DAxisLine(TestAxisLine2D):
    def setUp(self):
        tp.new_layout()
        self.filename,ds = sample_data('3x3x3_p')
        fr = tp.active_frame()
        fr.activate()
        plot = fr.plot(PlotType.Cartesian2D)
        plot.activate()
        self.line = plot.axes.x_axis.line

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_position(self):
        for val in [0,0.5,1,100]:
            self.line.position = val
            self.assertEqual(self.line.position, val)
        with self.assertRaises(ValueError):
            self.line.position = 'badvalue'
        with self.assertRaises(TecplotSystemError):
            self.line.position = -1
        with self.assertRaises(TecplotSystemError):
            self.line.position = 150


class TestAxisLine3D(TestAxisLine, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename,ds = sample_data('3x3x3_p')
        fr = tp.active_frame()
        fr.activate()
        plot = fr.plot(PlotType.Cartesian3D)
        plot.activate()
        self.line = plot.axes.x_axis.line

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_show_on_opposite_edge(self):
        for val in [True,False,True]:
            self.line.show_on_opposite_edge = val
            self.assertEqual(self.line.show_on_opposite_edge, val)

    def test_edge_assignment(self):
        for val in [AxisLine3DAssignment.YMinZMin,
                    AxisLine3DAssignment.YMinZMax,
                    AxisLine3DAssignment.Automatic]:
            self.line.edge_assignment = val
            self.assertEqual(self.line.edge_assignment, val)
        self.line.edge_assignment = None
        self.assertEqual(self.line.edge_assignment,
                         AxisLine3DAssignment.Automatic)
        with self.assertRaises(ValueError):
            self.line.edge_assignment = 0.5


class TestRadialAxisLine2D(TestAxisLine2D):
    def setUp(self):
        tp.new_layout()
        self.filename,ds = sample_data('xylines_poly')
        fr = tp.active_frame()
        fr.activate()
        plot = fr.plot(PlotType.PolarLine)
        plot.activate()
        self.line = plot.axes.r_axis.line

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_show_both_directions(self):
        for val in [True,False,True]:
            self.line.show_both_directions = val
            self.assertEqual(self.line.show_both_directions, val)

    def test_show_perpendicular(self):
        for val in [True,False,True]:
            self.line.show_perpendicular = val
            self.assertEqual(self.line.show_perpendicular, val)

    def test_angle(self):
        for val in [-100,-1,-0.5,0,0.5,1,100]:
            self.line.angle = val
            self.assertAlmostEqual(self.line.angle, val)
        with self.assertRaises(ValueError):
            self.line.angle = 'badvalue'

    def test_alignment(self):
        for val in [AxisAlignment.WithOpposingAxisValue,
                    AxisAlignment.WithGridMin,
                    AxisAlignment.WithGridMax,
                    AxisAlignment.WithSpecificAngle]:
            self.line.alignment = val
            self.assertEqual(self.line.alignment, val)
        with self.assertRaises(ValueError):
            self.line.alignment = 'badvalue'


if __name__ == '__main__':
    from .. import main
    main()
