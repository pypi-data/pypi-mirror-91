..
    This file is part of mailmanclient.

    mailmanclient is free software: you can redistribute it and/or modify it
    under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, version 3 of the License.

    mailmanclient is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
    or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
    License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with mailman.client.  If not, see <http://www.gnu.org/licenses/>.


==============
Mailman Client
==============

.. image:: https://gitlab.com/mailman/mailmanclient/badges/master/build.svg
    :target: https://gitlab.com/mailman/mailmanclient/commits/master

.. image:: https://readthedocs.org/projects/mailmanclient/badge
    :target: https://mailmanclient.readthedocs.io

.. image:: http://img.shields.io/pypi/v/mailmanclient.svg
    :target: https://pypi.python.org/pypi/mailmanclient

.. image:: http://img.shields.io/pypi/dm/mailmanclient.svg
    :target: https://pypi.python.org/pypi/mailmanclient

The ``mailmanclient`` library provides official Python bindings for the GNU
Mailman 3 REST API.


Requirements
============

``mailmanclient`` requires Python 3.5 or newer.


Documentation
=============

A `simple guide`_ to using the library is available within this package, in
the form of doctests.   The manual is also available online at:

    https://mailmanclient.readthedocs.io/en/latest/


Project details
===============

The project home page is:

    https://gitlab.com/mailman/mailmanclient

You should report bugs at:

    https://gitlab.com/mailman/mailmanclient/issues

You can download the latest version of the package either from the `Cheese Shop`_:

    http://pypi.python.org/pypi/mailmanclient

or from the GitLab page above.  Of course you can also just install it with
``pip`` from the command line::

    $ pip install mailmanclient

You can grab the latest development copy of the code using Git, from the Gitlab
home page above. If you have Git installed, you can grab your own branch of
the code like this::

    $ git clone https://gitlab.com/mailman/mailmanclient.git

You may contact the developers via mailman-developers@python.org


Acknowledgements
================

Many thanks to Florian Fuchs for his contribution of an initial REST
client. Also thanks to all the contributors of Mailman Client who have
contributed code, raised issues or devoted their time in any capacity!

.. _`simple guide`: https://mailmanclient.readthedocs.io/en/latest/src/mailmanclient/docs/using.html
.. _`Cheese Shop`: https://pypi.org/project/mailmanclient
