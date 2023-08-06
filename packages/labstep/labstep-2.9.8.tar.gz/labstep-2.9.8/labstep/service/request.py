#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Thomas Bullier <thomas@labstep.com>
# TODO Implement routing name
# Example: url = url_join(API_ROOT, "api/generic/share-link/email")

import requests
from labstep.service.helpers import url_join, handleError, getHeaders


class RequestService:
    def get(self, url, headers, params=None):
        response = requests.get(url, headers=headers, params=params, verify=False)
        handleError(response)
        return response

    def post(self, url, headers, json=None, files=None):
        response = requests.post(
            url, headers=headers, json=json, files=files, verify=False
        )
        handleError(response)
        return response

    def put(self, url, headers, json=None):
        response = requests.put(url, headers=headers, json=json, verify=False)
        handleError(response)
        return response

    def delete(self, url, headers, json=None):
        response = requests.delete(url, headers=headers, json=json, verify=False)
        handleError(response)
        return response


requestService = RequestService()
