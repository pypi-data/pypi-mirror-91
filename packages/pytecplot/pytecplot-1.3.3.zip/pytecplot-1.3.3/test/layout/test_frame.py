from __future__ import unicode_literals, with_statement

import base64, collections, os, re, sys, tempfile, textwrap, zlib

from collections.abc import Iterable
from contextlib import contextmanager

import unittest
from .. import patch_tecutil, skip_if_sdk_version_before
from unittest.mock import patch, Mock

import tecplot as tp
import tecplot.plot
from tecplot.exception import *
from tecplot.constant import *
from tecplot.constant import TECUTIL_BAD_ID
from tecplot.tecutil import sv
from tecplot.annotation import Text
from tecplot.layout import Frame

from test import sample_data

_TECUTIL_VALID_ID = TECUTIL_BAD_ID + 1


if sys.version_info >= (3,):
    long = int


class TestFrames(unittest.TestCase):

    def test_activate_frame(self):
        with TestFrame.non_active_frame() as frame:
            self.assertFalse(frame.active)
            frame.activate()
            self.assertTrue(frame.active)

    def test_active_frame(self):
        tp.add_page()
        frame = tp.active_frame()
        self.assertIsInstance(frame, tp.layout.Frame)
        self.assertIsInstance(frame.uid, (int, long))
        self.assertGreater(frame.uid, 0)


class TestFrame(unittest.TestCase):
    @staticmethod
    @contextmanager
    def active_frame():
        page = tp.add_page()
        yield page.active_frame()

    @staticmethod
    @contextmanager
    def non_active_frame():
        page = tp.add_page()
        frame = page.active_frame()
        page.add_frame()
        yield frame

    @staticmethod
    @contextmanager
    def frames():
        page = tp.add_page()
        yield [page.active_frame(), page.add_frame()]

    def test___str__(self):
        with TestFrame.active_frame() as frame:
            frame.name = 'Test'
            self.assertEqual(str(frame), 'Frame: "Test"')

    def test___repr__(self):
        ptrn = re.compile(r'Frame\(uid=\d+, page=Page\(uid=\d+\)\)')
        with TestFrame.active_frame() as frame:
            self.assertRegex(repr(frame), ptrn)

    def test_aux_data(self):
        with self.active_frame() as frame:
            a = frame.aux_data
            self.assertIsInstance(a, tp.session.AuxData)
            a['test'] = 'test'
            self.assertEqual(a['test'], 'test')

    def test_position(self):
        with TestFrame.active_frame() as frame: # type: Frame
            old_position = tuple(frame.position)
            frame.position = (old_position[0] + 1, old_position[1] + 1)
            new_position = tuple(frame.position)
            self.assertAlmostEqual(new_position[0], old_position[0]+1)
            self.assertAlmostEqual(new_position[1], old_position[1]+1)

            frame.position = (old_position[0], None)
            self.assertAlmostEqual(frame.position.x, old_position[0])
            self.assertAlmostEqual(frame.position.y, new_position[1])

            frame.position = (None, old_position[1])
            self.assertAlmostEqual(frame.position.x, old_position[0])
            self.assertAlmostEqual(frame.position.y, old_position[1])

    def test_texts(self):
        with TestFrame.active_frame() as frame:
            txt = frame.add_text('abc')
            text_iterator = frame.texts()
            self.assertIsInstance(text_iterator, Iterable)
            self.assertEqual(len(list(text_iterator)), 1)
            frame.delete_text(txt)
            text_iterator = frame.texts()
            self.assertIsInstance(text_iterator, Iterable)
            self.assertEqual(len(list(text_iterator)), 0)

    def test_delete_text(self):
        with TestFrame.active_frame() as frame:
            self.assertFalse(list(frame.texts()))  # No texts by default
            text = frame.add_text('abc')
            text.angle = 0.1
            self.assertEqual(len(list(frame.texts())), 1)  # One text
            frame.delete_text(text)  # Delete the only text
            self.assertFalse(list(frame.texts()))  # No texts

            # Should throw if a property is accessed
            with self.assertRaises((TecplotSystemError, TecplotLogicError)):
                text.angle = 0.0

    @skip_if_sdk_version_before(2017, 3, msg='LaTeX images added to SDK in 2017.3')
    def test_add_latex(self):
        with TestFrame.active_frame() as fr:
            txt = fr.add_latex(r'$\alpha$ \\ $\beta$')
            self.assertIsInstance(txt, tp.annotation.Text)
            self.assertEqual(txt.type, TextType.LaTeX)
            txt.type = TextType.Regular
            self.assertEqual(txt.type, TextType.Regular)

    @skip_if_sdk_version_before(2018, 2, msg='georef images added to SDK in 2018.2')
    def test_add_geometries(self):
        with TestFrame.active_frame() as fr:
            image_ftmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            image_ftmp.write(base64.b64decode(sample_data.images['swoosh_png']))
            image_ftmp.close()

            world_ftmp = tempfile.NamedTemporaryFile(suffix='.pgw', mode='w+t', delete=False)
            # example world file numbers taken from
            # http://webhelp.esri.com/arcims/9.3/General/topics/author_world_files.htm
            world_ftmp.write(textwrap.dedent(r'''
                20.17541308822119
                0.00000000000000
                0.00000000000000
                -20.17541308822119
                424178.11472601280548
                4313415.90726399607956
            '''))
            world_ftmp.close()

            imgs = [
                fr.add_georeferenced_image(image_ftmp.name,
                                                world_ftmp.name),
                fr.add_image(image_ftmp.name, (0,0), 10),
                fr.add_image(image_ftmp.name, (1,1), 5),
            ]

            geoms = [
                fr.add_circle((0,0), 1, CoordSys.Grid),
                fr.add_ellipse((0,0), (1,1), CoordSys.Grid),
                fr.add_rectangle((0,0), (1,1), CoordSys.Frame),
                fr.add_square((0,0), 1, CoordSys.Frame),
                fr.add_polyline([[0,0], [1,2], [3,4]]),
                fr.add_polyline([[0,0,1], [1,2,3], [2,3,4]]),
                fr.add_polyline([[0,0], [1,2], [3,4]],
                                [[0,0], [1,2], [3,4]],
                                coord_sys=CoordSys.Frame),
                fr.add_polyline([[0,0,1], [1,2,3], [2,3,4]],
                                [[0,0,1], [1,2,3], [2,3,4]]),
            ]

        geometries = fr.geometries()
        for expected, item in zip(geoms, geometries):
            self.assertEqual(expected, item)
        with self.assertRaises(StopIteration):
            _ = next(geometries)

        images = fr.images()
        for expected, item in zip(imgs, images):
            self.assertEqual(expected, item)
        with self.assertRaises(StopIteration):
            _ = next(images)

    @skip_if_sdk_version_before(2018, 2, msg='georef images added to SDK in 2018.2')
    def test_delete_geometries(self):
        with TestFrame.active_frame() as fr:
            image_ftmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            image_ftmp.write(base64.b64decode(sample_data.images['swoosh_png']))
            image_ftmp.close()

            world_ftmp = tempfile.NamedTemporaryFile(suffix='.pgw', mode='w+t', delete=False)
            # example world file numbers taken from
            # http://webhelp.esri.com/arcims/9.3/General/topics/author_world_files.htm
            world_ftmp.write(textwrap.dedent(r'''
                20.17541308822119
                0.00000000000000
                0.00000000000000
                -20.17541308822119
                424178.11472601280548
                4313415.90726399607956
            '''))
            world_ftmp.close()

            imgs = [
                fr.add_georeferenced_image(image_ftmp.name,
                                                world_ftmp.name),
                fr.add_image(image_ftmp.name, (0,0), 10),
            ]

            geoms = [
                fr.add_circle((0,0), 1, CoordSys.Grid),
                fr.add_ellipse((0,0), (1,1), CoordSys.Grid),
                fr.add_polyline([[0,0], [1,2], [3,4]]),
            ]

        gm = geoms.pop(0)
        fr.delete_geometry(gm)
        gm = geoms.pop(-1)
        fr.delete_geometry(gm)
        im = imgs.pop(1)
        fr.delete_image(im)

        geometries = fr.geometries()
        for expected, item in zip(geoms, geometries):
            self.assertEqual(expected, item)
        with self.assertRaises(StopIteration):
            _ = next(geometries)

        images = fr.images()
        for expected, item in zip(imgs, images):
            self.assertEqual(expected, item)
        with self.assertRaises(StopIteration):
            _ = next(images)

    @skip_if_sdk_version_before(2018, 2, msg='georef images added to SDK in 2018.2')
    def test_geometries_add_failures(self):
        with TestFrame.active_frame() as fr:
            image_ftmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            image_ftmp.write(base64.b64decode(sample_data.images['swoosh_png']))
            image_ftmp.close()

            world_ftmp = tempfile.NamedTemporaryFile(suffix='.pgw', mode='w+t', delete=False)
            # example world file numbers taken from
            # http://webhelp.esri.com/arcims/9.3/General/topics/author_world_files.htm
            world_ftmp.write(textwrap.dedent(r'''
                20.17541308822119
                0.00000000000000
                0.00000000000000
                -20.17541308822119
                424178.11472601280548
                4313415.90726399607956
            '''))
            world_ftmp.close()

            with patch_tecutil('GeomImageCreate', return_value=0):
                with self.assertRaises(TecplotSystemError):
                    fr.add_image(image_ftmp.name, (1,1), 5)
            with patch_tecutil('GeoRefImageCreate', return_value=0):
                with self.assertRaises(TecplotSystemError):
                    fr.add_georeferenced_image(image_ftmp.name, world_ftmp.name)
            with patch_tecutil('GeomCircleCreate', return_value=0):
                with self.assertRaises(TecplotSystemError):
                    fr.add_circle((0,0), 1, CoordSys.Grid)
            with patch_tecutil('GeomEllipseCreate', return_value=0):
                with self.assertRaises(TecplotSystemError):
                    fr.add_ellipse((0,0), (1,1), CoordSys.Grid)
            with patch_tecutil('GeomRectangleCreate', return_value=0):
                with self.assertRaises(TecplotSystemError):
                    fr.add_rectangle((0,0), (1,1), CoordSys.Frame)
            with patch_tecutil('GeomSquareCreate', return_value=0):
                with self.assertRaises(TecplotSystemError):
                    fr.add_square((0,0), 1, CoordSys.Frame)
            with patch_tecutil('Geom2DMPolyCreate', return_value=0):
                with self.assertRaises(TecplotSystemError):
                    fr.add_polyline([[0,0], [1,2], [3,4]])
            with patch_tecutil('Geom3DMPolyCreate', return_value=0):
                with self.assertRaises(TecplotSystemError):
                    fr.add_polyline([[0,0,1], [1,2,3], [2,3,4]])
            with patch_tecutil('Geom2DMPolyCreate', return_value=0):
                with self.assertRaises(TecplotSystemError):
                    fr.add_polyline([[0,0], [1,2], [3,4]],
                                    [[0,0], [1,2], [3,4]],
                                    coord_sys=CoordSys.Frame)
            with patch_tecutil('Geom3DMPolyCreate', return_value=0):
                with self.assertRaises(TecplotSystemError):
                    fr.add_polyline([[0,0,1], [1,2,3], [2,3,4]],
                                    [[0,0,1], [1,2,3], [2,3,4]])

            with self.assertRaises(TecplotLogicError):
                fr.add_polyline([[0,0], [1,2], [2,3]],
                                [[0,0,1], [1,2,3], [2,3,4]])

            with self.assertRaises(IndexError):
                fr.add_polyline([[0,0,0], [1,2], [2,3]],
                                [[0,0,1], [1,2,3], [2,3,4]])

    def test_name(self):
        with TestFrame.active_frame() as frame:
            frame.name = 'Test'
            self.assertEqual(frame.name, 'Test')

    def test_dataset(self):
        with TestFrame.active_frame() as frame:
            self.assertIsInstance(frame.dataset, tp.data.Dataset)

    def test___eq__(self):
        f1a = tp.layout.Frame(1, tp.layout.Page(2))
        f1b = tp.layout.Frame(1, tp.layout.Page(2))
        f2 = tp.layout.Frame(2, tp.layout.Page(2))
        self.assertEqual(f1a, f1b)
        self.assertNotEqual(f1a, f2)

    def test_plot_type(self):
        with TestFrame.active_frame() as frame:
            self.assertIsInstance(frame.plot_type, PlotType)
            with patch_tecutil(
                    'FrameSetPlotType',
                    return_value=SetValueReturnCode.ContextError1.value):
                with self.assertRaises(TecplotSystemError):
                    frame.plot_type = PlotType.Cartesian3D

    def test_move(self):
        with TestFrame.active_frame() as frame:
            self.assertIsNone(frame.move_to_bottom())
            self.assertIsNone(frame.move_to_top())

    def test_background_color(self):
        frame = tp.active_frame()
        for val in [Color.Black, Color.Red]:
            frame.background_color = val
            self.assertEqual(frame.background_color, val)
        with self.assertRaises(ValueError):
            frame.background_color = 0.5

    def test_header_background_color(self):
        frame = tp.active_frame()
        for val in [Color.Black, Color.Red]:
            frame.header_background_color = val
            self.assertEqual(frame.header_background_color, val)
        with self.assertRaises(ValueError):
            frame.header_background_color = 0.5

    def test_border_thickness(self):
        frame = tp.active_frame()
        for val in [0.5, 0.1]:
            frame.border_thickness = val
            self.assertEqual(frame.border_thickness, val)
        with self.assertRaises(ValueError):
            frame.border_thickness = 'badtype'
        with self.assertRaises(TecplotSystemError):
            frame.border_thickness = 0

    def test_create_dataset(self):
        fr = tp.active_page().add_frame()
        with patch_tecutil('DataSetCreate', return_value=False):
            with self.assertRaises(TecplotSystemError):
                fr.create_dataset('D')
            with self.assertRaises(TecplotSystemError):
                fr.create_dataset('D', ['x'])
        ds = fr.create_dataset('D', ['x','y'])
        self.assertEqual(ds.variable(0).name, 'x')
        self.assertEqual(ds.variable(1).name, 'y')

        ds = fr.dataset
        self.assertEqual(ds.variable(0).name, 'x')
        self.assertEqual(ds.variable(1).name, 'y')

        ds = fr.create_dataset('D', ['a','b'])
        self.assertEqual(ds.variable(0).name, 'a')
        self.assertEqual(ds.variable(1).name, 'b')

        ds = fr.dataset
        self.assertEqual(ds.variable(0).name, 'a')
        self.assertEqual(ds.variable(1).name, 'b')

        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            _ = fr.create_dataset('D', ['x', 'y'], reset_style=False)

    def test_height(self):
        frame = tp.active_frame()
        frame.size_pos_units = FrameSizePosUnits.Paper
        h = frame.height
        for val in [20, h]:
            frame.height = val
            self.assertEqual(frame.height, val)
        with self.assertRaises(ValueError):
            frame.height = 'badtype'
        with self.assertRaises(TecplotSystemError):
            frame.height = 0

    def test_show_border(self):
        frame = tp.active_frame()
        for val in [True, False]:
            frame.show_border = val
            self.assertEqual(frame.show_border, val)

    def test_show_header(self):
        frame = tp.active_frame()
        for val in [True, False]:
            frame.show_header = val
            self.assertEqual(frame.show_header, val)

    def test_size_pos_units(self):
        frame = tp.active_frame()
        for val in [FrameSizePosUnits.Paper,
                    FrameSizePosUnits.Workspace]:
            frame.size_pos_units = val
            self.assertEqual(frame.size_pos_units, val)
        with self.assertRaises(ValueError):
            frame.size_pos_units = 0.5

    def test_transparent(self):
        frame = tp.active_frame()
        for val in [True, False]:
            frame.transparent = val
            self.assertEqual(frame.transparent, val)

    def test_width(self):
        frame = tp.active_frame()
        frame.size_pos_units = FrameSizePosUnits.Paper
        w = frame.width
        for val in [20, w]:
            frame.width = val
            self.assertEqual(frame.width, val)
        with self.assertRaises(ValueError):
            frame.width = 'badtype'
        with self.assertRaises(TecplotSystemError):
            frame.width = 0

    def test_current(self):
        tp.new_layout()
        f1 = tp.active_frame()
        self.assertTrue(f1.current)

    def test_activation_failure(self):
        with patch_tecutil('FrameActivateByUniqueID', return_value=False):
            with self.assertRaises(TecplotSystemError):
                tp.new_layout()
                f1 = tp.active_frame()
                tp.active_page().add_frame()
                f1.activate()

    def test_plot_type_failure(self):
        with patch_tecutil('FrameSetPlotType',
                           return_value=SetValueReturnCode.ContextError1):
            with self.assertRaisesRegex(TecplotSystemError, 'no dataset attached to frame'):
                fr = tp.active_frame()
                fr.plot_type = PlotType.Cartesian3D
        with patch_tecutil('FrameSetPlotType', side_effect=TecplotSystemError):
            with patch_tecutil('DataSetIsAvailableForFrame', return_value=False):
                with self.assertRaisesRegex(TecplotSystemError, 'no dataset attached to frame'):
                    fr = tp.active_frame()
                    fr.plot_type = PlotType.Cartesian3D
            with patch_tecutil('DataSetIsAvailableForFrame', return_value=True):
                with self.assertRaises(TecplotSystemError):
                    fr = tp.active_frame()
                    fr.plot_type = PlotType.Cartesian3D
        with patch_tecutil('FrameSetPlotType',
                           return_value=SetValueReturnCode.ContextError2):
            with self.assertRaisesRegex(TecplotSystemError, "SetValueReturnCode.ContextError2"):
                fr = tp.active_frame()
                fr.plot_type = PlotType.Cartesian3D

    @skip_if_sdk_version_before(2019, 2, 0, 101193)
    def test_plot_type_without_zone(self):
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            fr = tp.active_frame()
            fr.create_dataset('Test', ['X','Y'])
            fr.plot_type = PlotType.Cartesian3D

    def test_plot(self):
        tp.new_layout()
        with sample_data.loaded_sample_data('3x3x3_p'):
            fr = tp.active_frame()
            fr.plot_type = PlotType.Cartesian3D
            self.assertIsInstance(fr.plot(PlotType.Cartesian3D),
                                  tp.plot.Cartesian3DFieldPlot)
            self.assertIsInstance(fr.plot(PlotType.Active),
                                  tp.plot.Cartesian3DFieldPlot)
            self.assertIsInstance(fr.plot(), tp.plot.Cartesian3DFieldPlot)

    def test_active_zones(self):
        tp.new_layout()
        # zones: Rectangular3D, Rectangular2D, Line, Cylinder
        with sample_data.loaded_sample_data('4zones') as dataset:
            fr = tp.active_frame()
            names = [z.name for z in fr.active_zones()]
            self.assertEqual(len(names), 4)
            self.assertEqual(names, ['Rectangular3D', 'Rectangular2D',
                                     'Line', 'Cylinder'])
            fr.active_zones(*dataset.zones('Rectangular*'))
            names = [z.name for z in fr.active_zones()]
            self.assertEqual(len(names), 2)
            self.assertEqual(names, ['Rectangular3D', 'Rectangular2D'])

    def test_activate(self):
        fr = tp.active_frame()
        self.assertEqual(fr, tp.active_frame())
        fr.activate()
        self.assertEqual(fr, tp.active_frame())
        tp.active_page().add_frame()
        self.assertNotEqual(fr, tp.active_frame())
        fr.page = None
        fr.activate()
        self.assertEqual(fr, tp.active_frame())

    def test_activated(self):
        fr0 = tp.active_frame()
        fr1 = tp.active_page().add_frame()
        self.assertEqual(fr1, tp.active_frame())
        with fr0.activated():
            self.assertEqual(fr0, tp.active_frame())
        self.assertEqual(fr1, tp.active_frame())
        with patch('tecplot.layout.frame.Frame.activate',
                   Mock(side_effect=Exception)):
            self.assertEqual(fr1, tp.active_frame())
            try:
                with fr0.activated():
                    assert False
                assert False
            except:
                pass
            self.assertEqual(fr1, tp.active_frame())

        fr = tp.active_frame()
        page = tp.add_page()
        page.add_frame()
        self.assertNotEqual(fr, tp.active_frame())
        with fr.activated():
            self.assertEqual(fr, tp.active_frame())
        self.assertNotEqual(fr, tp.active_frame())


    @skip_if_sdk_version_before(2017, 3)
    def test_load_stylesheet(self):
        data = textwrap.dedent('''\
            #!MC 1410
            $!PlotType  = Cartesian3D
            $!FrameLayout
              ShowHeader = No
              BackgroundColor = Black
            $!GlobalContour  1
              Var = 4
              ColorMapName = 'Modern'
            $!FieldMap  [1]
              Surfaces
                {
                SurfacesToPlot = ExposedCellFaces
                }
            $!FieldLayers
              ShowMesh = No
              ShowContour = Yes''')

        fsty = tempfile.NamedTemporaryFile(suffix='.sty', delete=False)
        try:
            fsty.write(data.encode())
            fsty.close()

            tp.new_layout()
            with sample_data.loaded_sample_data('3x3x3_p'):
                tp.active_frame().load_stylesheet(fsty.name)

                plot = tp.active_frame().plot()
                self.assertIsInstance(plot, tp.plot.Cartesian3DFieldPlot)
                self.assertTrue(plot.show_contour)
                self.assertFalse(plot.show_mesh)

                self.assertEqual(plot.contour(0).colormap_name, 'Modern')  # BOOM!

                # indent whole stylesheet to make it pass the
                # pre processor but not the stylesheet reader
                with open(fsty.name, 'w') as f:
                    f.write(r'\n    '+data.replace('\n','\n    '))

                with self.assertRaises(TecplotSystemError):
                    tp.active_frame().load_stylesheet(fsty.name)

                # will fail the pre processor
                with open(fsty.name, 'wt') as f:
                    f.write('#!MC 1410\n$!bad command')

                with self.assertRaises((TecplotLogicError, TecplotSystemError)):
                    tp.active_frame().load_stylesheet(fsty.name)

        finally:
            os.remove(fsty.name)

    @skip_if_sdk_version_before(2017, 3)
    def test_save_stylesheet(self):
        data = textwrap.dedent('''\
            #!MC 1410
            $!PlotType  = Cartesian3D
            $!FrameLayout
              ShowHeader = No
              BackgroundColor = Black
            $!GlobalContour  1
              Var = 4
              ColorMapName = 'Modern'
            $!FieldMap  [1]
              Surfaces
                {
                SurfacesToPlot = ExposedCellFaces
                }
            $!FieldLayers
              ShowMesh = No
              ShowContour = Yes''')

        fsty = tempfile.NamedTemporaryFile(suffix='.sty', delete=False)
        try:
            fsty.write(data.encode())
            fsty.close()

            tp.new_layout()
            with sample_data.loaded_sample_data('3x3x3_p'):
                frame = tp.active_frame()
                frame.load_stylesheet(fsty.name)

                fstycopy = tempfile.NamedTemporaryFile(suffix='.sty', delete=False)
                fstycopy.close()
                frame.save_stylesheet(fstycopy.name)

                with open(fstycopy.name) as f:
                    datacopy = f.read().upper()

                    self.assertRegex(datacopy, "\$\!PlotType  = Cartesian3D".upper())
                    self.assertRegex(datacopy, "ColorMapName = 'Modern'".upper())
                    self.assertRegex(datacopy, "ShowMesh = No".upper())
                    self.assertRegex(datacopy, "ShowContour = Yes".upper())

                with patch_tecutil('WriteStylesheetX', return_value=False):
                    with self.assertRaises(TecplotSystemError):
                        frame.save_stylesheet(fstycopy.name)

        finally:
            os.remove(fsty.name)
            os.remove(fstycopy.name)


class TestAddText(unittest.TestCase):
    def setUp(self):
        self.frame = tp.active_frame()

    def test_add_text_returns_correct_object(self):
        text = self.frame.add_text('abc')
        self.assertIsInstance(text, Text)

    def test_invalid_arg_types(self):
        if __debug__:
            frame = self.frame
            with self.assertRaises(TecplotTypeError):
                frame.add_text(text=3)
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', position='a')
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', coord_sys=3)
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', typeface=0)
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', bold=0.0)
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', italic=2.0)
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', size='a')
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', angle='a')
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', line_thickness='a')
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', size_units='a')
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', margin='a')
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', box_color=3)
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', color=0)
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', fill_color=0)
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', box_type=0)
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', box_type=False)
            with self.assertRaises(AttributeError):
                frame.add_text('', zone=0)
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', anchor='a')
            with self.assertRaises(AttributeError):
                frame.add_text('', zone=False)

    @patch('tecplot.data.OrderedZone')
    @patch('tecplot.plot.XYLinemap')
    def test_valid_arg_types(self, xy_map, zone):
        if __debug__:
            # Overwrite the auto-created magic mocks for the .index properties
            # with simple int's so they can be correctly incremented.
            zone.index = 0
            xy_map.index = 0
            with patch_tecutil('TextCreateX'):
                try:
                    frame = self.frame
                    frame.add_text(text='a')
                    frame.add_text('', position=(1, 2))
                    frame.add_text('', coord_sys=CoordSys.Grid)
                    frame.add_text('', typeface='a')
                    frame.add_text('', bold=True)
                    frame.add_text('', italic=True)
                    frame.add_text('', size=3)
                    frame.add_text('', angle=1)
                    frame.add_text('', line_thickness=2.0)
                    frame.add_text('', margin=1.3)
                    frame.add_text('', box_color=Color.Custom1)
                    frame.add_text('', color=Color.Custom2)
                    frame.add_text('', fill_color=Color.Custom3)
                    frame.add_text('', box_type=TextBox.Filled)
                    frame.add_text('', anchor=TextAnchor.HeadCenter)
                    frame.add_text('', size_units=Units.Grid)
                    frame.add_text('', zone=zone)
                    frame.add_text('', zone=xy_map)
                except TecplotTypeError:
                    self.fail('unexpected TecplotTypeError exception was raised')

    @patch('tecplot.data.OrderedZone')
    def test_args_are_passed_to_tecutil(self, zone):
        position = (1.1, 2.2)
        zone.index = 0
        text = 'abc'
        arg_dict = {
            'coord_sys': (sv.POSITIONCOORDSYS, CoordSys.Grid),
            'bold': (sv.ISBOLD, True),
            'italic': (sv.ISITALIC, True),
            'size_units': (sv.SIZEUNITS, Units.Grid),
            'size': (sv.HEIGHT, 3.14),
            'angle': (sv.ANGLE, .314),
            'line_thickness': (sv.LINETHICKNESS, 1.2),
            'margin': (sv.MARGIN, 1.3),
            'anchor': (sv.ANCHOR, TextAnchor.HeadCenter),
            'line_spacing': (sv.LINESPACING, 1.5),
            'color': (sv.TEXTCOLOR, Color.Custom3),
            'box_color': (sv.COLOR, Color.Custom4),
            'fill_color': (sv.FILLCOLOR, Color.Custom8),
            'box_type': (sv.BOXTYPE, TextBox.Filled),
        }

        def fake_text_create(arglist):
            # Zone should pass through as index 1
            self.assertEqual(arglist[sv.ZONE], 1)
            self.assertTrue(arglist[sv.ATTACHTOZONE])

            # position should pass through as x,y
            self.assertEqual(arglist[sv.XPOS], position[0])
            self.assertEqual(arglist[sv.YPOS], position[1])

            # All others should pass though unchanged
            for value in arg_dict.values():
                sv_name = value[0]
                if isinstance(arglist, tp.tecutil.LocalArgList):
                    sv_value = value[1]
                else:
                    sv_value = value[1].value if hasattr(value[1], 'value') else value[1]
                self.assertEqual(arglist[sv_name], sv_value)

            return _TECUTIL_VALID_ID

        with patch_tecutil('TextCreateX', side_effect=fake_text_create):
            args = {k: v[1] for k, v in arg_dict.items()}
            # Add zone and position
            args['zone'] = zone
            args['position'] = position
            self.frame.add_text(text, **args)

    def test_default_args(self):
        # noinspection PyStatementEffect
        def fake_text_create(arglist):
            for option in [sv.POSITIONCOORDSYS,
                           sv.ISBOLD,
                           sv.ISITALIC,
                           sv.SIZEUNITS,
                           sv.HEIGHT,
                           sv.ANGLE,
                           sv.LINETHICKNESS,
                           sv.MARGIN,
                           sv.ANCHOR,
                           sv.LINESPACING,
                           sv.COLOR,
                           sv.TEXTCOLOR,
                           sv.FILLCOLOR,
                           sv.BOXTYPE,
                           sv.ZONE,
                           sv.XPOS,
                           sv.YPOS]:
                with self.assertRaises((TypeError, KeyError)):
                    # Accessing the option should raise a TypeError
                    # since that option should not exist in the incoming
                    # arglist.
                    arglist[option]

            return _TECUTIL_VALID_ID

        with patch_tecutil('TextCreateX', side_effect=fake_text_create):
            self.frame.add_text('abc')

    def test_invalid_return_value(self):
        with patch_tecutil('TextCreateX', return_value=TECUTIL_BAD_ID):
            with self.assertRaises(TecplotSystemError):
                self.frame.add_text('abc')

if __name__ == '__main__':
    from .. import main
    main()
