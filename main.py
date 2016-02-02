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

import webapp2
import shorten

class CreateHandler(webapp2.RequestHandler):
    def get(self):
        hostname = self.request.host
        target = self.request.get('target')
        # TODO: Validate target URL against some rules.

        # Normalize URL (e.g. add schema if missing, etc)
        if not "://" in target:
            target = "http://" + target

        short = shorten.createShortRandom(target)

        # Check it is stored correctly.
        new_target = shorten.getTarget(short)

        if new_target != target:
            self.response.write("<br>We have a problem.  Couldn't confirm storage.")
        else:
            short_url = "http://%s/%s" % (hostname, short)
            self.response.write('Your shortened URL : <b><a href="%s">%s</a><b>' 
                                % (short_url, short_url))


class RedirectHandler(webapp2.RequestHandler):
    def get(self):
        short = self.request.path[1:]
        target = shorten.getTarget(short)

        if target:
            # self.response.write('We'll redirect %s to %s' % (short, target))
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
