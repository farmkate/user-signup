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
import cgi
import re

USER_RE = re.compile( "^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

def error_message(specify):
    return "You didn't enter a valid {SPECIFY}".format(SPECIFY=specify)


page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <p>Signup</p>
    </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""


class MainHandler(webapp2.RequestHandler):
    def get(self):
        form = '''
        <form action = '/complete' method = 'post'>
            <label>
                Username
                <input type='text' name='username' />
            </label>
            <br>
            <label>
                Password
                <input type='text' name='password' />
            </label>
            <br>
            <label>
                Verify Password
                <input type='text' name='verify_password' />
            </label>
            <br>
            <label>
                Email (optional)
                <input type='text' name='email' />
            </label>
            <input type="submit" value="Submit Query">
        </form>
        '''

        error = self.request.get("error")
        if error:
            error_esc = cgi.escape(error, quote=True)
            error_element = '<p class="error">' + error_esc + '</p>'
        else:
            error_element = ''

        main_content = form + '<br>' + error_element
        content = page_header + main_content +  page_footer
        self.response.write(content)


class SignedUp(webapp2.RequestHandler):
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        email = self.request.get('email')

        if not username or not valid_username(username):
            self.redirect('/?error=' + error_message(username))

        congrats = 'Thanks for signing up!' + '<br>'
        self.response.write(congrats + username + password + email)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/complete', SignedUp)
], debug=True)
