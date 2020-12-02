
# Copyright (C) 2013 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

import logging

from .base import Command

DEBUG_MODE = False
FUZZY_MATCHING = True

logger = logging.getLogger('autocomplete')


class AutoComplete(Command):
    """Return Jedi completions
    """

    def __init__(self, callback, uid, script):
        self.script = script
        super(AutoComplete, self).__init__(callback, uid)

    def run(self):
        """Run the command
        """

        try:
            # TODO: completions() is deprecated use complete
            completions = self.script.completions(fuzzy=FUZZY_MATCHING)
            if DEBUG_MODE is True:
                logger.info(completions)
            data = [
                ('{0}\t{1}'.format(comp.name, comp.type), comp.name)
                for comp in completions
            ]
            self.callback({
                'success': True, 'completions': data, 'uid': self.uid
            })
        except Exception as error:
            logger.exception('The underlying Jedi library as raised an exception')

            self.callback({
                'success': False, 'error': str(error), 'uid': self.uid
            })
