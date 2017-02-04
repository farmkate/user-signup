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
PASS_RE = re.compile("^.{3,20}$")
EMAIL_RE = re.compile("^[\S]+@[\S]+.[\S]+$")

def error_message(name_of_error):
    return "You didn't enter a valid %s.  Try again" % name_of_error

def password_match_error():
    return "Your passwords don't match"

def password_error():
    return "That's not a valid password"

def valid_username(username):
    return USER_RE.match(username) and username

def password_match(password, verify_password):
    return password==verify_password

def valid_password(password):
    return PASS_RE.match(password) and password

def valid_email(email):
    if email:
        return EMAIL_RE.match(email)
    else:
        return True

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

form = '''
<form action = '/' method = 'post'>
    <table>
        <tr>
            <td><label>Username</label></td>
            <td>
                <input type='text' name='username' value='{USERNAME_INPUT}'/>
                <div style="color: red; display: inline-block">{USERNAME_ERROR}</div>
            </td>
        </tr>
        <tr>
            <td><label>Password</label></td>
            <td>
                <input type='password' name='password' />
                <div style="color: red; display: inline-block">{PASSWORD_ERROR}</div>
            </td>
        <tr>
        <tr>
            <td><label>Verify Password</label></td>
            <td>
                <input type='password' name='verify_password' />
                <div style="color: red; display: inline-block">{PASSWORD_MATCH_ERROR}</div>
            </td>
        </tr>
        <tr>
            <td><label>Email (optional)<label></td>
            <td>
                <input type='text' name='email' value='{EMAIL_INPUT}'/>
                <div style="color: red; display: inline-block">{EMAIL_ERROR}</div>
            </td>
        </tr>
    </table>
    <input type="submit" value="Submit Query">
</form>
'''

class MainHandler(webapp2.RequestHandler):
    def get(self):
        username_error = ''
        password_error = ''
        password_match_error = ''
        email_error = ''

        username_input=''
        email_input=''

        esc_username = cgi.escape(username_input, quote=True)
        esc_email=cgi.escape(email_input, quote=True)

        self.response.write(page_header + form.format(USERNAME_ERROR=username_error, USERNAME_INPUT=esc_username, PASSWORD_ERROR=password_error, PASSWORD_MATCH_ERROR=password_match_error,  EMAIL_INPUT=esc_email, EMAIL_ERROR=email_error)+ page_footer)


    def post(self):
        username_input = self.request.get('username')
        password = self.request.get('password')
        verify_password = self.request.get('verify_password')
        email_input = self.request.get('email')

        username_ok = valid_username(username_input)
        password_match_ok = password_match(password, verify_password)
        password_ok = valid_password(password)
        email_ok = valid_email(email_input)

        username_error_message = ''
        password_error_message = ''
        password_match_error_message = ''
        email_error_message = ''

        if not username_ok:
            username_error_message = error_message('username')

        if not password_ok:
            password_error_message = password_error()

        if not password_match_ok:
            password_match_error_message = password_match_error()

        if not email_ok:
            email_error_message = error_message('email')

        esc_username = cgi.escape(username_input, quote=True)
        esc_email=cgi.escape(email_input, quote=True)

        if not username_ok or not password_ok or not password_match_ok or not email_ok:
            self.response.write(page_header + form.format(USERNAME_ERROR=username_error_message, USERNAME_INPUT=esc_username, PASSWORD_ERROR=password_error_message, PASSWORD_MATCH_ERROR=password_match_error_message,  EMAIL_INPUT=esc_email, EMAIL_ERROR=email_error_message)+ page_footer)
        else:
            self.redirect('/complete?username=' + esc_username)

class SignedUp(webapp2.RequestHandler):
    """ Handles requests coming in to '/signup'
        e.g. www.user-signup.com/add
    """
    def get(self):
        username_input = cgi.escape(self.request.get('username'), quote=True)
        congrats = '<h2>' + 'Welcome, ' + username_input + '!</h2>'
        self.response.write(congrats)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/complete', SignedUp)
], debug=True)
