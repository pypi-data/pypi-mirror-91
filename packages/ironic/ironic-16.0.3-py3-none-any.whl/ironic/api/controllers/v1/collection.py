# Copyright 2013 Red Hat, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from ironic import api
from ironic.api.controllers import base
from ironic.api.controllers import link
from ironic.api import types as atypes


def has_next(collection, limit):
    """Return whether collection has more items."""
    return len(collection) and len(collection) == limit


def get_next(collection, limit, url=None, key_field='uuid', **kwargs):
    """Return a link to the next subset of the collection."""
    if not has_next(collection, limit):
        return None

    fields = kwargs.pop('fields', None)
    # NOTE(saga): If fields argument is present in kwargs and not None. It
    # is a list so convert it into a comma seperated string.
    if fields:
        kwargs['fields'] = ','.join(fields)
    q_args = ''.join(['%s=%s&' % (key, kwargs[key]) for key in kwargs])

    last_item = collection[-1]
    # handle items which are either objects or dicts
    if hasattr(last_item, key_field):
        marker = getattr(last_item, key_field)
    else:
        marker = last_item.get(key_field)

    next_args = '?%(args)slimit=%(limit)d&marker=%(marker)s' % {
        'args': q_args, 'limit': limit,
        'marker': marker}

    return link.make_link('next', api.request.public_url,
                          url, next_args)['href']


class Collection(base.Base):

    next = str
    """A link to retrieve the next subset of the collection"""

    @property
    def collection(self):
        return getattr(self, self._type)

    @classmethod
    def get_key_field(cls):
        return 'uuid'

    def has_next(self, limit):
        """Return whether collection has more items."""
        return has_next(self.collection, limit)

    def get_next(self, limit, url=None, **kwargs):
        """Return a link to the next subset of the collection."""
        resource_url = url or self._type
        the_next = get_next(self.collection, limit, url=resource_url,
                            key_field=self.get_key_field(), **kwargs)
        if the_next is None:
            return atypes.Unset
        return the_next
