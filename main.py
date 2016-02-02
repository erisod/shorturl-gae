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
import shorten
from google.appengine.ext import ndb

class CreateHandler(webapp2.RequestHandler):
    def get(self):
        hostname = self.request.host

        target = self.request.get('target')
        # TODO: Validate target URL against some rules.

        short = shorten.createShort(target)
        

        # Check it is stored correctly.
        newTarget = shorten.getTarget(short)

        if (newTarget != target):
            self.response.write("<br>We have a problem.  Couldn't confirm storage.")
        else:
            self.response.write('Your shortened URL : <b>http://%s/%s<b>' 
                % (hostname, short,))


class RedirectHandler(webapp2.RequestHandler):
    def get(self):

        host = self.request.host
        short = self.request.path[1:]

        target = shorten.getTarget(short)

        if target:
          # self.response.write('%s WILL REDIRECT to %s' % (short, target))
          self.redirect(str(target))
        else:
          self.response.write('Sorry, %s is not a registered URL' % (short))


class ListHandler(webapp2.RequestHandler):
    def get(self):
        all_shorts = shorten.getAll()
        for s in all_shorts:
          self.response.write('<br>%s --> %s' % (s.short, s.target))


app = webapp2.WSGIApplication([
    ('/newUrl', CreateHandler),
    ('/list', ListHandler),
    ('/.*', RedirectHandler)

], debug=True)
