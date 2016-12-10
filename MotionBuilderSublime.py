"""SublimeText2/3 plugin for sending lines of code to MotionBuilder via
telnet.
"""
# ST2/ST3 compat
from __future__ import print_function
# Standard library
import re
import sys
import time
import socket
import textwrap
from telnetlib import Telnet
# Local
import sublime
import sublime_plugin


if sublime.version() < '3000':
    # we are on ST2 and Python 2.X
    _ST3 = False
else:
    _ST3 = True


# Our default plugin state
_settings = {
    'host': '127.0.0.1',
    'port': 4242,
    'strip_sending_comments': True,
    'no_collisions': True,
}


def settings_obj():
    return sublime.load_settings('MotionBuilderSublime.sublime-settings')


def sync_settings():
    so = settings_obj()
    _settings['host'] = so.get('motionbuilder_hostname')
    _settings['port'] = so.get('python_command_port')
    _settings['strip_comments'] = so.get('strip_sending_comments')
    _settings['no_collisions'] = so.get('no_collisions')


def telnet_write(command, host='127.0.0.1', port=4242):
    """Sends a block of code to MotionBuilder via Python's telnetlib.

    Example:
        command = "FBModelCube('TestCube1')"
        rsp = telnet_write(command)
        if rsp:print(rsp)
    """
    msg = '{0}\n'.format(command)
    print('SENDING: {0!r}'.format(msg))

    connection = Telnet(host, port)
    connection.read_until('>>>')
    connection.write(msg)

    response = connection.read_until('>>> ', .1)[:-6]
    response.replace('\r', '')

    connection.close()

    return str(response)


def _py_str(string):
    """Encode a py3 string if needed"""
    if _ST3:
        return string.encode(encoding='UTF-8')

    return string


def _send_to_motionbuilder(command, quiet=False):
    """Catch socket error for display in SublimeText error popup.
    
    Args:
        command (str): Command to be sent to MotionBuilder.
        quiet (bool): No popup.
    """
    try:
        rsp = telnet_write(_py_str(command))
        if rsp:print(rsp)
    except socket.error:
        host = _settings['host']
        port = _settings['port']
        e = sys.exc_info()[1]
        err = str(e)
        msg = 'Failed to communicate with MotionBuilder \
        ({host}:{port}):\n{err}'.format(**locals())
        if quiet:
            print(msg)
            return False

        sublime.error_message(msg)
        raise


# A template wrapper for sending Python source over telnet. 
# Note: No need to add any extra error catching here.
PY_CMD_TEMPLATE = '''{xtype}({cmd!r})'''


class send_to_motionbuilder(sublime_plugin.TextCommand):
    """
    API Docs:
        http://www.sublimetext.com/docs/2/api_reference.html#sublime.View
    """
    # Match single-line comments in Python.
    RX_COMMENT = re.compile(r'^\s*(#)')

    def run(self, edit):
        # Do we have a valid source language?
        syntax = self.view.settings().get('syntax')

        if re.search(r'python', syntax, re.I):
            lang = 'python'
            sep = '\n'
        else:
            print('No MotionBuilder-Recognized Language Found')
            return

        # Apparently ST3 doesn't always sync up its latest
        # plugin settings?
        if _settings['host'] is None:
            sync_settings()

        # Check the current number of separate selections to 
        # determine how we will send the source to be executed.
        region_set = self.view.sel()
        sel_size = 0
        for region in region_set:
            if not region.empty():
                sel_size += 1

        # If nothing is selected, we will use an approach that sends an
        # entire source file, and tell MotionBuilder to execute it.
        snips = []
        if sel_size == 0:
            exec_type = 'execfile'

            print('Nothing Selected, Attempting to exec entire file')

            if self.view.is_dirty():
                sublime.error_message('Save Changes Before MotionBuilder Source/Import')
                return

            file_path = self.view.file_name()
            if file_path is None:
                sublime.error_message('File must be saved before sending to MotionBuilder')
                return

            plat = sublime_plugin.sys.platform
            if plat == 'win32':
                file_path = file_path.replace('\\', '\\\\')
                print('FILE PATH:', file_path)

            snips.append(file_path)

        # Otherwise, we are sending snippets of code to be executed
        else:
            exec_type = 'exec'
            file_path = ''

            substr = self.view.substr
            match = self.RX_COMMENT.match
            stripComments = _settings['strip_comments']

            # Build up all of the selected lines, while removing single-line
            # comments to simplify the amount of data being sent.
            for region in region_set:
                if stripComments:
                    snips.extend(line for line in substr(region).splitlines() if not match(line))
                else:
                    snips.extend(substr(region).splitlines())
        cmd = str(sep.join(snips))
        if not cmd:
            return

        no_collide = _settings['no_collisions']
        opts = dict(xtype=exec_type, cmd=cmd, fp=file_path, ns=no_collide)
        mb_cmd = PY_CMD_TEMPLATE.format(**opts)

        print('Sending {0}:\n{1!r}\n...'.format(lang, mb_cmd[:200]))
        _send_to_motionbuilder(mb_cmd, quiet=False)


settings_obj().clear_on_change('MotionBuilderSublime.settings')
settings_obj().add_on_change('MotionBuilderSublime.settings', sync_settings)
sync_settings()
