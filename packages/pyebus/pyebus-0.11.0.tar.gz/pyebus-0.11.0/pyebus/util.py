"""Utilities."""

from .const import AUTO


def repr_(obj, args=None, kwargs=None):
    """
    Return Python Representation String.

    Keyword Args:
        args (tuple): Tuple with all arg values
        kwargs (tuple): Tuple of (key, value, default) tuples.
    """
    classname = obj.__class__.__qualname__
    args = [repr(arg) for arg in args or []]
    if kwargs:
        for key, value, default in kwargs:
            if value != default:
                args.append("%s=%r" % (key, value))
    return "%s(%s)" % (classname, ", ".join(args))


HIGHPRIO_KEYWORDS = ("temp", "status")
LOWPRIO_KEYWORDS = ("error", "min", "max", "param", "offset", "name", "hours", "energy", "yield")


def resolve_prio(msgdef, setprio):
    """Calculate best priority."""
    if msgdef.read:
        if setprio == AUTO:
            # Prio is only available on read messages.
            namelower = msgdef.name.lower()
            if msgdef.update or msgdef.write or any(keyword in namelower for keyword in LOWPRIO_KEYWORDS):
                # we just want to ensure that we do not miss any value
                setprio = 3
            elif any(keyword in namelower for keyword in HIGHPRIO_KEYWORDS):
                # we just want to ensure that we do not miss any value
                setprio = 1
            else:
                setprio = 2
        return setprio
    else:
        return None


class UnbufferedStream:

    """Unbuffered `stream`."""

    def __init__(self, stream):
        self.stream = stream

    def write(self, *args, **kwargs):
        """Write."""
        self.stream.write(*args, **kwargs)
        self.stream.flush()

    def writelines(self, *args, **kwargs):
        """Write multiple lines."""
        self.stream.writelines(*args, **kwargs)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)
