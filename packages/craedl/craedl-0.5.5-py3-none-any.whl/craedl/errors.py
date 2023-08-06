# Copyright 2019 The Johns Hopkins University
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

import json

class Connection_Refused_Error(Exception):
    def __init__(self):
        self.message = '''\n
Failed to establish a connection to https://api.craedl.org.
'''

    def __str__(self):
        return self.message

class Invalid_Token_Error(Exception):
    def __init__(self):
        self.message = '''\n
Your configured authentication token is invalid.
  (A) Configure your account through a system shell:
      `python -m craedl`
  (B) or configure your account through a Python interpreter:
      `import craedl; craedl.configure()`
'''

    def __str__(self):
        return self.message

class Missing_Token_Error(Exception):
    def __init__(self):
        self.message = '''\n
You have not configured an authentication token.
  (A) Configure your account through a system shell:
      `python -m craedl`
  (B) or configure your account through a Python interpreter:
      `import craedl; craedl.configure()`
'''

    def __str__(self):
        return self.message

class Not_Found_Error(Exception):
    def __init__(self):
        self.message = '''\n
The requested resource was not found.
'''

    def __str__(self):
        return self.message

class Other_Error(Exception):
    def __init__(self):
        self.message = '''\n
New error encountered. Determine the response error code and create a new error
class.
'''

    def __str__(self):
        return self.message

class Parse_Error(Exception):
    def __init__(self, details=None):
        self.message = '''\n
Your request included invalid parameters.
'''
        self.details = details

    def __str__(self):
        return self.message + ' ' + self.details

class Retry_Max_Error(Exception):
    def __init__(self, details=None):
        self.message = '''\n
Exceeded maximum number of retries. Check network connection.
'''

    def __str__(self):
        return self.message

class Server_Error(Exception):
    def __init__(self, details=None):
        self.message = '''\n
The server at https://api.craedl.org has encountered an error.
'''

    def __str__(self):
        return self.message

class Unauthorized_Error(Exception):
    def __init__(self):
        self.message = '''\n
You are not authorized to access the requested resource.
'''
