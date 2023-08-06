Perform SOAP, REST and UI / Feature tests


Installation
============
You can download and install the latest version of this software from the Python package index (PyPI) as follows::

    pip install --upgrade testly

Usage
=====
    python -m testly --help=

    python -m testly --command <command> [Options]
or

`python -m testly -c <command> [Options]`

**Params**

Available commands  &nbsp; &nbsp; &nbsp; &nbsp; http, texecute

Test HTTP URL
=============

     python -m testly -c http -h <your_host>

**Params**

-h, --host &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  The Http host  that you desire to test.


**Optional Params**

--proxy &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp;  Sets Http proxy

--proxysec  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Sets Https proxy

Test REST Endpoint
=============

    python -m testly -c texecute -w <path to directory> -f <name of file>
    
or

`python -m testly -c texecute`

**Params**

-w &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; The directory containing all yaml files.

-f &nbsp;&nbsp;&nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; The yaml file containing all the test cases.

**YAML File Example Layout**

- *test1:
  testType: Rest
  requestMethod: get
  url: https://api.github.com/users/defunkt
  responseCode: 200
  bodyContains: 
    &nbsp;&nbsp;login: defunkt
    &nbsp;&nbsp;name: Chris Wanstrath*
    <br/>

- *test2:
  testType: Rest
  requestMethod: post
  url: https://testaroo.free.beeceptor.com/api/postTest/2
  responseCode: 200
  bodyContains: 
    &nbsp; &nbsp;status: Awesome!
    &nbsp;&nbsp; working: True*
     