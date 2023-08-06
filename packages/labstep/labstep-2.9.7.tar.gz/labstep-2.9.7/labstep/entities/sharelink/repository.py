#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Barney Walker <barney@labstep.com>

from labstep.entities.sharelink.model import Sharelink
from labstep.generic.entity.repository import entityRepository


class ShareLinkRepository:
    def newSharelink(self, user, fields):
        return entityRepository.newEntity(user, Sharelink, fields)

    def getSharelink(self, entity):
        key = entity.__entityName__.replace("-", "_") + "_id"
        if entity.share_link is None:
            return self.newSharelink(entity.__user__, fields={key: entity.id})

        return Sharelink(entity.share_link, entity.__user__)


shareLinkRepository = ShareLinkRepository()
