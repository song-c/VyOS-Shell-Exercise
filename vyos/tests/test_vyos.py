#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `VyosDriver`
"""

import unittest
#from ..src.driver import VyosDriver
from cloudshell.cli.session.ssh_session import SSHSession
from cloudshell.cli.service.cli import CLI
from cloudshell.cli.service.command_mode import CommandMode

class TestVyosDriver(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        pass


if __name__ == '__main__':
    import sys

    host = '192.168.51.126'
    username = 'vyos'
    password = input('Enter password for {}@{}: '.format(username, host))
    session = SSHSession(host=host, username=username, password=password)
    mode = CommandMode(r'.*$')
    cli = CLI()
    with cli.get_session([session], mode) as cli_service:
        out = cli_service.send_command('show interfaces')
        print(out)

    sys.exit(unittest.main())

