
# Copyright (C) 2013 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

import logging

from .base import Command

logger = logging.getLogger('goto')


class FindUsages(Command):
    """Get back a python usages for the given object
    """
    # TODO (CEV): combine with Goto classes

    def __init__(self, callback, uid, script):
        self.script = script
        super(FindUsages, self).__init__(callback, uid)

    def _build_response(self, definitions):
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

    def _find_usages(self):
        usages = self.script.usages()
        if usages:
            return self._build_response(usages)
        raise RuntimeError('Can\'t find any usages')

    def run(self):
        """Run the command
        """
        try:
            usages = self._find_usages()
            success = True
        except Exception as error:
            usages = []
            success = False
            logger.exception('Usages')

        self.callback(
            {'success': success, 'result': usages, 'uid': self.uid})
