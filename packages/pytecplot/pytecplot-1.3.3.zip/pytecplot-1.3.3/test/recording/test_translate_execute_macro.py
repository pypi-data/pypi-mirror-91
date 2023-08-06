import unittest

import tecplot as tp

from test import skip_if_connected, skip_if_sdk_version_before


class TestTranslateExecuteMacro(unittest.TestCase):
    @skip_if_sdk_version_before(2017, 3, 0, 81450)
    @skip_if_connected
    def setUp(self):
        tp.new_layout()

    def check_result_is_comment(self, command):
        for line in tp.macro.translate(command).split('\n'):
            self.assertTrue(line.startswith('#'))

    def test_execute_invalid_macro_command(self):
        translated = tp.macro.translate(
            '$!INVALID_COMMAND')
        self.assertTrue(translated.startswith('#'))

    def test_execute_valid_macro_command(self):
        # $!PICK CUT will probably never exist in the pytecplot API
        translated = tp.macro.translate(
            '$!PICK CUT')
        self.assertFalse(translated.startswith('#'))
        self.assertIn('tp.macro.execute_command', translated)

    def test_commands_may_start_and_end_with_a_newline(self):
        # i.e., check that the translating engine trims the input
        # string.
        translated = tp.macro.translate(
            '\n$!CREATECIRCULARZONE \n  IMAX = 10\n  JMAX = 25\n  KMAX = 10\n')
        self.assertFalse(translated.startswith('#'))
        self.assertIn('tp.macro.execute_command', translated)

    def test_macro_command_strings_should_be_double_quoted(self):
        self.assertIn('"$!SYSTEM \'abc\'"', tp.macro.translate(r"$!SYSTEM 'abc'"))

    def test_invalid_macro_recorded_as_comment(self):
        self.check_result_is_comment('$!abc')

if __name__ == '__main__':
    from .. import main
    main()
