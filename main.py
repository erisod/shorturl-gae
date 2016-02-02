#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import cgi
import webapp2
from google.appengine.ext import ndb

class Redirect(ndb.Model):
    short = ndb.StringProperty()
    target = ndb.StringProperty()
    create_date = ndb.DateTimeProperty(auto_now_add=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):

        # TODO: Validate target URL against some rules.

        # TODO: Generate short url.
        shorturl = "1"

        newUrl = Redirect()
        newUrl.key
        newUrl.short = shorturl
        newUrl.id = shorturl
        newUrl.target = self.request.get('target')

        newUrl.put()
        
        self.response.write('http://domain.com/%s' % (newUrl.short))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
