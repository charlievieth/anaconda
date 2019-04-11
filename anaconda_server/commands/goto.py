
# Copyright (C) 2013 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

import logging

from .base import Command

logger = logging.getLogger('lint')


class Goto(Command):
    """Get back a python definition where to go
    """

    def __init__(self, callback, uid, script):
        self.script = script
        super(Goto, self).__init__(callback, uid)

    def _build_goto_response(self, definitions):
        if len(definitions) == 1:
            definition = definitions[0]
            if definition.in_builtin_module():
                raise RuntimeError('Can\' jump to builtin module')
            return [(definition.full_name,
                     definition.module_path,
                     definition.line,
                     definition.column + 1)]

        # TODO: do we need to filter out duplicates ???
        return [(i.full_name, i.module_path, i.line, i.column + 1)
                for i in definitions if not i.in_builtin_module()]

    def _goto_definition(self):
        definitions = self.script.goto_definitions()
        if definitions:
            return self._build_goto_response(definitions)
        raise RuntimeError('Can\'t jump to definition')

    def _goto_assignments(self):
        definitions = self.script.goto_assignments()
        if definitions:
            return self._build_goto_response(definitions)
        raise RuntimeError('Can\'t jump to assignment')

    def _get_definitions(self):
        try:
            return self._goto_definition()
        except Exception:
            return self._goto_assignments()

    def run(self):
        """Run the command
        """
        try:
            definitions = self._get_definitions()
            success = True
        except Exception as error:
            definitions = []
            success = False
            logger.exception('Failed to jump to definition or assignment')

        self.callback(
            {'success': success, 'result': definitions, 'uid': self.uid})


class GotoAssignment(Goto):
    """Get back a python assignment where to go
    """

    def _get_definitions(self):
        return self._goto_assignments()
