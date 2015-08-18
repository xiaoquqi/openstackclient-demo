#!/usr/bin/env python

from routes import Mapper

mapper = Mapper()
mapper.connect("versions", "/",
        controller="version",
        action="show",
        conditions={"method": ["GET"]})


mapper.resource("flavor", "flavors",
                controller="flavors",
                collection={"detail": "GET"},
                member={"action": "POST"})

mapper.resource("ip", "ips", controller="handle_ips",
                parent_resource=dict(member_name='server',
                                     collection_name='servers'))

print mapper
print "------------------------------------------"
print mapper.match('/')
print mapper.match('/flavors/13')
print mapper.match('/servers/1/ips')
