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
#error_dictionary = {'USERNAME': '', 'PASSWORD': '', 'EMAIL': ''}
#error_list = ['', '', '']

def error_message(name_of_error):
    return "You didn't enter a valid %s.  Try again." % name_of_error

def valid_username(username):
    #if not (USER_RE.match(username) and username):
        #error_dictionary[USERNAME] = error_message('username')
    return USER_RE.match(username) and username

def valid_password(password, verify_password):
    #if not (PASS_RE.match(password) and password==verify_password and password):
        #error_dictionary[PASSWORD] = error_message('password')
    return PASS_RE.match(password) and password==verify_password and password

def valid_email(email):
    #if not EMAIL_RE.match(email):
        #error_dictionary[EMAIL] = error_message('email')
    return EMAIL_RE.match(email)

#error_dictionary = {'USERNAME': '', 'PASSWORD': '', 'EMAIL': ''}
#username_error = "You didn't enter a valid username.  Try again."
#password_error = "You didn't enter a valid password.  Try again."
#email_error = "You didn't enter a valid email.  Try again."

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
    def write_form(self):
        form = '''
        <form action = '/complete' method = 'post'>
            <label>
                Username
                <input type='text' name='username' />
                <div style="color: red; display: inline-block">{0}</div>
            </label>
            <br>
            <label>
                Password
                <input type='text' name='password' />
                <div style="color: red; display: inline-block">{1}</div>
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
                <div style="color: red; display: inline-block">{2}</div>
            </label>
            <br>
            <input type="submit" value="Submit Query">
        </form>
        '''

        username_error = self.request.get("username_error")
        password_error = self.request.get("password_error")
        email_error = self.request.get("email_error")

#        if username_error or password_error or email_error:
#            error_esc = cgi.escape(error_list), quote=True)
            #error_element = '<p class="error">' + error_esc + '</p>'
#            self.response.write(page_header + form.format(error_esc)+ page_footer)
#        else:
#            error_esc =('', '', '')
        self.response.write(page_header + form.format(username_error, password_error, email_error)+ page_footer)

#        self.response.write(page_header + form.format(error_esc)+ page_footer)

    def get(self):
        self.write_form()

#        main_content = form + '<br>' + error_element
#        content = page_header + main_content +  page_footer
#        self.response.write(page_header + (form.format(error_esc))+ page_footer)

class SignedUp(webapp2.RequestHandler):
    """ Handles requests coming in to '/signup'
        e.g. www.user-signup.com/add
    """
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify_password = self.request.get('verify_password')
        email = self.request.get('email')

        username_ok = valid_username(username)
        password_ok = valid_password(password, verify_password)
        email_ok = valid_email(email)

        if username_ok:
            username_error_message = ''
        else:
            username_error_message = error_message('username')

        if password_ok:
            password_error_message = ''
        else:
            password_error_message = error_message('password')

        if email_ok:
            email_error_message = ''
        else:
            email_error_message = error_message('email')

        #error_list = [usename_error_message, password_error_message, email_error_message]

        if not username_ok or not password_ok or not email_ok:
            self.redirect('/?username_error=' + username_error_message + '&password_error=' + password_error_message + '&email_error=' + email_error_message)

        congrats = 'Thanks for signing up!' + '<br>'
        self.response.write(congrats)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/complete', SignedUp)
], debug=True)
