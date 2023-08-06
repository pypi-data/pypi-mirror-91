Jupyter-OpenBIS-Extension
=========================

Requirements
------------

The jupyter-openbis-extension needs at least **Python 3.3** in order to
run. The Jupyter notebook server starts this extension during startup
and must therefore run under the same Python version. The kernel can be
anything (Python 2.7, Julia, R, Perl...)

This extension has been successfully tested with Safari 12.0.3, Chrome
72.0 and Firefox 66.0. There is a known incompatibility before Firefox
61.0b13.

Install the extension
---------------------

If you haven't done yet: download the latest jupyter-openbis-extension
from pip. It will automatically install the various dependencies, e.g.
Pandas and NumPy.

::

    pip install --upgrade jupyter-openbis-extension

Create a configuration file
---------------------------

This step is not really necessary, as you can define openBIS connections
within the Jupyter notebook. However, if you need to connect to the same
openBIS connections many times, this will become convenient. Create a
file ``openbis-connections.yaml``. It should contain connection
information to your server(s), for example:

::

    connections:
        - name                : TEST local openBIS instance
          url                 : https://localhost:8443
          verify_certificates : false
          username            : username
          password            : password
        - name                : PRODUCTION openBIS instance
          url                 : https://openbis.example.com
          verify_certificates : true
          username            : username

**Note 1**: You do not need neither username nor password. With the
current version, you are able to enter username and password directly
from within a Jupyter notebook.

**Note 2**: Place this file in any of these directories (on Mac OS X):

::

    /Users/your_username/jupyter-openbis-extension/notebooks
    /Users/your_username/.jupyter
    /Users/your_username/.pyenv/versions/3.6.0/etc/jupyter  # or wherever your jupyter installation is located
    /usr/local/etc/jupyter
    /etc/jupyter

These directories can be found by invoking

::

    $ jupyter --paths

The ``config`` section from the output lists the directories where your
``openbis-connections.yaml`` file should be placed.

install Jupyter extension manually
----------------------------------

In most cases, a simple
``pip install --upgrade jupyter-openbis-extension`` will do. However, in
some cases you need to issue the following commands to get the extension
running correctly:

::

    $ jupyter serverextension enable --py jupyter-openbis-extension
    $ jupyter nbextension install --py jupyter-openbis-extension --user
    $ jupyter nbextension enable --py jupyter-openbis-extension --user

If you want to install the extension globally, use ``--system`` instead
of ``--user``.

Launching Jupyter notebook
--------------------------

Now you are ready to launch Jupyter notebook:

::

    $ jupyter notebook --no-browser

Observe the terminal. It should tell you which server(s) have been
registered. If you provided a password, it will try to connect:

::

    $ jupyter notebook
    Registered: https://localhost:8443
    Successfully connected to: https://localhost:8443
    Registered: https://openbis.example.com

**Congratulations!** You can retry non-successful connections later,
directly from the GUI. Copy the the URL given in the output and paste it
in your browser. You might also just start Jupyter without the
``--no-browser`` option.

Uninstall Jupyter extension
---------------------------

::

    $ jupyter serverextension disable --py jupyter-openbis-extension
    $ jupyter nbextension disable --py jupyter-openbis-extension --user
    $ jupyter nbextension uninstall --py jupyter-openbis-extension --user

This should remove the registrations in the paths listed by the

::

    $ jupyter --paths

command.

Development with Vagrant
------------------------

If you want to use a predefined development environment, follow these
steps:

1. Install latest version of VirtualBox (https://www.virtualbox.org)

2. Install latest version of Vagrant
   (https://www.vagrantup.com/downloads.html)

3. vagrant plugin install vagrant-vbguest vagrant-notify-forwarder
   vagrant-disksize

4. cd vagrant

5. vagrant up

After the setup is complete, you'll have

-  Jupyter with openBIS extension running at http://localhost:8888.
-  openBIS running at https://localhost:8122/openbis/, with credentials
   admin/password.
-  Object /DEFAULT/DEFAULT with a lot of datasets for testing.

Hint: Jupyter creates no log file. Everything is printed onto the
console. In order to see this output do the following: 1. vagrant ssh 2.
screen -r

You can escape from the screen by typing ^A followed by ^D.

clone repository and install extension for development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ git clone git@sissource.ethz.ch:sispub/jupyter-openbis-extension.git
    $ cd jupyter-openbis-extension
    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ pip install -e .

The ``-e`` is a shortcut for ``--editable``. This means, it will only
establish a link to your source folder instead of copying the files.
When you do any modifications on the jupyter server extension (the
Python files) you need to restart Jupyter notebook in order to see the
changes.

If you make modifications on the UI (the Javascript files) you only need
to reload the page in order the see the effect.

How to extend Jupyter Notebooks is described
`here <https://jupyter-notebook.readthedocs.io/en/stable/extending/index.html>`__.
To distribute Jupyter Extensions, read this
`documentation <https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Distributing%20Jupyter%20Extensions%20as%20Python%20Packages.html#>`__
carefully.
