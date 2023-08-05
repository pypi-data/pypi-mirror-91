# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mock_alchemy']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.22,<2.0.0', 'six>=1.15.0,<2.0.0']

setup_kwargs = {
    'name': 'mock-alchemy',
    'version': '0.1.0',
    'description': 'SQLAlchemy mock helpers.',
    'long_description': "===============\nMock SQLAlchemy\n===============\n.. image:: https://readthedocs.org/projects/mock-alchemy/badge/?version=latest\n    :target: https://mock-alchemy.readthedocs.io/en/latest/?badge=latest\n\n.. image:: https://img.shields.io/pypi/v/mock-alchemy.svg\n    :target: https://pypi.org/project/mock-alchemy/\n\n.. image:: https://img.shields.io/pypi/pyversions/mock-alchemy.svg\n    :target: https://pypi.org/project/mock-alchemy/\n\n.. image:: https://github.com/rajivsarvepalli/mock-alchemy/workflows/Tests/badge.svg\n    :target: https://github.com/rajivsarvepalli/mock-alchemy/actions?workflow=Tests\n\n.. image:: https://codecov.io/gh/rajivsarvepalli/mock-alchemy/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/rajivsarvepalli/mock-alchemy\n\nSQLAlchemy mock helpers.\n\n* Free software: MIT license\n* GitHub: https://github.com/rajivsarvepalli/mock-alchemy\n\nDocumentation\n-------------\n\nFull documentation is available at `http://mock-alchemy.rtfd.io/ <http://mock-alchemy.rtfd.io/>`__.\nOn the documentation, you should be able to select a version of your choice in order to view documentation\nof an older version if need be.\nThis README includes some basic examples, but more detailed examples are included in the documentation, especially in the `user guide <https://mock-alchemy.readthedocs.io/en/latest/user_guide/>`__.\n\nCredit\n----------\n\nThe original library (``alchemy-mock``) was created by Miroslav Shubernetskiy and Serkan Hoscai. This is a forked version due to a lack of updates\nin the original library. It appeared that the ``alchemy-mock`` project was no longer supported. Therefore, since I desired to add some basic support\nfor deleting, I created my own version of the library. Full credit goes to the original creators for starting and building this project. You can find the\noriginal package on `PyPi <https://pypi.org/project/alchemy-mock/>`__ and `Github <https://github.com/miki725/alchemy-mock>`__.\n\nInstalling\n----------\n\nYou can install ``mock-alchemy`` using pip::\n\n    $ pip install mock-alchemy\n\nWhy?\n----\n\nSQLAlchemy is awesome. Unittests are great.\nAccessing DB during tests - not so much.\nThis library provides easy way to mock SQLAlchemy's session\nin unittests while preserving ability to do sane asserts.\nNormally SQLAlchemy's expressions cannot be easily compared\nas comparison on binary expression produces yet another binary expression::\n\n    >>> type((Model.foo == 5) == (Model.bar == 5))\n    <class 'sqlalchemy.sql.elements.BinaryExpression'>\n\nBut they can be compared with this library::\n\n    >>> ExpressionMatcher(Model.foo == 5) == (Model.bar == 5)\n    False\n\nUsing\n-----\n\n``ExpressionMatcher`` can be directly used::\n\n    >>> from mock_alchemy.comparison import ExpressionMatcher\n    >>> ExpressionMatcher(Model.foo == 5) == (Model.foo == 5)\n    True\n\nAlternatively ``AlchemyMagicMock`` can be used to mock out SQLAlchemy session::\n\n    >>> from mock_alchemy.mocking import AlchemyMagicMock\n    >>> session = AlchemyMagicMock()\n    >>> session.query(Model).filter(Model.foo == 5).all()\n\n    >>> session.query.return_value.filter.assert_called_once_with(Model.foo == 5)\n\nIn real world though session can be interacted with multiple times to query some data.\nIn those cases ``UnifiedAlchemyMagicMock`` can be used which combines various calls for easier assertions::\n\n    >>> from mock_alchemy.mocking import UnifiedAlchemyMagicMock\n    >>> session = UnifiedAlchemyMagicMock()\n\n    >>> m = session.query(Model)\n    >>> q = m.filter(Model.foo == 5)\n    >>> if condition:\n    ...     q = q.filter(Model.bar > 10).all()\n    >>> data1 = q.all()\n    >>> data2 = m.filter(Model.note == 'hello world').all()\n\n    >>> session.filter.assert_has_calls([\n    ...     mock.call(Model.foo == 5, Model.bar > 10),\n    ...     mock.call(Model.note == 'hello world'),\n    ... ])\n\nAlso real-data can be stubbed by criteria::\n\n    >>> from mock_alchemy.mocking import UnifiedAlchemyMagicMock\n    >>> session = UnifiedAlchemyMagicMock(data=[\n    ...     (\n    ...         [mock.call.query(Model),\n    ...          mock.call.filter(Model.foo == 5, Model.bar > 10)],\n    ...         [Model(foo=5, bar=11)]\n    ...     ),\n    ...     (\n    ...         [mock.call.query(Model),\n    ...          mock.call.filter(Model.note == 'hello world')],\n    ...         [Model(note='hello world')]\n    ...     ),\n    ...     (\n    ...         [mock.call.query(AnotherModel),\n    ...          mock.call.filter(Model.foo == 5, Model.bar > 10)],\n    ...         [AnotherModel(foo=5, bar=17)]\n    ...     ),\n    ... ])\n    >>> session.query(Model).filter(Model.foo == 5).filter(Model.bar > 10).all()\n    [Model(foo=5, bar=11)]\n    >>> session.query(Model).filter(Model.note == 'hello world').all()\n    [Model(note='hello world')]\n    >>> session.query(AnotherModel).filter(Model.foo == 5).filter(Model.bar > 10).all()\n    [AnotherModel(foo=5, bar=17)]\n    >>> session.query(AnotherModel).filter(Model.note == 'hello world').all()\n    []\n\nThe ``UnifiedAlchemyMagicMock`` can partially fake session mutations\nsuch as ``session.add(instance)``. For example::\n\n    >>> session = UnifiedAlchemyMagicMock()\n    >>> session.add(Model(pk=1, foo='bar'))\n    >>> session.add(Model(pk=2, foo='baz'))\n    >>> session.query(Model).all()\n    [Model(foo='bar'), Model(foo='baz')]\n    >>> session.query(Model).get(1)\n    Model(foo='bar')\n    >>> session.query(Model).get(2)\n    Model(foo='baz')\n\nNote that its partially correct since if added models are filtered on,\nsession is unable to actually apply any filters so it returns everything::\n\n   >>> session.query(Model).filter(Model.foo == 'bar').all()\n   [Model(foo='bar'), Model(foo='baz')]\n\nFinally, ``UnifiedAlchemyMagicMock`` can partially fake deleting. Anything that can be\naccessed with ``all`` can also be deleted. For example::\n\n    >>> s = UnifiedAlchemyMagicMock()\n    >>> s.add(SomeClass(pk1=1, pk2=1))\n    >>> s.add_all([SomeClass(pk1=2, pk2=2)])\n    >>> s.query(SomeClass).all()\n    [1, 2]\n    >>> s.query(SomeClass).delete()\n    2\n    >>> s.query(SomeClass).all()\n    []\n\nNote the limitation for dynamic sessions remains the same. Additionally, the delete will not be propagated across\nqueries (only unified in the exact same query). As in if there are multiple queries in which the 'same'\nobject is present, this library considers them separate objects. For example::\n\n    >>> s = UnifiedAlchemyMagicMock(data=[\n    ...     (\n    ...         [mock.call.query('foo'),\n    ...          mock.call.filter(c == 'one', c == 'two')],\n    ...         [SomeClass(pk1=1, pk2=1), SomeClass(pk1=2, pk2=2)]\n    ...     ),\n    ...     (\n    ...         [mock.call.query('foo'),\n    ...          mock.call.filter(c == 'one', c == 'two'),\n    ...          mock.call.order_by(c)],\n    ...         [SomeClass(pk1=2, pk2=2), SomeClass(pk1=1, pk2=1)]\n    ...     ),\n    ...     (\n    ...         [mock.call.filter(c == 'three')],\n    ...         [SomeClass(pk1=3, pk2=3)]\n    ...     ),\n    ...     (\n    ...         [mock.call.query('foo'),\n    ...          mock.call.filter(c == 'one', c == 'two', c == 'three')],\n    ...         [SomeClass(pk1=1, pk2=1), SomeClass(pk1=2, pk2=2), SomeClass(pk1=3, pk2=3)]\n    ...     ),\n    ... ])\n\n    >>> s.query('foo').filter(c == 'three').delete()\n    1\n    >>> s.query('foo').filter(c == 'three').all()\n    []\n    >>> s.query('foo').filter(c == 'one').filter(c == 'two').filter(c == 'three').all()\n    [1, 2, 3]\n\nThe item referred to by :code:`c == 'three'` is still present in the filtered query despite the individual item being deleted.\n",
    'author': 'Rajiv Sarvepalli',
    'author_email': 'rajiv@sarvepalli.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rajivsarvepalli/mock-alchemy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
