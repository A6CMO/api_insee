#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

import api_insee.criteria as Criteria
from api_insee.conf import API_VERSION

__author__ = "Lenselle Nicolas"
__copyright__ = "Lenselle Nicolas"
__license__ = "mit"

base_siren_url = API_VERSION['url'] + API_VERSION['path_siren']


@pytest.mark.vcr
def test_request_first_pages(api):
    request = api.siren(
        Criteria.Raw('*')
    )

    pages = request.pages()
    first = next(pages)

    print(first['header'])

    assert first['header']['statut'] == 200
    assert first['header']['curseur'] == '*'
    assert first['header']['curseurSuivant']


@pytest.mark.vcr
def test_request_iterate_on_pages(api):
    request = api.siren(
        Criteria.Raw('*')
    )

    cursors = []

    for (index, page) in enumerate(request.pages()):
        cursors.append(page['header']['curseur'])
        if len(cursors) > 2:
            break

    assert cursors[0] != cursors[1] and cursors[1] != cursors[2]
