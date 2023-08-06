import os
import unittest

import tecplot as tp
from tecplot.tecutil import sv
from tecplot.constant import *
from tecplot.exception import *

from test import assert_style, skip_if_sdk_version_before, patch_tecutil
from ..sample_data import sample_data


class TestReferenceVectorLabel(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.datafile, ds = sample_data('3x3x3_p')
        vec = tp.active_frame().plot(PlotType.Cartesian2D).vector
        vec.u_variable = ds.variable(2)
        vec.v_variable = ds.variable(3)
        self.label = vec.reference_vector.label

    def tearDown(self):
        tp.new_layout()
        os.remove(self.datafile)

    def test_show(self):
        for val in [True, False, True]:
            self.label.show = val
            self.assertEqual(self.label.show, val)

    def test_color(self):
        for val in [Color.Black, Color.Red, Color.Blue]:
            self.label.color = val
            self.assertEqual(self.label.color, val)
        with self.assertRaises(ValueError):
            self.label.color = 0.5

    def test_offset(self):
        for val in [-100, -2, -1, -0.5, 0, 0.5, 1, 2, 100]:
            self.label.offset = val
            self.assertEqual(self.label.offset, val)
        with self.assertRaises(ValueError):
            self.label.offset = 'badtype'
        with self.assertRaises(TecplotSystemError):
            self.label.offset = -101
        with self.assertRaises(TecplotSystemError):
            self.label.offset = 101

    def test_font(self):
        self.assertIsInstance(self.label.font, tp.text.Font)

    def test_format(self):
        self.assertIsInstance(self.label.format, tp.text.LabelFormat)


class TestReferenceVector(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.datafile, ds = sample_data('3x3x3_p')
        vec = tp.active_frame().plot(PlotType.Cartesian2D).vector
        vec.u_variable = ds.variable(2)
        vec.v_variable = ds.variable(3)
        self.ref = vec.reference_vector

    def tearDown(self):
        tp.new_layout()
        os.remove(self.datafile)

    def test_show(self):
        for val in [True, False, True]:
            self.ref.show = val
            self.assertEqual(self.ref.show, val)

        with assert_style(True, sv.GLOBALTWODVECTOR, sv.REFVECTOR, sv.SHOW,
                          UNIQUEID=self.ref.vector.plot.frame.uid):
            self.ref.show = True
            _ = self.ref.show

    def test_color(self):
        for val in [Color.Black, Color.Red, Color.Blue]:
            self.ref.color = val
            self.assertEqual(self.ref.color, val)
        with self.assertRaises(ValueError):
            self.ref.color = 0.5

    def test_position(self):
        for val in [(0, 0), (0, 1), (1, 0), (100, 100)]:
            self.ref.position = val
            self.assertEqual(self.ref.position, val)
        with self.assertRaises(TecplotSystemError):
            self.ref.position = (-1, 0)
        with self.assertRaises(TecplotSystemError):
            self.ref.position = (0, -1)
        with self.assertRaises(TecplotSystemError):
            self.ref.position = (101, 0)
        with self.assertRaises(TecplotSystemError):
            self.ref.position = (0, 101)
        with self.assertRaises(TypeError):
            self.ref.position = 1
        with self.assertRaises(ValueError):
            self.ref.position = "badvalue"
        with self.assertRaises(TypeError):
            self.ref.position = None

    def test_magnitude(self):
        for val in [0.5, 1, 2, 100]:
            self.ref.magnitude = val
            self.assertEqual(self.ref.magnitude, val)
        with self.assertRaises(ValueError):
            self.ref.magnitude = 'badtype'
        with self.assertRaises(TecplotSystemError):
            self.ref.magnitude = -1
        with self.assertRaises(TecplotSystemError):
            self.ref.magnitude = 0

    def test_angle(self):
        for val in [-100, -1, 0, 0.5, 1, 2, 100]:
            self.ref.angle = val
            self.assertEqual(self.ref.angle, val)
        with self.assertRaises(ValueError):
            self.ref.angle = 'badtype'

    def test_line_thickness(self):
        for val in [0.5, 1, 2, 100]:
            self.ref.line_thickness = val
            self.assertEqual(self.ref.line_thickness, val)
        with self.assertRaises(ValueError):
            self.ref.line_thickness = 'badtype'
        with self.assertRaises(TecplotSystemError):
            self.ref.line_thickness = -1
        with self.assertRaises(TecplotSystemError):
            self.ref.line_thickness = 0
        with self.assertRaises(TecplotSystemError):
            self.ref.line_thickness = 101

    def test_label(self):
        self.assertIsInstance(self.ref.label, tp.plot.ReferenceVectorLabel)


class _TestVector(object):
    def test_arrowhead_angle(self):
        for val in [1, 45.5, 90]:
            self.vector.arrowhead_angle = val
            self.assertEqual(self.vector.arrowhead_angle, val)
        with self.assertRaises(ValueError):
            self.vector.arrowhead_angle = 'badtype'
        with self.assertRaises(TecplotSystemError):
            self.vector.arrowhead_angle = 0
        with self.assertRaises(TecplotSystemError):
            self.vector.arrowhead_angle = 91

    def test_arrowhead_fraction(self):  # 0-10
        for val in [0, 1.1, 10]:
            self.vector.arrowhead_fraction = val
            self.assertEqual(self.vector.arrowhead_fraction, val)
        with self.assertRaises(ValueError):
            self.vector.arrowhead_fraction = 'badtype'
        with self.assertRaises(TecplotSystemError):
            self.vector.arrowhead_fraction = -1
        with self.assertRaises(TecplotSystemError):
            self.vector.arrowhead_fraction = 11

    def test_arrowhead_size(self):  # 0-100
        for val in [0, 1.1, 100]:
            self.vector.arrowhead_size = val
            self.assertEqual(self.vector.arrowhead_size, val)
        with self.assertRaises(ValueError):
            self.vector.arrowhead_size = 'badtype'
        with self.assertRaises(TecplotSystemError):
            self.vector.arrowhead_size = -1
        with self.assertRaises(TecplotSystemError):
            self.vector.arrowhead_size = 101

    def test_use_grid_units(self):
        for val in [True, False, True]:
            self.vector.use_grid_units = val
            self.assertEqual(self.vector.use_grid_units, val)

    def test_size_arrowhead_by_fraction(self):
        for val in [True, False, True]:
            self.vector.size_arrowhead_by_fraction = val
            self.assertEqual(self.vector.size_arrowhead_by_fraction, val)

    def test_length(self):
        for val in [0, 1.1, 100]:
            self.vector.length = val
            self.assertEqual(self.vector.length, val)
        with self.assertRaises(ValueError):
            self.vector.length = 'badtype'
        with self.assertRaises(TecplotSystemError):
            self.vector.length = -1
        with self.assertRaises(TecplotSystemError):
            self.vector.length = 101

    @skip_if_sdk_version_before(2019, 2)
    def test_use_even_spacing(self):
        for val in [True, False, True]:
            self.vector.use_even_spacing = val
            self.assertEqual(self.vector.use_even_spacing, val)

    def test_use_relative(self):
        for val in [True, False, True]:
            self.vector.use_relative = val
            self.assertEqual(self.vector.use_relative, val)

    def test_reference_vector(self):
        self.assertIsInstance(self.vector.reference_vector,
                              tp.plot.ReferenceVector)

    def test_variables(self):
        self.vector.u_variable = self.ds.variable(0)
        self.vector.v_variable = self.ds.variable(1)
        self.assertEqual(self.vector.u_variable, self.ds.variable(0))
        self.assertEqual(self.vector.v_variable, self.ds.variable(1))
        self.assertEqual(self.vector.u_variable_index, 0)
        self.assertEqual(self.vector.v_variable_index, 1)

        self.vector.u_variable_index = 2
        self.vector.v_variable_index = 3
        self.assertEqual(self.vector.u_variable, self.ds.variable(2))
        self.assertEqual(self.vector.v_variable, self.ds.variable(3))
        self.assertEqual(self.vector.u_variable_index, 2)
        self.assertEqual(self.vector.v_variable_index, 3)


class TestVector2D(_TestVector, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.datafile, self.ds = sample_data('3x3x3_p')
        self.plot = tp.active_frame().plot(PlotType.Cartesian2D)
        self.plot.activate()
        self.vector = self.plot.vector
        self.vector.u_variable = self.ds.variable(2)
        self.vector.v_variable = self.ds.variable(3)

    def tearDown(self):
        tp.new_layout()
        os.remove(self.datafile)

    def test_type(self):
        self.assertIsInstance(self.vector, tp.plot.Vector2D)

    @skip_if_sdk_version_before(2017, 3)
    def test_relative_length(self):
        # 0.04 below is calculated based on loaded dataset
        self.assertEqual(self.vector.relative_length, 0.025)
        for val in [0, 0.01, 1.1, 200]:
            self.vector.relative_length = val
            self.assertEqual(self.vector.relative_length, val)

        with self.assertRaises(ValueError):
            self.vector.relative_length = 'badtype'
        with self.assertRaises(TecplotSystemError):
            self.vector.relative_length = -1

    @skip_if_sdk_version_before(2019, 2)
    def test_even_spacing(self):
        for xval in [0.1, 0.2]:
            for yval in [0.1, 0.2]:
                self.vector.even_spacing = (xval, yval)
                self.assertEqual(self.vector.even_spacing,(xval, yval))

        with self.assertRaises(ValueError):
            self.vector.even_spacing = 'badtype'
        with self.assertRaises(TecplotSystemError):
            self.vector.even_spacing.x = -1.0
        with self.assertRaises(TecplotSystemError):
            self.vector.even_spacing.y = -1.0

    @skip_if_sdk_version_before(2019, 2)
    def test_reset_even_spacing(self):
        self.vector.reset_even_spacing()
        orig_spacing = self.vector.even_spacing
        new_spacing = (orig_spacing[0] + 0.5, orig_spacing[1] + 0.5)
        self.vector.even_spacing = new_spacing
        self.assertAlmostEqual(self.vector.even_spacing[0], new_spacing[0])
        self.assertAlmostEqual(self.vector.even_spacing[1], new_spacing[1])
        self.vector.reset_even_spacing()
        self.assertAlmostEqual(self.vector.even_spacing[0], orig_spacing[0])
        self.assertAlmostEqual(self.vector.even_spacing[1], orig_spacing[1])

        with patch_tecutil('ResetVectorSpacing', return_value=False):
            with self.assertRaises(TecplotSystemError):
                self.vector.reset_even_spacing()

    def test_reset_vector_length(self):
        self.plot.show_vector = True
        self.vector.reset_length()
        orig_length = self.vector.relative_length
        self.vector.relative_length = orig_length * 1.1
        self.vector.reset_length()
        self.assertAlmostEqual(self.vector.relative_length, orig_length)

        # Test that we don't allow reset if vector vars are not assigned.
        # See inverse test for 2D over on 3D side..
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            with tp.active_frame().plot(PlotType.Cartesian3D).activated():
                self.vector.reset_length()


class TestVector3D(TestVector2D):
    def setUp(self):
        tp.new_layout()
        self.datafile, self.ds = sample_data('3x3x3_p')
        self.plot = tp.active_frame().plot()
        self.vector = self.plot.vector
        self.vector.u_variable = self.ds.variable(1)
        self.vector.v_variable = self.ds.variable(2)
        self.vector.w_variable = self.ds.variable(3)

    def tearDown(self):
        tp.new_layout()
        os.remove(self.datafile)

    def test_type(self):
        self.assertIsInstance(self.vector, tp.plot.Vector3D)

    def test_w_variable(self):
        self.vector.w_variable = self.ds.variable(0)
        self.assertEqual(self.vector.w_variable, self.ds.variable(0))
        self.assertEqual(self.vector.w_variable_index, 0)

        self.vector.w_variable_index = 2
        self.assertEqual(self.vector.w_variable, self.ds.variable(2))
        self.assertEqual(self.vector.w_variable_index, 2)

    @skip_if_sdk_version_before(2017, 3)
    def test_relative_length(self):
        # 0.04 below is calculated based on loaded dataset
        self.assertEqual(self.vector.relative_length, 0.04)
        for val in [0, 0.01, 1.1, 200]:
            self.vector.relative_length = val
            self.assertEqual(self.vector.relative_length, val)

        with self.assertRaises(ValueError):
            self.vector.relative_length = 'badtype'
        with self.assertRaises(TecplotSystemError):
            self.vector.relative_length = -1

    @skip_if_sdk_version_before(2019, 2)
    def test_even_spacing(self):
        for xval in [0.1, 0.2]:
            for yval in [0.1, 0.2]:
                for zval in [0.1, 0.2]:
                    self.vector.even_spacing = (xval, yval, zval)
                    self.assertEqual(self.vector.even_spacing,(xval, yval, zval))

        with self.assertRaises(ValueError):
            self.vector.even_spacing = 'badtype'
        with self.assertRaises(TecplotSystemError):
            self.vector.even_spacing.x = -1.0
        with self.assertRaises(TecplotSystemError):
            self.vector.even_spacing.y = -1.0
        with self.assertRaises(TecplotSystemError):
            self.vector.even_spacing.z = -1.0

    @skip_if_sdk_version_before(2019, 2)
    def test_reset_even_spacing(self):
        self.vector.reset_even_spacing()
        orig_spacing = self.vector.even_spacing
        new_spacing = (orig_spacing[0] + 0.5,
                       orig_spacing[1] + 0.5,
                       orig_spacing[2] + 0.5,)
        self.vector.even_spacing = new_spacing
        self.assertAlmostEqual(self.vector.even_spacing[0], new_spacing[0])
        self.assertAlmostEqual(self.vector.even_spacing[1], new_spacing[1])
        self.assertAlmostEqual(self.vector.even_spacing[2], new_spacing[2])
        self.vector.reset_even_spacing()
        self.assertAlmostEqual(self.vector.even_spacing[0], orig_spacing[0])
        self.assertAlmostEqual(self.vector.even_spacing[1], orig_spacing[1])
        self.assertAlmostEqual(self.vector.even_spacing[2], orig_spacing[2])

        with patch_tecutil('ResetVectorSpacing', return_value=False):
            with self.assertRaises(TecplotSystemError):
                self.vector.reset_even_spacing()

    def test_reset_vector_length(self):
        self.plot.show_vector = True
        self.vector.reset_length()
        orig_length = self.vector.relative_length
        self.vector.relative_length = orig_length * 1.1
        self.vector.reset_length()
        self.assertAlmostEqual(self.vector.relative_length, orig_length)

        # Test that we don't allow reset if vector vars are not assigned.
        # See inverse test for 3D over on 2D side..
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            with tp.active_frame().plot(PlotType.Cartesian2D).activated():
                self.vector.reset_length()


if __name__ == '__main__':
    from .. import main
    main()
