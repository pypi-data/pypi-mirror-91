# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2017,2018
"""
Stream transformations using relational predicates.
"""

from streamsx.spl.op import Invoke, Map

import streamsx.standard._version
__version__ = streamsx.standard._version.__version__

class Aggregate(Map):
    """Aggregation against a window of a structured schema stream.

    The resuting stream (attribute ``stream``) will contain aggregations
    of the window defined by the methods invoked against the instance.

    The aggregation is invoked when the window is triggered.
    A grouped aggregation will result in `N` output tuples per aggregation
    where `N` is the number of groups in the window at the time of the
    trigger. A non-grouped window results in a single tuple per aggregation.
    A window punctuation mark is submitted after the tuples resulting
    from the aggregation.

    In all examples, an input schema of ``tuple<int32 id, timestamp ts, float64 reading>`` is assumed representing an input stream of sensor readings.

    Example of aggregating sensor readings to produce a stream containing
    the maximum, minimum and average reading over the last ten minutes
    updating every minute and grouped by sensor::

        from streamsx.standard.relational import Aggregate

        # Declare the window
        win = readings.last(datetime.timedelta(minutes=10)).trigger(datetime.timedelta(minutes=1))

        # Declare the output schema
        schema = 'tuple<int32 id, timestamp ts, float64 max_reading, float64 min_reading, float64 avg_reading>'


        # Invoke the aggregation
        agg = Aggregate.invoke(win, schema, group='id')

        # Declare the output attribute assignments.
        agg.min_reading = agg.min('reading')
        agg.max_reading = agg.max('reading')
        agg.avg_reading = agg.average('reading')

        # resulting stream is agg.stream
        agg.stream.print()

    When an output attribute is not assigned and it has a matching
    input attribute the value in the last tuple for the group is used.
    In the example above ``id`` will be set to the sensor identifier
    of the group and ``ts`` will be set to the timestamp of the most
    recent tuple for the group.

    For the output attribute assignment methods that return a grouped
    value, such as :py:meth:`count`, :py:meth:`max`, when the window is not
    grouped the value is against all tuples in the window.

    The aggregation is implemented using the ``spl.relational::Aggregate``
    SPL primitive operator from the SPL Standard toolkit.
    """
    @staticmethod
    def invoke(window, schema, group=None, name=None):
        """Invoke an aggregation against a window.

        Args:
            window(streamsx.topology.topology.Window): Window to aggregate against.
            schema(str,StreamSchema): Schema of output stream containing aggregations.
            group(str): Attribute name to group aggregations.
            name(str): Invocation name, defaults to a generated name.

        Returns:
             Aggregate: Aggregate invocation.
        """
        if not isinstance(window, streamsx.topology.topology.Window):
            raise TypeError(window)
        _op = Aggregate(window, schema, group, name=name)
        if window._config is not None:
           if 'partitioned' in window._config:
              if (window._config['partitioned']):
                 _op.params['partitionBy'] =  _op.attribute(window._config['partitionBy'])
        return _op
  
    def _output_func(self, name, attribute=None):
        _eofn = name + '('
        if attribute is not None:
            _eofn = _eofn + attribute
        _eofn = _eofn + ')'
        return self.output(self.expression(_eofn))
        
    def __init__(self, window, schema, group=None, name=None):
        topology = window.topology
        kind="spl.relational::Aggregate"
        params = dict()
        if group is not None:
            params['groupBy'] = group
        #if aggregateIncompleteWindows is not None:
        #    params['aggregateIncompleteWindows'] = aggregateIncompleteWindows
        #if aggregateEvictedPartitions is not None:
        #    params['aggregateEvictedPartitions'] = aggregateEvictedPartitions
        super(Aggregate, self).__init__(kind,window,schema,params,name)

    def count(self):
        """Count of tuples in the group.

        Returns an output expression of type ``int32`` representing
        the number of tuples in the group.

        Example::

            # Count the number of tuples grouped by sensor id in the last minute
            schema = 'tuple<int32 id, timestamp ts, int32 n>'
            agg = Aggregate.invoke(s.last(datetime.timedelta(minutes=1)), schema, group='id')
            agg.n = agg.count()

        Returns:
            Expression: Output expression with the type ``int32``.
        """
        return self._output_func('Count')

    def count_all(self):
        """Count of all tuples in the window.

        Returns:
            Expression: Output expression with the type ``int32``.
        """
        return self._output_func('CountAll')
    def count_groups(self):
        """Count of all groups in the window.

        Returns:
            Expression: Output expression with the type ``int32``.
        """
        return self._output_func('CountGroups')

    def interval_end(self):
        """Get the end of the current *time-interval* window.

        .. versionadded:: 1.2

        Returns:
            Expression: Output expression with the type ``timestamp``.
        """
        return self._output_func('intervalEnd')

    def interval_start(self):
        """Get the start of the current *time-interval* window.

        .. versionadded:: 1.2

        Returns:
            Expression: Output expression with the type ``timestamp``.
        """
        return self._output_func('intervalStart')

    def pane_timing(self):
        """Get timing of a *time-interval* window pane.

        The timing of a window pane triggering in relation to the enclosing operator's watermark that is used for predicting pane completion.

        * "paneEarly": The system has not yet predicted that it has seen all data which may contribute to a pane's window.
        * "paneOnComplete": The system predicts that it has seen all data which may contribute to a pane's window.
        * "paneLate": The system encountered new data for a pane's window after predicting no more could arrive.

        .. versionadded:: 1.3

        Returns:
            Expression: Output expression with the type ``rstring``.
        """
        return self._output_func('(rstring)paneTiming')

    def max(self, attribute):
        """Maximum value for an input attribute.

        Returns an output expression representing the maximum value
        of the input attribute in the group.

        Example::

            # Get the maximum reading of the last ten tuples grouped by sensor id in the last minute
            schema = 'tuple<int32 id, timestamp ts, float64 max_reading>'

            agg = Aggregate.invoke(s.last(10), schema, group='id')
            agg.max_reading = agg.max('reading')

        Args:
            attribute(str): Attribute name to find the maximum value of.

        Returns:
            Expression: Output expression with the type of the input attribute.
        """
        return self._output_func('Max', attribute)

    def min(self, attribute):
        """Minimum value for an input attribute.

        Returns an output expression representing the minimum value
        of the input attribute in the group.

        Example::

            # Get the minimum reading of the last ten tuples grouped by sensor id
            # updating every input tuple.
            schema = 'tuple<int32 id, timestamp ts, float64 min_reading>'

            agg = Aggregate.invoke(s.last(10), schema, group='id')
            agg.min_reading = agg.min('reading')

        Args:
            attribute(str): Attribute name to find the minimum value of.

        Returns:
            Expression: Output expression with the type of the input attribute.
        """
        return self._output_func('Min', attribute)

    def sum(self, attribute):
        """Sum of values for an input attribute.

        Returns an output expression representing the sum of values
        of the input attribute in the group.

        Example::

            # Get the sum reading of the last ten tuples grouped by sensor id
            # updating every input tuple.
            schema = 'tuple<int32 id, timestamp ts, float64 sum_readings>'

            agg = Aggregate.invoke(s.last(10), schema, group='id')
            agg.sum_readings = agg.sum('reading')

        Args:
            attribute(str): Attribute name to find the sum of.

        Returns:
            Expression: Output expression with the type of the input attribute.
        """
        return self._output_func('Sum', attribute)

    def average(self, attribute):
        """Average of values for an input attribute.

        Returns an output expression representing the average of values
        of the input attribute in the group.

        Example::

            # Get the average reading of the last ten tuples grouped by sensor id
            # updating every input tuple.
            schema = 'tuple<int32 id, timestamp ts, float64 avg_reading>'

            agg = Aggregate.invoke(s.last(10), schema, group='id')
            agg.avg_reading = agg.average('reading')

        Args:
            attribute(str): Attribute name to find the average value of.

        Returns:
            Expression: Output expression with the type of the input attribute.
        """
        return self._output_func('Average', attribute)

    def first(self, attribute):
        """First value for an input attribute.

        Returns an output expression representing the first (earliest) value
        of the input attribute in the group.

        Example::

            # Get the first reading of the last ten tuples grouped by sensor id
            # updating every input tuple.
            schema = 'tuple<int32 id, timestamp ts, float64 first_reading>'

            agg = Aggregate.invoke(s.last(10), schema, group='id')
            agg.first_reading = agg.first('reading')

        Args:
            attribute(str): Attribute name to find the first value of.

        Returns:
            Expression: Output expression with the type of the input attribute.
        """
        return self._output_func('First', attribute)

    def last(self, attribute):
        """Last value for an input attribute.

        Returns an output expression representing the last
        (latest, most recent) value of the input attribute in the group.

        Example::

            # Get the last reading of the last ten tuples grouped by sensor id
            # updating every input tuple.
            schema = 'tuple<int32 id, timestamp ts, float64 last_reading>'

            agg = Aggregate.invoke(s.last(10), schema, group='id')
            agg.last_reading = agg.last('reading')

        Args:
            attribute(str): Attribute name to find the first value of.

        Returns:
            Expression: Output expression with the type of the input attribute.
        """
        return self._output_func('Last', attribute)

    def std(self, attribute, sample=False):
        """Standard deviation of values for an input attribute.

        Returns an output expression representing the standard deviation of values
        of the input attribute in the group.

        Example::

            # Get the standard deviation reading of the last ten tuples grouped by sensor id
            # updating every input tuple.
            schema = 'tuple<int32 id, timestamp ts, float64 sd_reading>'

            agg = Aggregate.invoke(s.last(10), schema, group='id')
            agg.sd_reading = agg.standard_('reading')

        Args:
            attribute(str): Attribute name to find the average value of.
            sample(bool): True to use sample standard deviation otherwise population standard deviation is used.

        Returns:
            Expression: Output expression with the type of the input attribute.
        """
        return self._output_func('SampleStdDev' if sample else 'PopulationStdDev', attribute)


class Filter(Invoke):
    """Removes tuples from a stream by passing along only those tuples that satisfy a user-specified condition.

    Non-matching tuples can be sent to a second optional output.

    The schema transformation is implemented using the ``spl.relational::Filter``
    SPL primitive operator from the SPL Standard toolkit.

    Example with one output stream::

        import streamsx.standard.relational as R
        import streamsx.standard.utility as U

        topo = Topology()
        s = U.sequence(topo, iterations=4)
        matches = R.Filter.matching(s, filter='seq>=2ul')

    Example with matching and non matching streams::

        topo = Topology()
        s = U.sequence(topo, iterations=4)
        matches, non_matches = R.Filter.matching(s, filter='seq<2ul', non_matching=True)

    """
    @staticmethod
    def matching(stream, filter, non_matching=False, name=None):
        """Filters input tuples to one or two output streams

        Args:
            stream: Input stream
            filter(str): Specifies that the condition that determines the tuples to be passed along by the Filter operator
            non_matching(bool): Non-matching tuples are sent to a second optional output stream
            name(str): Invocation name, defaults to a generated name.

        Returns:
             Stream: matching tuples (optional second stream for non matching tuples).
        """
        _op = Filter(stream, non_matching, name=name)
        if filter is not None:
            _op.params['filter'] = _op.expression(filter);
        if non_matching:
            return _op.outputs[0], _op.outputs[1]
        else:
            return _op.outputs[0]

    def __init__(self, stream, non_matching=False, name=None):
        topology = stream.topology
        kind="spl.relational::Filter"
        inputs=stream
        schema = stream.oport.schema
        schemas = [schema,schema] if non_matching else schema
        params = dict()
        super(Filter, self).__init__(topology,kind,inputs,schemas,params,name)


class Functor(Invoke):
    """Transform input tuples into output ones, and optionally filter them.

    If you do not filter an input tuple, any incoming tuple results in a tuple on each output stream

    The schema transformation is implemented using the ``spl.relational::Functor``
    SPL primitive operator from the SPL Standard toolkit.

    Example with schema transformation and two output streams::

        import streamsx.standard.relational as R
        import streamsx.standard.utility as U

        topo = Topology()
        s = U.sequence(topo, iterations=10) # schema is 'tuple<uint64 seq, timestamp ts>'
        fo = R.Functor.map(s, [StreamSchema('tuple<uint64 seq>'),StreamSchema('tuple<timestamp ts>')])
        seq_stream = fo.outputs[0] # schema is 'tuple<uint64 seq>' only
        ts_stream = fo.outputs[1] # schema is 'tuple<timestamp ts>' only

    Example with filter some tuples::

        topo = Topology()
        s = U.sequence(topo, iterations=5)
        fo = R.Functor.map(s, StreamSchema('tuple<uint64 seq>'), filter='seq>=2ul')
        fstream = fo.outputs[0]
        fstream.print()

    """
    @staticmethod
    def map(stream, schema, filter=None, name=None):
        """Map input stream schema to one or more output schemas

        Args:
            stream: Input stream
            schema(str,StreamSchema): Schema of output stream(s).
            filter(str): Specifies the condition that determines which input tuples are to be operated on.
            name(str): Invocation name, defaults to a generated name.

        Returns:
             Functor: Functor invocation.
        """
        _op = Functor(stream, schema, name=name)
        if filter is not None:
            _op.params['filter'] = _op.expression(filter);
        return _op
   
    def __init__(self, stream, schemas, filter=None, name=None):
        topology = stream.topology
        kind="spl.relational::Functor"
        inputs=stream
        params = dict()
        super(Functor, self).__init__(topology,kind,inputs,schemas,params,name)


class Join(Invoke):
    """Correlate tuples from two streams that are based on user-specified match predicates and window configurations.

    The correlation is implemented using the ``spl.relational::Join``
    SPL primitive operator from the SPL Standard toolkit.
    """
    @staticmethod
    def lookup(reference, reference_key, lookup, lookup_key, schema, match=None, name=None):
        """Used to correlate tuples from two streams that are based on user-specified match predicates and window configurations.

        When a tuple is received on an input port, it is inserted into the window corresponding to the input port, which causes the window to trigger.
        As part of the trigger processing, the tuple is compared against all tuples inside the window of the opposing input port.
        If the tuples match, then an output tuple is produced for each match.

        The ``reference_key`` and ``lookup_key`` parameters are used to specify equijoin match predicates, which result in using a hash-based join implementation.

        Args:
            reference(streamsx.topology.topology.Window): Input window
            reference_key(str): Name of the attribute
            lookup(Stream): Input stream
            lookup_key(str): Name of the attribute
            schema(str,StreamSchema): Schema of output stream.
            match(str): Specifies an expression to be used for matching the tuples. The expression might refer to attributes from both input ports. When this parameter is omitted, the default value of true is used.
            name(str): Invocation name, defaults to a generated name.

        Returns:
             Join: Join invocation.
        """
        if not isinstance(reference, streamsx.topology.topology.Window):
            raise TypeError(reference)

        _op = Join(reference, lookup.last(0), schemas=schema, match=match, name=name)
        _op.params['equalityLHS'] = _op.attribute(reference.stream, reference_key)
        _op.params['equalityRHS'] = _op.attribute(lookup, lookup_key)

        if reference._config is not None:
           if 'partitioned' in reference._config:
              if (reference._config['partitioned']):
                 _op.params['partitionByLHS'] = _op.attribute(reference.stream, reference._config['partitionBy'])

        return _op

    def __init__(self, left, right, schemas, match=None, name=None):
        topology = left.topology
        kind="spl.relational::Join"
        inputs = [left, right]
        params = dict()
        if match is not None:
            params['match'] = self.expression(match)
        #if algorithm is not None:
        #    params['algorithm'] = algorithm
        #if defaultTupleLHS is not None:
        #    params['defaultTupleLHS'] = defaultTupleLHS
        #if defaultTupleRHS is not None:
        #    params['defaultTupleRHS'] = defaultTupleRHS
        #if partitionByRHS is not None:
        #    _op.params['partitionByRHS'] = partitionByRHS
        super(Join, self).__init__(topology,kind,inputs,schemas,params,name)


