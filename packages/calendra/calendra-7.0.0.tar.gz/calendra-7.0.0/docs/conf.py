#!/usr/bin/env python3
# -*- coding: utf-8 -*-

extensions = ['sphinx.ext.autodoc', 'jaraco.packaging.sphinx', 'rst.linker']

master_doc = "index"

link_files = {
    '../CHANGES.rst': dict(
        using=dict(
            GH='https://github.com',
            workalendar='https://github.com/peopledoc/workalendar/',
        ),
        replace=[
            dict(
                pattern=r'(Issue #|\B#)(?P<issue>\d+)',
                url='{package_url}/issues/{issue}',
            ),
            dict(
                pattern=r'(?m:^((?P<scm_version>v?\d+(\.\d+){1,2}))\n[-=]+\n)',
                with_scm='{text}\n{rev[timestamp]:%d %b %Y}\n',
            ),
            dict(
                pattern=r'PEP[- ](?P<pep_number>\d+)',
                url='https://www.python.org/dev/peps/pep-{pep_number:0>4}/',
            ),
            dict(
                pattern=r'\(#(?P<wk_issue>\d+)(.*?)\)',
                url='{workalendar}issues/{wk_issue}',
            ),
            dict(
                pattern=r'(?P<wk_ver>[Ww]orkalendar \d+\.\d+(\.\d+)?)',
                url='{workalendar}blob/master/Changelog.md',
            ),
        ],
    )
}
