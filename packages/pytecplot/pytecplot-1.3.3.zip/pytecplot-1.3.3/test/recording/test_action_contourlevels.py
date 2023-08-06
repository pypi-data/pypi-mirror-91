import re
import unittest

import tecplot as tp

from test import skip_if_connected, skip_if_sdk_version_before


class TestTranslateContourLevels(unittest.TestCase):
    @skip_if_sdk_version_before(2017, 3, 0, 81450)
    @skip_if_connected
    def setUp(self):
        tp.new_layout()

    def test_new(self):
        self.assertEqual(tp.macro.translate(
            "$!CONTOURLEVELS NEW\nRAWDATA 3 1.0 2.0 3.1"),
            "tp.active_frame().plot().contour(0).levels.reset_levels([1, 2, 3.1])")

        self.assertEqual(tp.macro.translate(
            "$!CONTOURLEVELS NEW CONTOURGROUP=8\nRAWDATA 3 1.0 2.0 3.1"),
            "tp.active_frame().plot().contour(7).levels.reset_levels([1, 2, 3.1])")

    def test_add(self):
        self.assertEqual(tp.macro.translate(
            "$!CONTOURLEVELS ADD\nRAWDATA 3 1.0 2.0 3.1"),
            "tp.active_frame().plot().contour(0).levels.add([1, 2, 3.1])")

    def test_no_raw_data(self):
        result = tp.macro.translate("""
$!CONTOURLEVELS RESETTONICE
CONTOURGROUP = 1
APPROXNUMVALUES = 12""")
        # No raw data, so should not have comments.
        self.assertNotIn('#', result)

    def test_reset(self):
        self.assertEqual(tp.macro.translate(
            "$!CONTOURLEVELS RESET\nNUMVALUES=15"),
            "tp.active_frame().plot().contour(0).levels.reset(num_levels=15)")

        self.assertEqual(tp.macro.translate(
            "$!CONTOURLEVELS RESET\nNUMVALUES=10"),
            "tp.active_frame().plot().contour(0).levels.reset()")

    def test_reset_to_nice(self):
        self.assertEqual(tp.macro.translate(
            "$!CONTOURLEVELS RESETTONICE\nAPPROXNUMVALUES=15"),
            "tp.active_frame().plot().contour(0).levels.reset_to_nice(num_levels=15)")

        self.assertEqual(tp.macro.translate(
            "$!CONTOURLEVELS RESETTONICE\nAPPROXNUMVALUES=10"),
            "tp.active_frame().plot().contour(0).levels.reset_to_nice()")

    def test_delete_range(self):
        self.assertIsNotNone(re.match(
            r"tp\.active_frame\(\)\.plot\(\)\.contour\(0\)\.levels\.delete_range\("
            r"min_value=0.1,\s*max_value=0.7\)",tp.macro.translate(
            "$!CONTOURLEVELS DELETERANGE\nRANGEMIN=0.1\nRANGEMAX=0.7"),
            re.MULTILINE))
