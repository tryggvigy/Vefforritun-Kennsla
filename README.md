Vefforritun-Kennsla
===================

This repository contains tools created to help myself to grade students faster.

Using getmail.py
----------------

- Forward your emails to a gmail account.
- Put target emails into the starred folder.
- Make sure you have IMAP enabled in your gmail settings.
- Also make sure you change the access for settings for less secure apps to enabled:
- https://www.google.com/settings/security/lesssecureapps
- Run getmail.py.

getmail.py can not currently handle utf-8 strings in attatchment names. Pull requests are most wellcome.



sendmail.py
-----------

- Mass sends email to students containing grades and a review textfile.
- Emails and grades are fetched from an .ods file.
- Review is fetched from a directory with the same name as the email address.


unzip.sh
--------
- Can be run from getmail.py to automatically unzip email attachment zip files.


Stuff to come
--------------

- Documentation on how to structure the .ODS file and how to use sendmail.py.
- Grading proccess gulp tools like, validating html and css, jshint and more.


License
-------

####(The MIT License)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


_Tools in this repo only tested on Ubuntu 14.04._
