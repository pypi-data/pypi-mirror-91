# coding: utf-8
from __future__ import unicode_literals

import base64
import os
import sys
import unittest
import zlib

import numpy as np
from numpy import random as rand

from contextlib import contextmanager
from ctypes import *
from tempfile import NamedTemporaryFile
from unittest.mock import patch, Mock, PropertyMock, MagicMock
from .. import patch_tecutil

import tecplot as tp
from tecplot import session, tecutil
from tecplot.exception import *
from tecplot.constant import *
from tecplot.tecutil import sv
from tecplot.data import Dataset, Variable

from .. import sample_data


class TestExecuteEquationIndexing(unittest.TestCase):
    def setUp(self):
        shape = (6, 7, 8)
        x = np.linspace(0, 1, shape[0])
        y = np.linspace(0, 1, shape[1])
        z = np.linspace(0, 3, shape[2])

        # Create (x,y,z) mesh with indexing (i,j,k) = shape
        Z, Y, X = np.meshgrid(z, y, x, indexing='ij')
        shape = Z.shape[::-1]

        # Adjust x position to vary along z
        X += np.sin(Z)

        # Set the values at each node
        scalar_data = np.sqrt(Y**2 + Z**2)

        # Add some noise just for fun, fixing the random seed for this example
        rand.seed(1)
        scalar_data += rand.normal(0, 0.2, scalar_data.shape)

        # Setup dataset and zone
        tp.new_layout()
        fr = tp.active_frame()
        ds = fr.create_dataset('Data', ['x','y','z','s'])
        z = ds.add_ordered_zone(name='Ordered Float Nodal {}'.format(shape),
                                shape=shape)

        # Fill in node locations
        z.values('x')[:] = X
        z.values('y')[:] = Y
        z.values('z')[:] = Z

        # Set the scalar data
        z.values('s')[:] = scalar_data

        plot = fr.plot(PlotType.Cartesian3D)
        plot.activate()

    def test_irange(self):
        z = tp.active_frame().dataset.zone(0)
        s = z.values('s')

        s[:] = np.zeros(z.num_points)
        tp.data.operate.execute_equation('{s} = 1')
        np.testing.assert_allclose(s[:], np.ones(z.num_points))

        s[:] = np.zeros(z.num_points)
        ss = np.zeros(z.dimensions[::-1])
        ss[...,1:] = 1
        tp.data.operate.execute_equation('{s} = 1', i_range=(1, None, None))
        np.testing.assert_allclose(s[:], ss.ravel())

        s[:] = np.zeros(z.num_points)
        ss[:] = 0
        ss[...,1:4:2] = 1
        tp.data.operate.execute_equation('{s} = 1', i_range=(1, 3, 2))
        np.testing.assert_allclose(s[:], ss.ravel())

        s[:] = np.zeros(z.num_points)
        ss[:] = 0
        ss[...,1:5:1] = 1
        tp.data.operate.execute_equation('{s} = 1', i_range=(1, 4, 1))
        np.testing.assert_allclose(s[:], ss.ravel())

        s[:] = np.zeros(z.num_points)
        ss[:] = 0
        ss[...,1:5:2] = 1
        tp.data.operate.execute_equation('{s} = 1', i_range=(1, 4, 2))
        np.testing.assert_allclose(s[:], ss.ravel())

        s[:] = np.zeros(z.num_points)
        ss[:] = 0
        ss[...,1:4:3] = 1
        tp.data.operate.execute_equation('{s} = 1', i_range=(1, 3, 3))
        np.testing.assert_allclose(s[:], ss.ravel())

        s[:] = np.zeros(z.num_points)
        ss[:] = 0
        ss[...,1:5:3] = 1
        tp.data.operate.execute_equation('{s} = 1', i_range=(1, 4, 3))
        np.testing.assert_allclose(s[:], ss.ravel())

    def test_ijkrange(self):
        z = tp.active_frame().dataset.zone(0)
        s = z.values('s')

        s[:] = np.zeros(z.num_points)
        tp.data.operate.execute_equation('{s} = 1')
        np.testing.assert_allclose(s[:], np.ones(z.num_points))

        s[:] = np.zeros(z.num_points)
        ss = np.zeros(z.dimensions[::-1])
        ss[1:-1:3,:3:2,:2] = 1
        tp.data.operate.execute_equation('{s} = 1',
            i_range=(0, 1, 1),
            j_range=(0, 2, 2),
            k_range=(1, -2, 3)
        )
        np.testing.assert_allclose(s[:], ss.ravel())


class TestExecuteEquation(unittest.TestCase):

    def setUp(self):
        tp.new_layout()
        self.filename, self.ds = sample_data.sample_data('3x3_2x2')
        self.z_inner = self.ds.zone('Rectangular zone inner')
        self.z_outer = self.ds.zone('Rectangular zone outer')
        self.z_var = self.z_inner.values('Z')  # type: Variable

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_range_option(self):
        # noinspection PyStatementEffect
        def fake_data_alter(arglist):
            for option in [sv.IMIN, sv.IMAX, sv.ISKIP,
                           sv.JMIN, sv.JMAX, sv.JSKIP,
                           sv.KMIN, sv.KMAX, sv.KSKIP]:
                with self.assertRaises((TypeError, KeyError)):
                    arglist[option]

            return True

        with patch_tecutil('DataAlterX', side_effect=fake_data_alter):
            # Even though we are passing Range tuples, since the
            # min/max/skip values are None, none of the corresponding
            # options should exist in the arglist value passed to
            # the fake data alter function above.
            tp.data.operate.execute_equation(
                'X', i_range=(None, None, None))

            tp.data.operate.execute_equation(
                'X', j_range=(None, None, None))

            tp.data.operate.execute_equation(
                'X', k_range=(None, None, None))

    def test_return_value(self):
        with patch_tecutil('DataAlterX', return_value=False):
            with self.assertRaises(TecplotSystemError):
                tp.data.operate.execute_equation('X')

    def test_default_options(self):
        # noinspection PyStatementEffect
        def fake_data_alter(arglist):
            for option in [sv.ZONESET, sv.IMIN, sv.JMIN, sv.JSKIP,
                           sv.JMIN, sv.JMAX, sv.JSKIP,
                           sv.KMIN, sv.KMAX, sv.KSKIP,
                           sv.VALUELOCATION,
                           sv.VARDATATYPE,
                           sv.IGNOREDIVIDEBYZERO]:
                with self.assertRaises((TypeError, KeyError)):
                    # Accessing the option should raise a TypeError
                    # since that option should not exist in the incoming
                    # arglist.
                    arglist[option]
            return True

        with patch_tecutil('DataAlterX', side_effect=fake_data_alter):
            tp.data.operate.execute_equation('X')

    # noinspection PyUnresolvedReferences
    def test_all_execute_equation_options(self):
        equation = 'X = X + 1'
        zone_list = [self.z_inner]
        i_range = (2, 3, 4)
        j_range = (5, 6, 7)
        k_range = (8, 9, 10)

        value_location = ValueLocation.Nodal
        variable_data_type = FieldDataType.Byte
        ignore_divide_by_zero = True

        def fake_data_alter(arglist):
            self.assertIsInstance(arglist, tecutil.ArgList)

            self.assertEqual(arglist[sv.EQUATION], equation)

            zones = [Z for Z in arglist[sv.ZONESET]]
            self.assertTrue(self.z_inner.index in zones)

            self.assertEqual(arglist[sv.IMIN], i_range[0])
            self.assertEqual(arglist[sv.IMAX], i_range[1])
            self.assertEqual(arglist[sv.ISKIP], i_range[2])
            self.assertEqual(arglist[sv.JMIN], j_range[0])
            self.assertEqual(arglist[sv.JMAX], j_range[1])
            self.assertEqual(arglist[sv.JSKIP], j_range[2])
            self.assertEqual(arglist[sv.KMIN], k_range[0])
            self.assertEqual(arglist[sv.KMAX], k_range[1])
            self.assertEqual(arglist[sv.KSKIP], k_range[2])

            self.assertEqual(ValueLocation(arglist[sv.VALUELOCATION]),
                             ValueLocation.Nodal)

            self.assertEqual(FieldDataType(arglist[sv.VARDATATYPE]),
                             FieldDataType.Byte)

            self.assertTrue(arglist[sv.IGNOREDIVIDEBYZERO])

            return True

        with patch_tecutil('DataAlterX', side_effect=fake_data_alter):
            tp.data.operate.execute_equation(
                equation,
                zones=zone_list,
                i_range=i_range,
                j_range=j_range,
                k_range=k_range,
                value_location=value_location,
                variable_data_type=variable_data_type,
                ignore_divide_by_zero=ignore_divide_by_zero)

    def test_execute_equation(self):
        self.assertTrue(np.allclose(list(self.z_var[:]), [0, 0, 0, 0]))
        tp.data.operate.execute_equation('{Z} = 1', zones=self.z_inner)
        self.assertTrue(np.allclose(list(self.z_var[:]), [1, 1, 1, 1]))

    def test_invalid_equation_parameter(self):
        if __debug__:
            with self.assertRaises(TecplotTypeError):
                # Requires a string
                tp.data.operate.execute_equation(1 + 1)

            with self.assertRaises(TecplotValueError):
                # Requires non-zero length string
                tp.data.operate.execute_equation('')
        else:
            with self.assertRaises((TecplotLogicError, TecplotSystemError)):
                # Requires a string
                tp.data.operate.execute_equation(1 + 1)

            with self.assertRaises(TecplotSystemError):
                # Requires non-zero length string
                tp.data.operate.execute_equation('')

    def test_invalid_zone_set_parameter(self):
        class ClassWithoutIndexMethod(object):
            def __init__(self):
                pass  # Fake class without an .index() method

        if __debug__:
            expected_error = TecplotTypeError
        else:
            expected_error = TecplotSystemError

        with self.assertRaises(TecplotTypeError):
            tp.data.operate.execute_equation(
                'X', zones=ClassWithoutIndexMethod())
        with self.assertRaises(TecplotTypeError):
            tp.data.operate.execute_equation(
                'X', zones=[ClassWithoutIndexMethod()])

    def test_zones_as_indices(self):
        self.z_inner.values('X')[1] = 3.1415
        self.assertFalse(np.allclose(self.z_inner.values('X')[:],
                                     self.z_inner.values('Y')[:]))
        tp.data.operate.execute_equation('X=Y', zones=self.z_inner.index)
        self.assertTrue(np.allclose(self.z_inner.values('X')[:],
                                    self.z_inner.values('Y')[:]))

        self.z_inner.values('X')[1] = 3.1415
        self.assertFalse(np.allclose(self.z_inner.values('X')[:],
                                     self.z_inner.values('Y')[:]))
        tp.data.operate.execute_equation('X=Y', zones=[self.z_inner.index])
        self.assertTrue(np.allclose(self.z_inner.values('X')[:],
                                    self.z_inner.values('Y')[:]))

    def test_zones_from_different_datasets(self):
        if __debug__:
            with self.assertRaises(TecplotValueError):
                self.z_inner.dataset.uid += 1  # Create different parent
                zone_list = [self.z_inner, self.z_outer]
                tp.data.operate.execute_equation('X = X + 1', zone_list)

    def test_range(self):
        with self.assertRaises(TypeError):
            tp.data.operate.execute_equation('X', i_range=1)
        with self.assertRaises(TypeError):
            tp.data.operate.execute_equation('X', j_range=2)
        with self.assertRaises(TypeError):
            tp.data.operate.execute_equation('X', k_range=3)
        with self.assertRaises(TecplotLogicError):
            tp.data.operate.execute_equation('X', i_range=(0, -1, -1))

    def test_valid_location_parameter(self):
        if __debug__:
            with self.assertRaises(TecplotTypeError):
                tp.data.operate.execute_equation('X', value_location=1)
            with self.assertRaises(TecplotTypeError):
                tp.data.operate.execute_equation(
                    'X', value_location=FieldDataType.Byte)
        else:
            with self.assertRaises(TecplotSystemError):
                tp.data.operate.execute_equation('X', value_location=1)
            with self.assertRaises((TecplotLogicError, TecplotSystemError)):
                tp.data.operate.execute_equation(
                    'X', value_location=FieldDataType.Byte)

    def test_variable_data_type(self):
        if __debug__:
            with self.assertRaises(TecplotTypeError):
                tp.data.operate.execute_equation('X', variable_data_type=1)

            with self.assertRaises(TecplotTypeError):
                tp.data.operate.execute_equation(
                    'X', variable_data_type=ValueLocation.Nodal)

    def test_ignore_divide_by_zero_param_type(self):
        if __debug__:
            with self.assertRaises(TecplotTypeError):
                tp.data.operate.execute_equation('X',
                                                 ignore_divide_by_zero='Yep!')
        else:
            with self.assertRaises((TecplotLogicError, TecplotSystemError)):
                tp.data.operate.execute_equation('X',
                                                 ignore_divide_by_zero='Yep!')

    def test_step_should_use_the_default_if_it_is_zero(self):
        # noinspection PyStatementEffect
        def fake_data_alter(arglist):
            # If skip is zero, then we should use the default
            with self.assertRaises((TypeError, KeyError)):
                arglist[sv.ISKIP]  # Should not exist (that is, use default)

            return True

        with patch_tecutil('DataAlterX', side_effect=fake_data_alter):
            tp.data.operate.execute_equation('X', i_range=(0, -1, 0))


class TestInterpolate(unittest.TestCase):

    def setUp(self):
        self.filename = sample_data.sample_data_file('3x3_2x2')

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_interpolate_linear(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filename)
        zouter = ds.zone('Rectangular zone outer')
        zinner = ds.zone('Rectangular zone inner')
        z = zinner.values('Z')
        self.assertTrue(np.allclose(list(z[:]), [0, 0, 0, 0]))
        tp.data.operate.interpolate_linear(zinner, zouter)
        self.assertTrue(np.allclose(list(z[:]), [.5, 1, 1, 1.5]))

    def test_interpolate_linear_source_zones(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filename)
        zouter = ds.zone('Rectangular zone outer')
        zinner = ds.zone('Rectangular zone inner')
        z = zinner.values('Z')
        self.assertTrue(np.allclose(list(z[:]), [0, 0, 0, 0]))
        tp.data.operate.interpolate_linear(zinner, source_zones=zouter.index)
        self.assertTrue(np.allclose(list(z[:]), [.5, 1, 1, 1.5]))

    def test_interpolate_linear_allzones(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filename)
        zinner = ds.zone('Rectangular zone inner')
        z = zinner.values('Z')
        self.assertTrue(np.allclose(list(z[:]), [0, 0, 0, 0]))
        tp.data.operate.interpolate_linear(zinner)
        self.assertTrue(np.allclose(list(z[:]), [.5, 1, 1, 1.5]))

    def test_failure(self):
        tp.new_layout()

        fr0 = tp.active_frame()
        ds0 = tp.data.load_tecplot(self.filename)
        zouter0 = ds0.zone('Rectangular zone outer')
        zinner0 = ds0.zone('Rectangular zone inner')

        with patch_tecutil('LinearInterpolate', return_value=False):
            with self.assertRaises(TecplotSystemError):
                tp.data.operate.interpolate_linear(zinner0, zouter0)

        fr1 = tp.active_page().add_frame()
        ds1 = tp.data.load_tecplot(self.filename)
        zouter1 = ds1.zone('Rectangular zone outer')
        zinner1 = ds1.zone('Rectangular zone inner')

        if __debug__:
            with self.assertRaises(TecplotLogicError):
                tp.data.operate.interpolate_linear(zinner0, zouter0)
            with self.assertRaises(TecplotLogicError):
                tp.data.operate.interpolate_linear(zinner1, zouter0)
            with self.assertRaises(TecplotLogicError):
                tp.data.operate.interpolate_linear(zinner0, zouter1)

            tp.data.operate.interpolate_linear(zinner1, zouter1)

            with self.assertRaises(TecplotLogicError):
                tp.data.operate.interpolate_linear(zinner1, zouter1,
                    variables=ds0.variable('Z'))

        tp.data.operate.interpolate_linear(zinner0, zouter0, plot=fr0.plot())

    def test_interpolate_linear_allopts(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filename)
        zouter = ds.zone('Rectangular zone outer')
        zinner = ds.zone('Rectangular zone inner')
        tp.active_frame().plot_type = PlotType.Sketch
        z = zinner.values('Z')
        self.assertTrue(np.allclose(list(z[:]), [0, 0, 0, 0]))
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            tp.data.operate.interpolate_linear(zinner, [zouter],
                ds.variable('Z'), fill_value=10,
                plot=tp.active_frame().plot(PlotType.Cartesian3D))
        self.assertEqual(tp.active_frame().plot_type, PlotType.Sketch)
        self.assertTrue(np.allclose(list(z[:]), [0, 0, 0, 0]))
        tp.data.operate.interpolate_linear(zinner.index, [zouter],
            ds.variable('Z'), fill_value=10,
            plot=tp.active_frame().plot(PlotType.Cartesian2D))
        self.assertTrue(np.allclose(list(z[:]), [.5, 1, 1, 1.5]))
        self.assertEqual(tp.active_frame().plot_type, PlotType.Sketch)
        tp.data.operate.interpolate_linear(zouter, [zinner],
            ds.variable('Z').index, fill_value=10,
            plot=tp.active_frame().plot(PlotType.Cartesian2D))
        z = zouter.values('Z')
        self.assertTrue(np.allclose(list(z[:]), [10.]*4 + [1.] + [10.]*4))
        self.assertEqual(tp.active_frame().plot_type, PlotType.Sketch)

    def test_krig(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filename)
        zouter = ds.zone('Rectangular zone outer')
        zinner = ds.zone('Rectangular zone inner')
        z = zinner.values('Z')
        self.assertTrue(np.allclose(list(z[:]), [0, 0, 0, 0]))
        tp.data.operate.interpolate_kriging(zinner, zouter)
        self.assertTrue(np.allclose(list(z[:]), [.5, 1, 1, 1.5]))

        tp.data.operate.interpolate_kriging(zinner, zouter, krig_range=0.8,
            zero_value=0.9, drift=Drift.None_,
            point_selection=PtSelection.NearestN, num_points=2)
        self.assertTrue(np.allclose(list(z[:]), [.25, .75, .75, 1.25]))

        with patch_tecutil('Krig', return_value=False):
            with self.assertRaises(TecplotSystemError):
                tp.data.operate.interpolate_kriging(zinner, zouter)

    def test_inverse_distance(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filename)
        zouter = ds.zone('Rectangular zone outer')
        zinner = ds.zone('Rectangular zone inner')
        z = zinner.values('Z')
        self.assertTrue(np.allclose(list(z[:]), [0, 0, 0, 0]))
        tp.data.operate.interpolate_inverse_distance(zinner, zouter)
        self.assertTrue(np.allclose(list(z[:]), [.5423286, 1, 1, 1.45767138]))

        tp.data.operate.interpolate_inverse_distance(zinner, zouter,
            exponent=2., min_radius=0.3, point_selection=PtSelection.All,
            num_points=100)
        self.assertTrue(np.allclose(list(z[:]),
            [0.656108597, 1., 1., 1.3438914027]))

        with patch_tecutil('InverseDistInterpolation', return_value=False):
            with self.assertRaises(TecplotSystemError):
                tp.data.operate.interpolate_inverse_distance(zinner, zouter)


class TestSmooth(unittest.TestCase):
    def test_smooth(self):
        plot = sample_data.create_ordered_3d()
        ds = plot.frame.dataset
        s = ds.zone(0).values('s')
        sbefore = s[:]
        tp.data.operate.smooth(s)
        safter = s[:]
        self.assertFalse(np.allclose(sbefore, safter))

    def test_smooth_arguments(self):
        plot = sample_data.create_ordered_3d()
        fr = plot.frame
        tp.active_page().add_frame()
        ds = fr.dataset
        s = ds.zone(0).values('s')
        sbefore = s[:]
        tp.data.operate.smooth(s, num_passes=2, weight=0.4,
           boundary_condition=BoundaryCondition.ZeroGradient, frame=fr)
        safter = s[:]
        self.assertFalse(np.allclose(sbefore, safter))

    def test_failure(self):
        plot = sample_data.create_ordered_3d()
        ds = plot.frame.dataset
        s = ds.zone(0).values('s')
        with patch_tecutil('Smooth', return_value=False):
            with self.assertRaises(TecplotSystemError):
                tp.data.operate.smooth(s)


class TestTransformCoordinates(unittest.TestCase):
    def setUp(self):
        self.filename = sample_data.sample_data_file('3x3x3_p')

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_transform_polar_to_rectangular(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filename)
        tp.active_frame().plot(PlotType.Cartesian2D).activate()

        x, y = ds.variable('x'), ds.variable('y')
        self.assertAllClose(x.values(0)[:6], [0, .5, 1, 0, .5, 1])
        self.assertAllClose(y.values(0)[:6], [0, 0, 0, .5, .5, .5])

        tp.data.operate.transform_rectangular_to_polar(x, y)
        theta, r = ds.variable(-2), ds.variable(-1)
        self.assertAllClose(r.values(0)[:6], [0, .5, 1, 0.5, 0.70710677, 1.118034])
        self.assertAllClose(theta.values(0)[:6], [0. , 0. , 0. , 1.570796, 0.785398, 0.463648])

        tp.data.operate.transform_polar_to_rectangular(r, theta)
        xx, yy = ds.variable(-2), ds.variable(-1)
        self.assertAllClose(xx.values(0)[:6], [0, .5, 1, 0, .5, 1])
        self.assertAllClose(yy.values(0)[:6], [0, 0, 0, .5, .5, .5])

        tp.data.operate.transform_rectangular_to_polar(xx, yy, r, theta,
            angle_units=AngleUnits.Degrees)
        self.assertAllClose(r.values(0)[:6], [0, .5, 1, 0.5, 0.70710677, 1.118034])
        self.assertAllClose(theta.values(0)[:6], [0, 0, 0, 90, 45, 26.565052])

        tp.data.operate.transform_polar_to_rectangular(r, theta, x, y,
            angle_units=AngleUnits.Degrees, zones=[0])
        self.assertAllClose(x.values(0)[:6], [0, .5, 1, 0, .5, 1])
        self.assertAllClose(y.values(0)[:6], [0, 0, 0, .5, .5, .5])

    def test_transform_spherical_to_rectangular(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filename)
        tp.active_frame().plot(PlotType.Cartesian3D).activate()

        x, y, z = ds.variable('x'), ds.variable('y'), ds.variable('z')
        self.assertAllClose(x.values(0)[:6], [0, .5, 1, 0, .5, 1])
        self.assertAllClose(y.values(0)[:6], [0, 0, 0, .5, .5, .5])
        self.assertAllClose(z.values(0)[:6], [0, 0, 0, 0, 0, 0])

        self.assertAllClose(x.values(0)[-6:], [0, .5, 1, 0, .5, 1])
        self.assertAllClose(y.values(0)[-6:], [0.5, 0.5, 0.5, 1. , 1. , 1. ])
        self.assertAllClose(z.values(0)[-6:], [1., 1., 1., 1., 1., 1.])

        tp.data.operate.transform_rectangular_to_spherical(x, y, z)
        theta, r, psi = ds.variable(-3), ds.variable(-2), ds.variable(-1)
        self.assertAllClose(r.values(0)[:6], [0. , 0.5 , 1. , 0.5 , 0.707107, 1.118034])
        self.assertAllClose(theta.values(0)[:6], [0. , 0. , 0. , 1.570796, 0.785398, 0.463648])
        self.assertAllClose(psi.values(0)[:6], [0. , 1.570796, 1.570796, 1.570796, 1.570796, 1.570796])

        self.assertAllClose(r.values(0)[-6:], [1.118034, 1.224745, 1.5 , 1.414214, 1.5 , 1.732051])
        self.assertAllClose(theta.values(0)[-6:], [1.570796, 0.785398, 0.463648, 1.570796, 1.107149, 0.785398])
        self.assertAllClose(psi.values(0)[-6:], [0.463648, 0.61548 , 0.841069, 0.785398, 0.841069, 0.955317])

        tp.data.operate.transform_spherical_to_rectangular(r, theta, psi)
        xx, yy, zz = ds.variable(-3), ds.variable(-2), ds.variable(-1)
        self.assertAllClose(xx.values(0)[:6], [0, .5, 1, 0, .5, 1])
        self.assertAllClose(yy.values(0)[:6], [0, 0, 0, .5, .5, .5])
        self.assertAllClose(zz.values(0)[:6], [0, 0, 0, 0, 0, 0])

        self.assertAllClose(xx.values(0)[-6:], [0, .5, 1, 0, .5, 1])
        self.assertAllClose(yy.values(0)[-6:], [0.5, 0.5, 0.5, 1. , 1. , 1. ])
        self.assertAllClose(zz.values(0)[-6:], [1, 1, 1, 1, 1, 1])

        tp.data.operate.transform_rectangular_to_spherical(xx, yy, zz, r, theta, psi,
        angle_units=AngleUnits.Degrees)
        self.assertAllClose(r.values(0)[:6], [0. , 0.5 , 1. , 0.5 , 0.707107, 1.118034])
        self.assertAllClose(theta.values(0)[:6], [0. , 0. , 0. , 90, 45, 26.565052])
        self.assertAllClose(psi.values(0)[:6], [0. ,90, 90, 90, 90, 90])

        self.assertAllClose(r.values(0)[-6:], [1.118034, 1.224745, 1.5 , 1.414214, 1.5 , 1.732051])
        self.assertAllClose(theta.values(0)[-6:], [90. , 45. , 26.565052, 90. , 63.43495 , 45. ])
        self.assertAllClose(psi.values(0)[-6:], [26.565052, 35.26439 , 48.189686, 45. , 48.189686, 54.73561 ])

        tp.data.operate.transform_spherical_to_rectangular(r, theta, psi, x, y, z,
        angle_units=AngleUnits.Degrees, zones=[0])
        self.assertAllClose(x.values(0)[:6], [0, .5, 1, 0, .5, 1])
        self.assertAllClose(y.values(0)[:6], [0, 0, 0, .5, .5, .5])
        self.assertAllClose(z.values(0)[:6], [0, 0, 0, 0, 0, 0])

        self.assertAllClose(x.values(0)[-6:], [0, .5, 1, 0, .5, 1])
        self.assertAllClose(y.values(0)[-6:], [0.5, 0.5, 0.5, 1. , 1. , 1. ])
        self.assertAllClose(z.values(0)[-6:], [1, 1, 1, 1, 1, 1])

    def test_determining_dataset_spherical(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filename)
        x, y, z = ds.variable('x'), ds.variable('y'), ds.variable('z')

        tp.data.operate.transform_rectangular_to_spherical(x.index, y.index, z.index)
        theta, r, psi = ds.variable(-3), ds.variable(-2), ds.variable(-1)
        self.assertAllClose(r.values(0)[:6], [0. , 0.5 , 1. , 0.5 , 0.707107, 1.118034])
        self.assertAllClose(theta.values(0)[:6], [0. , 0. , 0. , 1.570796, 0.785398, 0.463648])
        self.assertAllClose(psi.values(0)[:6], [0. , 1.570796, 1.570796, 1.570796, 1.570796, 1.570796])

        tp.data.operate.transform_rectangular_to_spherical(x.index, y.index, z.index, zones=[ds.zone(0)])
        theta, r, psi = ds.variable(-3), ds.variable(-2), ds.variable(-1)
        self.assertAllClose(r.values(0)[:6], [0. , 0.5 , 1. , 0.5 , 0.707107, 1.118034])
        self.assertAllClose(theta.values(0)[:6], [0. , 0. , 0. , 1.570796, 0.785398, 0.463648])
        self.assertAllClose(psi.values(0)[:6], [0. , 1.570796, 1.570796, 1.570796, 1.570796, 1.570796])

        tp.data.operate.transform_spherical_to_rectangular(r.index, theta.index, psi.index)
        xx, yy, zz = ds.variable(-3), ds.variable(-2), ds.variable(-1)
        self.assertAllClose(xx.values(0)[:6], [0, .5, 1, 0, .5, 1])
        self.assertAllClose(yy.values(0)[:6], [0, 0, 0, .5, .5, .5])
        self.assertAllClose(zz.values(0)[:6], [0, 0, 0, 0, 0, 0])

        tp.data.operate.transform_spherical_to_rectangular(r.index, theta.index, psi.index, zones=[ds.zone(0)])
        xx, yy, zz = ds.variable(-3), ds.variable(-2), ds.variable(-1)
        self.assertAllClose(xx.values(0)[:6], [0, .5, 1, 0, .5, 1])
        self.assertAllClose(yy.values(0)[:6], [0, 0, 0, .5, .5, .5])
        self.assertAllClose(zz.values(0)[:6], [0, 0, 0, 0, 0, 0])

    def test_determining_dataset_polar(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filename)
        x, y = ds.variable('x'), ds.variable('y')

        tp.data.operate.transform_rectangular_to_polar(x.index, y.index)
        theta, r = ds.variable(-2), ds.variable(-1)
        self.assertAllClose(r.values(0)[:6], [0. , 0.5 , 1. , 0.5 , 0.707107, 1.118034])
        self.assertAllClose(theta.values(0)[:6], [0. , 0. , 0. , 1.570796, 0.785398, 0.463648])

        tp.data.operate.transform_rectangular_to_polar(x.index, y.index, zones=[ds.zone(0)])
        theta, r = ds.variable(-2), ds.variable(-1)
        self.assertAllClose(r.values(0)[:6], [0. , 0.5 , 1. , 0.5 , 0.707107, 1.118034])
        self.assertAllClose(theta.values(0)[:6], [0. , 0. , 0. , 1.570796, 0.785398, 0.463648])

        tp.data.operate.transform_polar_to_rectangular(r.index, theta.index)
        xx, yy = ds.variable(-2), ds.variable(-1)
        self.assertAllClose(xx.values(0)[:6], [0, .5, 1, 0, .5, 1])
        self.assertAllClose(yy.values(0)[:6], [0, 0, 0, .5, .5, .5])

        tp.data.operate.transform_polar_to_rectangular(r.index, theta.index, zones=[ds.zone(0)])
        xx, yy = ds.variable(-2), ds.variable(-1)
        self.assertAllClose(xx.values(0)[:6], [0, .5, 1, 0, .5, 1])
        self.assertAllClose(yy.values(0)[:6], [0, 0, 0, .5, .5, .5])

    def test_failures(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filename)
        x, y, z, p = ds.variable('x'), ds.variable('y'), ds.variable('z'), ds.variable('p')
        with self.assertRaises(TecplotLogicError):
            tp.data.operate.transform_rectangular_to_polar(x, y, z)
        with self.assertRaises(TecplotLogicError):
            tp.data.operate.transform_polar_to_rectangular(x, y, z)
        with self.assertRaises(TecplotLogicError):
            tp.data.operate.transform_rectangular_to_spherical(x, y, z, p)
        with self.assertRaises(TecplotLogicError):
            tp.data.operate.transform_spherical_to_rectangular(x, y, z, p)
        with patch_tecutil('TransformCoordinatesX', return_value=False):
            with self.assertRaises((TecplotLogicError, TecplotSystemError)):
                tp.data.operate.transform_rectangular_to_polar(x, y)
            with self.assertRaises((TecplotLogicError, TecplotSystemError)):
                tp.data.operate.transform_polar_to_rectangular(x, y)
            with self.assertRaises((TecplotLogicError, TecplotSystemError)):
                tp.data.operate.transform_rectangular_to_spherical(x, y, z)
            with self.assertRaises((TecplotLogicError, TecplotSystemError)):
                tp.data.operate.transform_spherical_to_rectangular(x, y, z)


if __name__ == '__main__':
    from .. import main
    main()
