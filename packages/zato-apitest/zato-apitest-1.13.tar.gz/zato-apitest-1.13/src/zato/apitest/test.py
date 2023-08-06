# -*- coding: utf-8 -*-

"""
Copyright (C) Zato Source s.r.o. https://zato.io

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

# Part of Zato - Open-Source ESB, SOA, REST, APIs and Cloud Integrations in Python
# https://zato.io

# stdlib
from json import dumps

# lxml
from lxml import etree

# Requests
from requests_testadapter import Resp, TestAdapter

# six
from six import BytesIO

def xml_c14nize(data):
    """ Returns a canonical value of an XML document.
    """
    if not isinstance(data, etree._Element):
        data = etree.fromstring(data.encode('utf-8'))

    out = BytesIO()
    data.getroottree().write_c14n(out)
    value = out.getvalue()
    out.close()
    return value

class EchoAdapter(TestAdapter):
    def serialize(self, data):
        raise NotImplementedError('Needs to implemented in subclasses')

    def send(self, request, **kwargs):
        stream = self.serialize(dumps({
            'request': {
                'data': request.body,
                'headers': dict(request.headers)
            }
        }))

        resp = Resp(stream, self.status, self.headers)
        return self.build_response(request, resp)

class XMLEchoAdapter(EchoAdapter):
    def serialize(self, data):
        return '<response><![CDATA[{}]]></response>'.format(data).encode('utf-8')

class JSONEchoAdapter(EchoAdapter):
    def serialize(self, data):
        return dumps({'data': data.encode('utf-8')})
