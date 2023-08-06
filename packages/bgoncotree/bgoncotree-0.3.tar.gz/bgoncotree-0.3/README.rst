
BGOncoTree
==========

.. |ot| replace:: **BGOncoTree**
.. |tree| replace:: *oncotree*

|ot| is a Python package to standardize the use of the OncoTree within the BBGLab.


Installation
------------

|ot| works with Python 3.5+ and can be installed with pip::

	pip install bgoncotree



Usage
-----

Any use of |ot| requires to initialize the tree:

.. code:: python

	from bgoncotree.main import BGOncoTree

	tree = BGOncoTree()

|ot| accepts a file as argument if you want to `provide your own tree`_.

Each node is composed by:

- ``id``: short identifier of the node (e.g. ``ALL``)
- ``parent``: ancestor node
- ``children``: list of descendent nodes
- ``synonyms``: list of alternative names that can be used to search for this node
- ``name``: first provided synonym or node id



Python
******

The first thing to do is **initialize** the *BGOncoTree* object:

.. code:: python

	tree = BGOncoTree()

The *BGOncoTree* object is a *dictionary* that you can query to **get
each node**:

.. code:: python

	node = tree['CANCER']

Using the ID of the node or any synonym you can ``find`` the node:

.. code:: python

	node = tree.find('clear cell sarcoma')


To **explore** the tree, you can use the ``iter_from`` method:

.. code:: python

	for node, level in tree.iter_from(tree['ALL'], descending=True):
		...

The `level` is simply an integer indicating the level of nested with respect
to the ``starting_node``.
If you want to explore the full tree, you can get the **root node** as:

.. code:: python

	root_node = tree.root


The methods ``descendants`` and ``ancestors`` do the same as ``iter_from``
but you do not need to indicate the ``descending`` flag, the ``level`` is not
returned and node can also be a string. E.g.:

.. code:: python

	for node in tree.descendants('ALL'):
		...


.. important:: `iter_from``, ``descendants`` and ``ancestors`` methods
   return the starting node.


There are two other methods that you can make use of.
``search`` can be used to **search** for all nodes containing a word
in their names. E.g.:

.. code:: python

	for node in tree.search('acute'):
		...

The ``get`` method is useful if you expect only one result from a search.
E.g.:

.. code:: python

	node = tree.get('Cholangiocarcinoma')

This method will raise an exception if none or more than 1 items are found.


Command line
************

The command line provides two utilities to explore the tree
``bgoncotree ancestors`` and ``bgoncotree descendants``.
Output can be formatted in json, and you can also set a recursion limit.

See first one level of childs of ``HEMATO`` node:

.. code:: bash

	bgoncotree descendants --node HEMATO --json --limit 2


In addition, the same ``search`` function as in Python can be called
from the command line as::

	bgoncotree search acute


Tab completion can be enabled adding
``eval "$(_BGONCOTREE_COMPLETE=source bgoncotree)"`` to your ``.bashrc``
file as explained in the
`bash completion section of Click <https://click.palletsprojects.com/en/7.x/bashcomplete/>`_



.. _provide your own tree:

Defining your own tree
----------------------

|ot| uses `bgdata <https://pypi.org/project/bgdata/>`_ to get the most recent
version of the |tree| used in the lab.
However, you can pass a file with your own |tree|::

	from bgoncotree.main import BGOncoTree

	tree = BGOncoTree(file)

If you are interested in creating your own |tree|,
you need a ``tsv`` file with 2 columns: ``ID`` and ``PARENT``.
Each node can only have 1 parent, and there must but one node without a
parent: the root node.

You can provide an additional extra column ``NAMES`` with a comma separated
list of synonyms for each node. The first name will be used as the
name to display.

You can **validate** your tree using the command line::

	bgoncotree validate my_tree.tsv




