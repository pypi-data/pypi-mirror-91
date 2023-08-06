"""Query objects definition and supporting code.

This module defines the interfaces provided by top-level queries and
inner, nested queries respectively.
"""

import copy
from typing import Any, List, Optional, Tuple, Type, TypeVar, Union

import yarl

from .support import (CensusValue, JoinedQueryData, QueryBaseData, QueryData,
                      SearchModifier, SearchTerm)
from .urlgen import generate_url

__all__ = [
    'JoinedQuery',
    'Query',
    'QueryBase'
]

_QueryBaseT = TypeVar('_QueryBaseT', bound='QueryBase')
_T = TypeVar('_T')


class QueryBase:
    """Base class for functionality shared between queries and joins.

    If you want to re-use the same query multiple times, use this
    class. For more control about how the query is performed, refer to
    the :class:`Query` and :class:`JoinedQuery` subclasses.

    To convert between different types of queries, use the
    :meth:`QueryBase.copy()` factory. See that method's docstring for
    details.

    Attributes:
        data: Provides low-level access to the represented query
        joins: A list of inner queries that were attached to this one.

    """

    def __init__(self, collection: Optional[str] = None,
                 **kwargs: CensusValue) -> None:
        """Initialise the query.

        Arguments:
            collection (optional): The API collection to access or
                ``None`` to display the list of available collections.
                Defaults to ``None``.
            *kwargs: Key/value pairs to pass to the
                :meth:`QueryBase.add_term()` method.

        """
        self.data = QueryBaseData(collection)
        self.joins: List[JoinedQuery] = []
        # Replace and double underscores with dots to allow accessing inner
        # fields like "name.first" or "battle_rank.value"
        kwargs = {k.replace('__', '.'): v for k, v in kwargs.items()}
        # Run the add_term method for each of the converted key/value pairs
        _ = [self.add_term(k, v, parse_modifier=True)
             for k, v in kwargs.items()]

    def add_join(self: _QueryBaseT, query: 'JoinedQuery',
                 **kwargs: Any) -> _QueryBaseT:
        """Add an existing :class:`JoinedQuery` to this query.

        This converts an existing :class:`QueryBase` instance to a
        :class:`JoinedQuery` using the :meth:`QueryBase.copy()`
        factory. The created join is then added to this query.

        To create a new query and add it immediately, use the
        :meth:`QueryBase.create_join` method instead.

        Arguments:
            query: Another query to join to the current query.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.joins.append(JoinedQuery.copy(query, **kwargs))
        return self

    def add_term(self: _QueryBaseT, field: str, value: CensusValue,
                 modifier: SearchModifier = SearchModifier.EQUAL_TO, *,
                 parse_modifier: bool = False) -> _QueryBaseT:
        """Add a new filter term to the query.

        Filter terms are used to either reduce the number of results
        returned, or to specify the exact ID expected. Refer to the
        :class:`SearchTerm` class for details and examples.

        Arguments:
            field: The field to filter by.
            value: The value of the filter term.
            modifier(optional): A search modifier to use. This will
                only be used if ``parse_modifier`` is False.
                Defaults to ``SearchModifier.EQUAL_TO``.
            parse_modifier(optional): If True, the search modifier
                will be inferred from the value. Defaults to ``False``.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        if parse_modifier:
            term = SearchTerm.infer(field, value)
        else:
            term = SearchTerm(field, value, modifier=modifier)
        self.data.terms.append(term)
        return self

    @classmethod
    def copy(cls: Type[_QueryBaseT], template: 'QueryBase',
             copy_joins: bool = False, deep_copy: bool = False,
             **kwargs: Any) -> _QueryBaseT:
        """Create a new query, copying most data from the template.

        The new query will share the collection, terms and show/hide
        markers of the template. If ``copy_joins`` is enabled, it will
        also copy its list of joins.

        Among other things, allows easy creation of joins from existing
        queries, which is handy if you have complex existing joins or
        hidden fields that would be tedious to recreate.

        By default, this creates a shallow copy. Modifying the terms or
        joined queries will cause mutations of the template. Set the
        ``deep_copy`` flag to ensure complete independence.

        Any keyword arguments are passed to the new query's
        initialiser.

        Example:

            .. code-block:: python3

                # This is an existing query that does what we need it
                # to, assume it has some complex join or hidden field
                # setup that would make it tedious to re-create.
                old = Query('character')

                # This is an unrelated, new query. We want its join to
                # return the exact same data structure as the previous
                # query.
                new = Query('outfit_member', outfit_id=...).limit(1000)

                # Create a join emulating the original query and add it
                join = JoinedQuery.copy(old, copy_joins=True)
                new.add_join(join)

        Arguments:
            template: The query to copy.
            copy_joins (optional): Whether to recursively copy joined
                queries. Defaults to ``False``.
            deep_copy (optional): Whether to perform a deep copy. Use
                this if you intend to modify the list of terms or other
                mutable types to avoid changing the template. Defaults
                to ``False``.
            **kwargs: Any keyword arguments are passed on to the new
                query's constructor.

        Raises:
            TypeError: Raised when attempting to copy into a
                :class:`JoinedQuery` without a collection specified.

        Returns:
            An instance of the current class populated with information
            from the template query.

        """
        copy_func = copy.deepcopy if deep_copy else _dummy_copy
        # Create a new querybase instance
        instance = cls(copy_func(template.data.collection), **kwargs)
        attrs = ['terms', 'hide', 'show']
        for attr in attrs:
            value = copy_func(getattr(template.data, attr))
            setattr(instance.data, attr, value)
        if copy_joins:
            instance.joins = copy_func(template.joins)
        return instance

    def create_join(self, collection: str, *args: Any,
                    **kwargs: Any) -> 'JoinedQuery':
        """Create a new joined query and add it to the current one.

        See the initialiser for JoinedQuery for arguments, this method
        passes and parameters given on.

        Arguments:
            collection: The collection to join.
            *args: Any anonymous positional arguments are passed on to
                :meth:`JoinedQuery.__init__()`
            *kwargs: Any anonymous keyword arguments are passed on to
                :meth:`JoinedQuery.__init__()`

        Returns:
            The JoinedQuery instance that was created.

        """
        join = JoinedQuery(collection, *args, **kwargs)
        self.joins.append(join)
        return join

    def hide(self: _QueryBaseT, field: str, *args: str) -> _QueryBaseT:
        """Set the fields to hide in the response.

        The given fields will not be included in the result. Note that
        this can break joins if the field they are attached to is not
        included.

        This is mutually exclusive with :meth:`QueryBase.show()`;
        setting one will undo any changes made by the other.

        Arguments:
            field: A field name to hide from the result data.
            *args: Any number of additional fields to hide.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.data.hide = [field]
        self.data.hide.extend(args)
        self.data.show = []
        return self

    def show(self: _QueryBaseT, field: str, *args: str) -> _QueryBaseT:
        """Set the fields to show in the response.

        Any other fields will not be included in the result. Note that
        this can break joins if the field they are attached to is not
        included.

        This is mutually exclusive with :meth:`QueryBase.hide()`;
        setting one will undo any changes made by the other.

        Arguments:
            field: A field name to include in the result data.
            *args: Any number of additional fields to include.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.data.show = [field]
        self.data.show.extend(args)
        self.data.hide = []
        return self


class Query(QueryBase):
    """The main query supplied to the API.

    The top-level query has access to additional return value formats
    such as sorting or tree views, and also supports additional, global
    flags that will propagate through to any inner, joined queries.

    This subclasses :class:`QueryBase`. Refer to its docstring for
    details on inherited methods and attributes.

    You can find additional information on the attributes in their
    respective setter methods.

    Attributes:
        data: Provides low-level access to the represented query

    """

    def __init__(self, collection: Optional[str] = None,
                 namespace: str = 'ps2:v2', service_id: str = 's:example',
                 **kwargs: CensusValue) -> None:
        """Create a new top-level query.

        The collection argument, as well as any keyword arguments, are
        passed on to the constructor of the QueryBase class.

        Arguments:
            collection (optional): The API collection to access.
                Defaults to ``None``.
            namespace (optional): The namespace to access. Defaults to
                ``'ps2:v2'``.
            service_id (optional): Your personal service ID. Note that
                the default service ID is heavily rate limited.
                Defaults to ``'s:example'``.

        """
        super().__init__(collection, **kwargs)
        data: QueryBaseData = self.data  # type: ignore
        self.data = QueryData.from_base(data)
        self.data.namespace = namespace
        self.data.service_id = service_id

    def __str__(self) -> str:
        """Return the string representation of the query.

        This is the URL in its finished form. Use :meth:`Query.url()`
        to retrieve the URL as a :class:`yarl.URL` instance for extra
        control.

        Returns:
            The full URL describing this query and all of its joins.

        """
        return str(self.url().human_repr())

    def case(self, value: bool = True) -> 'Query':
        """Globally ignore case for this query.

        Note that case-insensitive look-ups are significantly slower.
        Where available, use a case-sensitive query targeting a
        lowercase field like ``ps2/character.name.first_lower``.

        Arguments:
            value (optional): Whether to ignore case for this query.
                Defaults to ``True``.

        Returns:
            The full URL describing this query and all of its joins.

        """
        self.data.case = value
        return self

    @classmethod
    def copy(cls, template: QueryBase,  # type: ignore
             copy_joins: bool = False, deep_copy: bool = False,
             **kwargs: Any) -> 'Query':
        """Create a new query, copying most data from the template.

        The new query will share the collection, terms and show/hide
        markers of the template. If ``copy_joins`` is enabled, it will
        also copy its list of joins.

        Among other things, allows easy creation of joins from existing
        queries, which is handy if you have complex existing joins or
        hidden fields that would be tedious to recreate.

        By default, this creates a shallow copy. Modifying the terms or
        joined queries will cause mutations of the template. Set the
        ``deep_copy`` flag to ensure complete independence.

        Any keyword arguments are passed to the new query's
        initialiser.

        Example:

            .. code-block:: python3

                # This is an existing query that does what we need it
                # to, assume it has some complex join or hidden field
                # setup that would make it tedious to re-create.
                old = Query('character')

                # This is an unrelated, new query. We want its join to
                # return the exact same data structure as the previous
                # query.
                new = Query('outfit_member', outfit_id=...).limit(1000)

                # Create a join emulating the original query and add it
                join = JoinedQuery.copy(old, copy_joins=True)
                new.add_join(join)

        Arguments:
            template: The query to copy.
            copy_joins (optional): Whether to recursively copy joined
                queries. Defaults to ``False``.
            deep_copy (optional): Whether to perform a deep copy. Use
                this if you intend to modify the list of terms or other
                mutable types to avoid changing the template. Defaults
                to ``False``.
            **kwargs: Any keyword arguments are passed on to the new
                query's constructor.

        Raises:
            TypeError: Raised when attempting to copy into a
                :class:`JoinedQuery` without a collection specified.

        Returns:
            An instance of the current class populated with information
            from the template query.

        """
        copy_func = copy.deepcopy if deep_copy else _dummy_copy
        # Create a new Query instance
        instance = super().copy(template, copy_joins=copy_joins,
                                deep_copy=deep_copy, *kwargs)
        assert isinstance(instance, Query)
        if isinstance(template, Query):
            # Additional attributes to include when copying a top-level query
            attrs = ['case', 'distinct', 'exact_match_first', 'has',
                     'include_null', 'lang', 'limit', 'limit_per_db',
                     'namespace', 'resolve', 'retry', 'service_id', 'sort',
                     'start', 'timing', 'tree']
            for attr in attrs:
                value = copy_func(getattr(template.data, attr))
                setattr(instance.data, attr, value)
        # Include an arbitrary limit when copying from a joined list
        elif isinstance(template, JoinedQuery) and template.data.is_list:
            # NOTE: Joined lists have no set length, so this might break for
            # very long or complex joins.
            instance.limit(10000)  # pylint: disable=no-member
        return instance

    def has(self, field: str, *args: str) -> 'Query':
        """Hide results with a ``NULL`` value at the given field.

        This is useful for filtering large data sets by optional
        fields, such as searching the ``ps2/weapons`` collection for
        heat-based weapons using the heat-mechanic-specific fields.

        Arguments:
            field: The field required for results to be included.
            *args: Additional required fields.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.data.has = [field]
        self.data.has.extend(args)
        return self

    def distinct(self, field: Optional[str]) -> 'Query':
        """Query command used to show all unique values for a field.

        Arguments:
            field: The field to show unique values for. Set to ``None``
                to disable.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.data.distinct = field
        return self

    def exact_match_first(self, value: bool = True) -> 'Query':
        """Whether to display exact matches before partial matches.

        When performing RegEx searches (i.e. ones using either
        :attr:`SearchModifier.STARTS_WITH` or
        :attr:`SearchModifier.CONTAINS`), this setting will always
        promote an exact match to be the first item returned,
        regardless of any sorting settings applied.

        Arguments:
            value (optional): Whether to promote exact matches.
                Defaults to ``True``.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.data.exact_match_first = value
        return self

    def include_null(self, value: bool) -> 'Query':
        """Whether to include NULL values in the response.

        This is useful for API introspection, but it is generally more
        bandwidth-friendly to use the :meth:`dict.get()` method with a
        default value when parsing the result dictionary.

        This only affects the top-level query itself; joined queries
        will only show non-NULL values.

        Arguments:
            value: Enable or disable the setting.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.data.include_null = value
        return self

    def lang(self, lang: Optional[str] = None) -> 'Query':
        """Set the locale to user for the query.

        By default, queries return all locales for localised strings.
        Use this flag to only include the given locale, or reset to
        ``None`` to include all localisations.

        The following locales are currently supported and maintained:::

            German: 'de', English: 'en', Spanish: 'es',
            French: 'fr', Italian: 'it'

        Arguments:
            lang (optional): The locale identifier to return. Defaults
                to ``None``.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.data.lang = lang
        return self

    def limit(self, limit: int) -> 'Query':
        """Specify the number of results returned.

        By default, the API will only return the first match for any
        given query, you can increase the number of results using this
        method.

        The maximum number of values permissible varies from collection
        to collection, e.g. 100k for ``ps2/character``, but only 5000
        for ``ps2/item``. Use your best judgement.

        This is mutually exclusive with :meth:`Query.limit_per_db()`,
        setting one will undo the changes made by the other.

        Arguments:
            limit: The number of results to return. Must be at least 1.

        Raises:
            ValueError: Raised if ``limit`` is less than 1.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        if limit < 1:
            raise ValueError('limit must be greater than or equal to 1')
        self.data.limit = limit
        self.data.limit_per_db = 1
        return self

    def limit_per_db(self, limit_per_db: int) -> 'Query':
        """Specify the number of results returned per database.

        This method works similarly to :meth:`Query.limit()`, but will
        yield better results for distributed collections such as
        ps2/character, which is spread across 20 different databases
        more or less randomly.

        This is mutually exclusive with :meth:`Query.limit()`, setting
        one will undo the changes made by the other.

        Arguments:
            limit_per_db: The number of results to return per database.
                Must be at least 1.

        Raises:
            ValueError: Raised if ``limit_per_db`` is less than 1.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        if limit_per_db < 1:
            raise ValueError('limit_per_db must be greater than or equal to 1')
        self.data.limit_per_db = limit_per_db
        self.data.limit = 1
        return self

    def offset(self, offset: int) -> 'Query':
        """Alias for the :meth:`Query.start()` method.

        Refer to its docstring for details.

        Arguments:
            offset: The number of results to skip.

        Raises:
            ValueError: Raised if offset is negative.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        try:
            self.start(offset)
        except ValueError as err:
            raise ValueError('offset may not be negative') from err
        return self

    def resolve(self, name: str, *args: str) -> 'Query':
        """Resolve additional data for a collection.

        Resolves are a lighter version of joined queries and can be
        used to quickly include associated information with the
        results.

        Perform a query with no collection specified to see a list of
        resolvable names for each collection.

        Arguments:
            name: A resolvable name to attach to the query.
            *args: Any number of additional resolvable names to attach.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.data.resolve = [name]
        self.data.resolve.extend(args)
        return self

    def retry(self, retry: bool = False) -> 'Query':
        """Enable automatic query retry.

        By default, failed queries will be retried automatically. Set
        this to False to disable this behaviour if you want to fail
        early.

        Arguments:
            retry (optional): Whether to enable automatic query
                retrying. Defaults to ``False``.

        Returns:
            The full URL describing this query and all of its joins.

        """
        self.data.retry = retry
        return self

    def start(self, start: int) -> 'Query':
        """Skip the given number of results in the response.

        Together with :meth:`Query.limit()`, this can be used to create
        a paginated view of API data.

        Arguments:
            start: The number of results to skip.

        Raises:
            ValueError: Raised if start is negative.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        if start < 0:
            raise ValueError('start may not be negative')
        if start >= 0:
            self.data.start = start
        return self

    def sort(self, field: Union[str, Tuple[str, bool]],
             *args: Union[str, Tuple[str, bool]]) -> 'Query':
        """Sort the results by one or more fields.

        By default, this uses ascending sort order. For descending
        order, pass a tuple with a negative second element:

        .. code-block:: python3

            QueryBase.sort('field1', ('field'2, True))  # Ascending
            QueryBase.sort(('field3', False))  # Descending

        If multiple field names are provided, multiple sorting passes
        will be performed in order to further refine the list returned.

        Arguments:
            field: A qualified field name to sort by.
            *args: Additional fields to sort by.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.data.sort = [field]
        self.data.sort.extend(args)
        return self

    def timing(self, value: bool = True) -> 'Query':
        """Enabling query profiling output.

        Setting this flag will include an additional "timing" key in
        the response, providing timing information for the main query
        and any joins.

        Arguments:
            value (optional): Whether to enable profiling. Defaults to
                ``True``.

        Returns:
            The full URL describing this query and all of its joins.

        """
        self.data.timing = value
        return self

    def tree(self, field: str, is_list: bool = False, prefix: str = '',
             start: Optional[str] = None) -> 'Query':
        """Reformat a result list into a data tree.

        This is useful for lists of data with obvious categorisation,
        such as grouping weapons by their type.

        Arguments:
            field: The field to remove and use for the data structure.
            list (optional): Whether the tree data is a list. Defaults
                to 0.
            prefix (optional): A prefix to add to the field value to
                increase readability. Defaults to ``''``.
            start (optional): Used to tell the tree where to start. If
                ``None``, the root list of results will be reformatted
                as a tree. Defaults to ``None``.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.data.tree = {'field': field, 'is_list': is_list,
                          'prefix': prefix, 'start': start}
        return self

    def url(self, verb: str = 'get', skip_checks: bool = False) -> yarl.URL:
        """Generate the URL representing this query.

        This will also recursively process any joined queries.

        Arguments:
            verb (optional): The query verb to use for the query. Known
                options are ``'get'``, used to return a list of
                results, and ``'count'``, used to return the length of
                that list. Defaults to ``'get'``.
            skip_checks (optional): By default, the URL generator will
                perform a number of checks to validate your query.
                Enabling this flag will skip the checks. Defaults to
                ``False``.

        Returns:
            A URL object representing the query.

        """
        self.data.joins = [j.serialise() for j in self.joins]
        return generate_url(self.data, verb, validate=not skip_checks)


class JoinedQuery(QueryBase):
    """A sub-query to be joined to an existing query.

    Joined queries (or "joins") allow performing multiple, related
    look-ups in the same request. For a simpler but less powerful
    interface, see the :meth:`Query.resolve()` method.

    This subclasses :class:`QueryBase`. Refer to its docstring for
    details on inherited methods and attributes.

    You can find additional information on the attributes in their
    respective setter methods.

    Attributes:
        data: Provides low-level access to the represented joined query

    """

    def __init__(self, collection: str, **kwargs: CensusValue) -> None:
        """Instantiate a joined, inner query."""
        super().__init__(collection, **kwargs)
        data: QueryBaseData = self.data  # type: ignore
        self.data = JoinedQueryData.from_base(data)

    @classmethod
    def copy(cls, template: QueryBase,  # type: ignore
             copy_joins: bool = False,   deep_copy: bool = False,
             **kwargs: Any) -> 'JoinedQuery':
        """Create a new query, copying most data from the template.

        The new query will share the collection, terms and show/hide
        markers of the template. If ``copy_joins`` is enabled, it will
        also copy its list of joins.

        Among other things, allows easy creation of joins from existing
        queries, which is handy if you have complex existing joins or
        hidden fields that would be tedious to recreate.

        By default, this creates a shallow copy. Modifying the terms or
        joined queries will cause mutations of the template. Set the
        ``deep_copy`` flag to ensure complete independence.

        Any keyword arguments are passed to the new query's
        initialiser.

        Example:

            .. code-block:: python3

                # This is an existing query that does what we need it
                # to, assume it has some complex join or hidden field
                # setup that would make it tedious to re-create.
                old = Query('character')

                # This is an unrelated, new query. We want its join to
                # return the exact same data structure as the previous
                # query.
                new = Query('outfit_member', outfit_id=...).limit(1000)

                # Create a join emulating the original query and add it
                join = JoinedQuery.copy(old, copy_joins=True)
                new.add_join(join)

        Arguments:
            template: The query to copy.
            copy_joins (optional): Whether to recursively copy joined
                queries. Defaults to ``False``.
            deep_copy (optional): Whether to perform a deep copy. Use
                this if you intend to modify the list of terms or other
                mutable types to avoid changing the template. Defaults
                to ``False``.
            **kwargs: Any keyword arguments are passed on to the new
                query's constructor.

        Raises:
            TypeError: Raised when attempting to copy into a
                :class:`JoinedQuery` without a collection specified.

        Returns:
            An instance of the current class populated with information
            from the template query.

        """
        # A joined query cannot be created without a collection
        if template.data.collection is None:
            raise TypeError('JoinedQuery requires a collection')
        copy_func = copy.deepcopy if deep_copy else _dummy_copy
        # Create a new JoinedQuery instance
        instance = super().copy(template, copy_joins=copy_joins,
                                deep_copy=deep_copy, **kwargs)
        assert isinstance(instance, JoinedQuery)
        if isinstance(template, JoinedQuery):
            # Additional attributes to include when copying another join
            attrs = [
                'inject_at', 'is_list', 'is_outer', 'field_on', 'field_to']
            for attr in attrs:
                value = copy_func(getattr(template.data, attr))
                setattr(instance.data, attr, value)
        # If the original query had a non-default limit value, the join should
        # also return a list.
        elif isinstance(template, Query):
            if template.data.limit > 1 or template.data.limit_per_db > 1:
                instance.data.is_list = True
        return instance

    def serialise(self) -> JoinedQueryData:
        """Process any internal joins and return a nested data dict."""
        data = self.data
        data.joins = [j.serialise() for j in self.joins]
        return data

    def set_fields(self, parent: Optional[str], child: Optional[str] = None
                   ) -> 'JoinedQuery':
        """Set the field names to use for the join.

        The API will use inferred names whenever possible, inferred
        names might be ``<parent-collection>_id`` or`
        ``<child-collection>_id``.

        Use this method to specify the field names manually. Either of
        the given values may be ``None`` to use the default naming
        system.

        Specifying only the parent's name will apply it to both fields.

        Arguments:
            parent: The field name on the parent collection.
            child (optional): The field name on the child collection.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        if parent is not None:
            self.data.field_on = parent
            if child is None:
                self.data.field_to = parent
        if child is not None:
            self.data.field_to = child
        return self

    def set_inject_at(self, key: Optional[str]) -> 'JoinedQuery':
        """Set the name of the field to insert the joined data at.

        By default, the inserted is added to a dynamically generated
        key following the pattern
        ``<parent_field>_join_<joined_collection>``. Example:::

            character_id_join_characters_online_status

        This method allows overriding the name of this insertion key.

        This will overwrite existing keys. If the existing key is a
        JSON object/Python dict, the added keys will be merged. When
        updating this dictionary, any colliding keys will be appended
        with ``_merged``.
        Non-dict keys will simply be overwritten by the joined data.

        Arguments:
            key (optional): The name of the key to inject the joined
                data at. If ``None``, the autogenerated name is used.
                Defaults to ``None``.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.data.inject_at = key
        return self

    def set_list(self, is_list: bool) -> 'JoinedQuery':
        """Set whether the current join should return a list.

        If True, the join will return any matching elements. Be wary of
        large relational collections such as ``ps2/characters_item``;
        there is no limiting system, just an eventual hard cut-off. Use
        terms to reduce the number of matching elements when flagging a
        join as a list.

        Arguments:
            is_list: Whether the join should return a list.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.data.is_list = is_list
        return self

    def set_outer(self, is_outer: bool) -> 'JoinedQuery':
        """Set whether the current join is an outer or inner join.

        An outer join (the default setting) will include all results,
        regardless of whether some of the terms in its joins are met or
        not.

        An inner join will exclude these settings, which can be useful
        when filtering by inner values.

        For example, say you were displaying a ``ps2/characters_item``
        list with the associated ``ps2/item`` collection joined. Even
        if you added a term to only add the joins for items that are
        weapons, you would still find the full ``ps2/character_item``
        list in your results. This is the outer join behaviour.
        However, if the join is flagged as an inner join, it will
        discard any results that do not meet the join's terms.

        Arguments:
            is_outer: If True, the join will be an outer join. Set to
                False for inner join behaviour.

        Returns:
            The query instance; this allows for chaining of operations.

        """
        self.data.is_outer = is_outer
        return self


def _dummy_copy(obj: _T) -> _T:
    """Dummy function that does not actually copy anything."""
    return obj
