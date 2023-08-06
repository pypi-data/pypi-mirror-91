#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Barney Walker <barney@labstep.com>

from labstep.service.htmlToProseMirror import htmlToProseMirrorService


def parseHTML(authenticatedUser, html):
    """
    Converts HTML into the JSON format used in protocols
    and experiment entries.

    Parameters
    ----------
    authenticatedUser (:)
        An authenticated Labstep :class:`~labstep.user.User`
        (see :func:`~labstep.user.authenticate`)
    html (str)
        HTML to be converted (as a string).
    """
    return htmlToProseMirrorService.parseHTML(authenticatedUser, html)
