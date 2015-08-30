Vefforritun-Kennsla
===================

This repository contains tools created to help myself to grade students faster.

Email utils
-----------
#### Dependencies
Recommended installation is with pip.
- odfpy (0.9.6)

### Directory structure
~~~
|-- getmail.py
|-- sendmail.py
|-- unzip.sh
|-- email_composer.py
|-- ... all the other python files
|-- verkefni1/
    |-- yfirferd.ods
    |-- YFIRFARID/
~~~
Let's say I have in my gmail account's starred folder an email from trg8
containing the zip file trg8.zip

Running the command:
~~~bash
python getmail.py --unseen --outdir verkefni1/
~~~
Will spit the zip file into verkefni1/ with the name 0__trg8.zip:
~~~
|-- verkefni1/
    |-- yfirferd.ods
    |-- YFIRFARID/
    |-- 0__trg8.zip
~~~
Next run:
~~~bash
bash unzip.sh
~~~
We get:
~~~
|-- verkefni1/
    |-- yfirferd.ods
    |-- YFIRFARID/
    |-- 10__trg8/
      |-- UMSOGN.txt
      |-- verkefnid/
~~~
The UMSOGN.txt file is generated by the script. The prefix numbers
(10__) are "unique" identifiers as many students WILL
turn in a .zip file named "verkefni" or something, especially for
the first few weeks.

OK. Once we have graded Mr. trg8 let's move his UMSOGN.txt into
a directory with his name and put it in the YFIRFARID/ directory.
10__trg8/ can now be deleted if you want.
~~~
|-- verkefni1/
    |-- yfirferd.ods
    |-- YFIRFARID/
        |-- trg8/
          |-- UMSOGN.txt
    |-- 10__trg8/
      |-- UMSOGN.txt
      |-- verkefnid/
~~~
Now let's email him his grades.
~~~bash
python sendmail.py --basedir verkefni/1 --subject "Yfirferð á verkefni 1 í vefforritun"
~~~
Running sendmail.py will read all students listed in the yfirferd.ods, compose an email with their grade and attach their
UMSOGN.txt file to the email.

#### Structure of the yfirferd.ods files
[yfirferd.ods](https://www.dropbox.com/s/sh941z8udnt294q/yfirferd.ods?dl=0)

This yfirferd.ods will send an email to trg8@hi.is. with the following email body:

~~~txt
SJÁ VIÐHENGI FYRIR UMSÖGNINA ÞÍNA!

Vefforritun	Verkefni 1

Upplýsingar um einkunnagjöf:
Snyrtilegt, vel inndegið, gilt HTML: 20.00%
Merkingarfræði og aðgengilegt HTML: 15.00%
Uppsetning á töflu: 15.00%
Uppsetning á formi: 15.00%
Uppsetning á textasíðu: 15.00%
Útlit útfært valmynd til hliðar við efni: 10.00%
Uppsetning á efni annarstaðar frá: 10.00%
Alls: 100.00%

====================== ÞÍNAR EINKUNNIR ======================
Nemandi: trg8
Snyrtilegt, vel inndegið, gilt HTML: 20.00%
Merkingarfræði og aðgengilegt HTML: 14.00%
Uppsetning á töflu: 10.00%
Uppsetning á formi: 11.00%
Uppsetning á textasíðu: 13.00%
Útlit útfært valmynd til hliðar við efni: 9.00%
Uppsetning á efni annarstaðar frá: 10.00%
Alls: 87.00%

Einkunn: 8.7
==============================================================

emailið er auto-generatað.
~~~

#### getmail.py
- Forward your emails to a gmail account.
- Put target emails into the starred folder.
- Make sure you have IMAP enabled in your gmail settings.
- Also make sure you change the access for settings for less secure apps to enabled:
- https://www.google.com/settings/security/lesssecureapps
- Run getmail.py.

getmail.py can not currently handle utf-8 strings in attatchment names. Pull requests are most welcome.



#### sendmail.py
- Mass sends email to students containing grades and a review textfile.
- Emails and grades are fetched from an .ods file.
- Review is fetched from a directory with the same name as the email address.


#### unzip.sh
- Mass unzip and create a folder for each file. Also generate an empty UMSOGN.txt for each .zip file.


Stuff to come
--------------
- Grading proccess gulp tools like, validating html and css, jshint and more.


License
-------
####(The MIT License)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


_Tools in this repo only tested on Ubuntu 14.04._
