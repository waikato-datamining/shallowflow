STRING_READERS = None
""" contains all readers that convert strings into objects (list of AbstractStringReader) """

STRING_WRITERS = None
""" contains all writers that convert objects into strings (list of AbstractStringWriter) """

STRING_READERS_CACHE = None
""" cache of class to AbstractStringReader relation """

STRING_WRITERS_CACHE = None
""" cache of class to AbstractStringWriter relation """


class AbstractStringReader(object):
    """
    Ancestor for classes that turn strings into objects.
    """

    def handles(self, cls):
        """
        Whether it can convert a string into the specified class.

        :param cls: the class to convert to
        :type cls: type
        :return: True if it can handle it
        """
        raise NotImplemented()

    def convert(self, s):
        """
        Turns the string into an object.

        :param s: the string to convert
        :type s: str
        :return: the generated object
        """
        raise NotImplemented()


class StringReader(AbstractStringReader):
    """
    Ancestor for classes that turn strings into strings.
    """

    def handles(self, cls):
        """
        Whether it can convert a string into the specified class.

        :param cls: the class to convert to
        :type cls: type
        :return: True if it can handle it
        """
        return issubclass(cls, str)

    def convert(self, s):
        """
        Turns the string into an object.

        :param s: the string to convert
        :type s: str
        :return: the generated object
        """
        return str(s)


class BoolStringReader(AbstractStringReader):
    """
    Ancestor for classes that turn strings into bool.
    """

    def handles(self, cls):
        """
        Whether it can convert a string into the specified class.

        :param cls: the class to convert to
        :type cls: type
        :return: True if it can handle it
        """
        return issubclass(cls, bool)

    def convert(self, s):
        """
        Turns the string into an object.

        :param s: the string to convert
        :type s: str
        :return: the generated object
        """
        return bool(s)


class IntStringReader(AbstractStringReader):
    """
    Ancestor for classes that turn strings into int.
    """

    def handles(self, cls):
        """
        Whether it can convert a string into the specified class.

        :param cls: the class to convert to
        :type cls: type
        :return: True if it can handle it
        """
        return issubclass(cls, int)

    def convert(self, s):
        """
        Turns the string into an object.

        :param s: the string to convert
        :type s: str
        :return: the generated object
        """
        return int(s)


class FloatStringReader(AbstractStringReader):
    """
    Ancestor for classes that turn strings into float.
    """

    def handles(self, cls):
        """
        Whether it can convert a string into the specified class.

        :param cls: the class to convert to
        :type cls: type
        :return: True if it can handle it
        """
        return issubclass(cls, float)

    def convert(self, s):
        """
        Turns the string into an object.

        :param s: the string to convert
        :type s: str
        :return: the generated object
        """
        return float(s)


class AbstractStringWriter(object):
    """
    Ancestor for classes that turn objects into strings.
    """

    def handles(self, cls):
        """
        Whether it can convert the object into a string.

        :param cls: the class to convert
        :type cls: type
        :return: True if it can handle it
        """
        raise NotImplemented()

    def convert(self, o):
        """
        Turns the object into a string.

        :param o: the object to convert
        :return: the generated string
        :rtype: str
        """
        raise NotImplemented()


class StringWriter(AbstractStringWriter):
    """
    Ancestor for classes that turn strings into strings.
    """

    def handles(self, cls):
        """
        Whether it can convert the object into a string.

        :param cls: the class to convert
        :type cls: type
        :return: True if it can handle it
        """
        return issubclass(cls, str)

    def convert(self, o):
        """
        Turns the object into a string.

        :param o: the object to convert
        :return: the generated string
        :rtype: str
        """
        return str(o)


class BoolStringWriter(AbstractStringWriter):
    """
    Ancestor for classes that turn bools into strings.
    """

    def handles(self, cls):
        """
        Whether it can convert the object into a string.

        :param cls: the class to convert
        :type cls: type
        :return: True if it can handle it
        """
        return issubclass(cls, bool)

    def convert(self, o):
        """
        Turns the object into a string.

        :param o: the object to convert
        :return: the generated string
        :rtype: str
        """
        return str(o)


class IntStringWriter(AbstractStringWriter):
    """
    Ancestor for classes that turn objects into strings.
    """

    def handles(self, cls):
        """
        Whether it can convert the object into a string.

        :param cls: the class to convert
        :type cls: type
        :return: True if it can handle it
        """
        return issubclass(cls, int)

    def convert(self, o):
        """
        Turns the object into a string.

        :param o: the object to convert
        :return: the generated string
        :rtype: str
        """
        return str(o)


class FloatStringWriter(AbstractStringWriter):
    """
    Ancestor for classes that turn objects into strings.
    """

    def handles(self, cls):
        """
        Whether it can convert the object into a string.

        :param cls: the class to convert
        :type cls: type
        :return: True if it can handle it
        """
        return issubclass(cls, float)

    def convert(self, o):
        """
        Turns the object into a string.

        :param o: the object to convert
        :return: the generated string
        :rtype: str
        """
        return str(o)


def get_string_readers():
    """
    Returns the registered readers.

    :return: the readers
    :rtype: list
    """
    global STRING_READERS
    if STRING_READERS is None:
        STRING_READERS = list()
    return STRING_READERS


def get_string_readers_cache():
    """
    Returns the cache for registered readers (class -> reader).

    :return: the readers
    :rtype: dict
    """
    global STRING_READERS_CACHE
    if STRING_READERS_CACHE is None:
        STRING_READERS_CACHE = dict()
    return STRING_READERS_CACHE


def add_string_reader(reader):
    """
    Adds a reader.

    :param reader: the reader to add
    :type reader: object
    """
    get_string_readers().append(reader)


def has_string_reader(cls):
    """
    Checks whether a reader is registered for the class.

    :param cls: the class to check
    :type cls: object
    :return: true if reader registered
    :rtype: bool
    """
    return get_string_reader(cls) is not None


def get_string_reader(cls):
    """
    Returns the reader registered for the class.

    :param cls: the class to get the reader for
    :type cls: object
    :return: the reader method, None if none registered
    """
    if cls in get_string_readers_cache():
        if isinstance(get_string_readers_cache()[cls], bool):
            # we store False as a placeholder
            return None
        else:
            return get_string_readers_cache()[cls]

    # iterate readers to see whether any can handle the class
    for reader in get_string_readers():
        if reader().handles(cls):
            get_string_readers_cache()[cls] = reader
            return reader

    # flag entry
    get_string_readers_cache()[cls] = False
    return None


def get_string_writers():
    """
    Returns the registered writers.

    :return: the writers
    :rtype: list
    """
    global STRING_WRITERS
    if STRING_WRITERS is None:
        STRING_WRITERS = list()
    return STRING_WRITERS


def get_string_writers_cache():
    """
    Returns the cache for registered writers (class -> writer).

    :return: the writers
    :rtype: dict
    """
    global STRING_WRITERS_CACHE
    if STRING_WRITERS_CACHE is None:
        STRING_WRITERS_CACHE = dict()
    return STRING_WRITERS_CACHE


def add_string_writer(writer):
    """
    Adds a writer for the specified class.

    :param cls: the class to add the writer for
    :type cls: object
    :param writer: the writer method to add
    :type writer: object
    """
    get_string_writers().append(writer)


def has_string_writer(cls):
    """
    Checks whether a writer is registered for the class.

    :param cls: the class to check
    :type cls: object
    :return: true if writer registered
    :rtype: bool
    """
    return get_string_writer(cls) is not None


def get_string_writer(cls):
    """
    Returns the writer registered for the class.

    :param cls: the class to get the writer for
    :type cls: object
    :return: the writer method, None if none registered
    :rtype: object
    """
    if cls in get_string_writers_cache():
        if isinstance(get_string_writers_cache()[cls], bool):
            # we store False as a placeholder
            return None
        else:
            return get_string_writers_cache()[cls]

    # iterate writers to see whether any can handle the class
    for writer in get_string_writers():
        w = writer()
        if w.handles(cls):
            get_string_writers_cache()[cls] = writer
            return writer

    # flag entry
    get_string_writers_cache()[cls] = False
    return None


# add default readers
add_string_reader(StringReader)
add_string_reader(BoolStringReader)
add_string_reader(IntStringReader)
add_string_reader(FloatStringReader)

# add default writers
add_string_writer(StringWriter)
add_string_writer(BoolStringWriter)
add_string_writer(IntStringWriter)
add_string_writer(FloatStringWriter)
