# -*- coding: utf-8 -*-
"""
:copyright: Copyright 2020 Sphinx Confluence Builder Contributors (AUTHORS)
:license: BSD-2-Clause (LICENSE)
"""

from sphinx.application import Sphinx
from sphinx.util.docutils import docutils_namespace
from sphinxcontrib.confluencebuilder.compat import input
from sphinxcontrib.confluencebuilder.config import process_ask_configs
from sphinxcontrib.confluencebuilder.logger import ConfluenceLogger as logger
from sphinxcontrib.confluencebuilder.publisher import ConfluencePublisher
from tempfile import TemporaryDirectory
import os
import sys

def wipe_main(args_parser):
    """
    wipe mainline

    The mainline for the 'wipe' action.

    Args:
        args_parser: the argument parser to use for argument processing

    Returns:
        the exit code
    """

    args_parser.add_argument('--danger', action='store_true')

    known_args = sys.argv[1:]
    args, unknown_args = args_parser.parse_known_args(known_args)
    if unknown_args:
        logger.warn('unknown arguments: {}'.format(' '.join(unknown_args)))

    work_dir = args.work_dir if args.work_dir else os.getcwd()

    # protection warning
    if not args.danger:
        print('')
        sys.stdout.flush()
        logger.warn('!!! DANGER DANGER DANGER !!!')
        print("""
A request has been made to attempt to wipe the pages from a configured
Confluence instance. This is a helper utility call to assist a user in cleaning
out a space since removing a bulk set of data may not be trivial for a user.

Note that this action is not reversible with this tool and may require
assistance from an administrator from a Confluence instance to recover pages.
Only use this action if you know what you are doing.

To use this action, the argument '--danger' must be set.
            """)
        sys.stdout.flush()
        logger.warn('!!! DANGER DANGER DANGER !!!')
        print('')
        return 1

    # check configuration and prepare publisher
    publisher = None
    with TemporaryDirectory() as tmp_dir:
        with docutils_namespace():
            app = Sphinx(
                work_dir,     # document sources
                work_dir,     # directory with configuration
                tmp_dir,      # output for generated documents
                tmp_dir,      # output for doctree files
                'confluence') # builder to execute

            aggressive_search = app.config.confluence_adv_aggressive_search
            server_url = app.config.confluence_server_url
            space_name = app.config.confluence_space_name

            # initialize the publisher (if permitted)
            if app.config.confluence_publish:
                process_ask_configs(app.config)

                publisher = ConfluencePublisher()
                publisher.init(app.config)

    if not publisher:
        print('(error) publishing not configured in sphinx configuration')
        return 1

    # reminder warning
    print('')
    sys.stdout.flush()
    logger.warn('!!! DANGER DANGER DANGER !!!')
    print("""
A request has been made to attempt to wipe the pages from a configured
Confluence instance.  This action is not reversible with this tool and may
require assistance from an administrator from a Confluence instance to recover
pages. Only use this action if you know what you are doing.
        """)
    sys.stdout.flush()

    logger.warn('!!! DANGER DANGER DANGER !!!')
    print('')

    if not ask_question('Are you sure you want to continue?'):
        return 0
    print('')

    # user has confirmed; start an attempt to wipe
    publisher.connect()

    if aggressive_search:
        legacy_pages = publisher.getDescendantsCompat(None)
    else:
        legacy_pages = publisher.getDescendants(None)
    if not legacy_pages:
        print('No pages are published on this space. Exiting...')
        return 0

    print('         URL:', server_url)
    print('       Space:', space_name)
    logger.note('       Pages: All Pages')
    print(' Total pages:', len(legacy_pages))
    print('')
    if not ask_question('Are you sure you want to REMOVE these pages?'):
        return 0
    print('')

    logger.info('Removing pages...', nonl=True)
    for page_id in legacy_pages:
        publisher.removePage(page_id)
        logger.info('.', nonl=True)
    logger.info(' done\n')

    return 0

def ask_question(question, default='no'):
    """
    ask the user a question

    The mainline for the 'wipe' action.

    Args:
        question: the question
        default (optional): the default state

    Returns:
        the users response to the question
    """

    if default is None:
        prompt = ' [y/n] '
    elif default == 'yes':
        prompt = ' [Y/n] '
    elif default:
        prompt = ' [y/N] '

    while True:
        rsp = input(question + prompt).strip().lower()
        if default is not None and rsp == '':
            return default == 'yes'
        elif rsp in ('y', 'yes'):
            return True
        elif rsp in ('n', 'no', 'q'): # q for 'quit'
            return False
        else:
            print("Please respond with 'y' or 'n'.\n")
