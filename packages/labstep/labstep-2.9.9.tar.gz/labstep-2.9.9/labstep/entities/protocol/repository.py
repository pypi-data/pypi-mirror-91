#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Barney Walker <barney@labstep.com>

from labstep.service.helpers import (
    getTime,
    createdAtFrom,
    createdAtTo,
    handleDate,
    listToClass,
)
from labstep.entities.protocol.model import Protocol
from labstep.entities.protocolVersion.model import ProtocolVersion
from labstep.generic.entity.repository import entityRepository


class ProtocolRepository:
    def getProtocol(self, user, protocol_id):
        return entityRepository.getEntity(user, Protocol, id=protocol_id)

    def getProtocols(
        self,
        user,
        count=100,
        search_query=None,
        created_at_from=None,
        created_at_to=None,
        tag_id=None,
        collection_id=None,
        extraParams={},
    ):
        params = {
            "search_query": search_query,
            "created_at_from": createdAtFrom(created_at_from),
            "created_at_to": createdAtTo(created_at_to),
            "tag_id": tag_id,
            "folder_id": collection_id,
            **extraParams,
        }
        return entityRepository.getEntities(user, Protocol, count, params)

    def newProtocol(self, user, name, extraParams={}):
        params = {"name": name, **extraParams}
        return entityRepository.newEntity(user, Protocol, params)

    def editProtocol(
        self, protocol, name=None, body=None, deleted_at=None, extraParams={}
    ):
        params = {"name": name, "deleted_at": deleted_at, **extraParams}

        if body is not None:
            entityRepository.editEntity(
                ProtocolVersion(protocol.last_version, protocol.__user__),
                {"state": body},
            )
            protocol.update()

        return entityRepository.editEntity(protocol, params)


protocolRepository = ProtocolRepository()
