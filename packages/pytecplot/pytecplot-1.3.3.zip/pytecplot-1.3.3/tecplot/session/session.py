import atexit
import contextlib
import datetime
import logging
import platform
import textwrap

from ..tecutil import _tecutil_connector
from ..exception import *
from .state_changed import _emit_state_changes


log = logging.getLogger(__name__)


def stop():
    """Releases the |Tecplot License| and shuts down |Tecplot Engine|.

    This shuts down the |Tecplot Engine| and releases the |Tecplot License|.
    Call this function when your script is finished using |PyTecplot|.
    Calling this function is not required. If you do not call this function,
    it will be called automatically when your script exists. However, the
    |Tecplot License| will not be released until you call this function.

    This method is silently ignored when connected to a running instance of
    |Tecplot 360| (see `tecplot.session.connect()`).

    Note that stop() may only be called once during the life of a Python
    session. If it has already been called, subsequent calls do nothing::

        >>> # Shutdown tecplot and release license
        >>> tecplot.session.stop()

    See also: `tecplot.session.acquire_license()`,
    `tecplot.session.release_license()`.
    """
    _tecutil_connector.stop()


def acquire_license():
    """Attempts to acquire the |Tecplot License|

    Call this function to attempt to acquire a |Tecplot License|. If
    |Tecplot Engine| is not started, this function will start the
    |Tecplot Engine| before attempting to acquire a license.

    This function can be used to re-acquire a license that was released with
    `tecplot.session.release_license`.

    If the |Tecplot Engine| is currently running, and a
    |Tecplot License| has already been acquired, this function has no effect.

    Licenses may be acquired and released any number of times during the same
    Python session.

    Raises `TecplotLicenseError` if a valid license could not be acquired.

    .. note:: Warning emitted when close to expiration date.

        A warning is emitted using Python's built-in `warnings` module if you
        are within 30 days of your TecPLUS subscription expiration date. The
        message will look like this:

        .. code-block:: shell

            $ python
            >>> import tecplot
            >>> tecplot.session.acquire_license()
            /path/to/tecutil_connector.py:458: UserWarning:
            Your Tecplot software maintenance subscription
            (TecPLUS) will expire in **13 days**, after which you
            will no longer be able to use PyTecplot. Contact
            sales@tecplot.com to renew your TecPLUS subscription.

              warn(warning_msg)

        These warnings can be suppressed by using the ``-W ignore`` option when
        invoking the python interpreter:

        .. code-block:: shell

            $ python -W ignore
            >>> import tecplot
            >>> tecplot.session.acquire_license()

    See also: `tecplot.session.release_license()`

    Example::

        >>> import tecplot
        >>> # Do useful things
        >>> tecplot.session.release_license()
        >>> # Do time-consuming things not related to |PyTecplot|
        >>> tecplot.session.acquire_license()  # re-acquire the license
        >>> # Do useful |PyTecplot| related things.
    """
    _tecutil_connector.acquire_license()


def release_license():
    """Attempts to release the |Tecplot License|

    Call this to release a |Tecplot License|. Normally you do not need to call
    this function since `tecplot.session.stop()` will call it for you when your
    script exists and the Python interpreter is unloaded.

    This function can be used to release a license so that the license is
    available to other instances of |Tecplot 360|.

    If the |Tecplot License| has already been released, this function has
    no effect.

    Licenses may be acquired and released any number of times during the same
    Python session. This method is silently ignored when connected to a running
    instance of |Tecplot 360| (see `tecplot.session.connect()`).

    See also: `tecplot.session.acquire_license()`

    Example usage::

        >>> import tecplot
        >>> # Do useful things
        >>> tecplot.session.release_license()
        >>> # Do time-consuming things not related to |PyTecplot|
        >>> tecplot.session.acquire_license()  # re-acquire the license
        >>> # Do useful |PyTecplot| related things.
    """
    _tecutil_connector.release_license()


def start_roaming(days):
    """Check out a roaming license.

    Parameters:
        days (`int`): Number of days to roam.

    This will acquire a PyTecplot license and then attempt to set it up for
    roaming. The maximum number of days one may roam is typically 90. This
    function can be called in an interactive terminal
    and will affect all subsequent uses of PyTecplot on the local machine.
    Do not forget to `release <tecplot.session.stop_roaming>`
    the roaming license to the server if you are finished roaming before the
    expiration date.

    See also: `tecplot.session.stop_roaming()`

    Example usage where ``YYYY-MM-DD`` will be the date 10 days from when this
    code was executed::

        >>> tecplot.session.start_roaming(10)
        You have successfully checked out a roaming license of
        PyTecplot. This will be valid for 10 days until
        midnight of YYY-MM-DD.
        >>> tecplot.session.stop_roaming()
        Your PyTecplot roaming license has been checked in.
    """
    if _tecutil_connector.connected:
        msg = textwrap.dedent('''\
            Roaming PyTecplot is not available when connected.
            To roam PyTecplot, first disconnect with
            tecplot.session.disconnect(). Roaming with Tecplot 360
            is available under Help -> License Roaming.
        ''')
        raise TecplotLogicError(msg)
    _tecutil_connector.start_roaming(days)


def stop_roaming(force=False):
    """Check in (release) a roaming license.

    This will check in and make available to others on the network a license
    that you previously checked out for roaming.

    See also: `tecplot.session.start_roaming()`

    Example usage::

        >>> tecplot.session.stop_roaming()
        Your PyTecplot roaming license has been checked in.
    """
    if _tecutil_connector.connected:
        msg = textwrap.dedent('''\
            Roaming PyTecplot is not available when connected.
            To roam PyTecplot, first disconnect with
            tecplot.session.disconnect(). Roaming with Tecplot 360
            is available under Help -> License Roaming.
        ''')
        raise TecplotLogicError(msg)
    _tecutil_connector.stop_roaming(force)


def license_expiration():
    """Expiration date of the current license.

    Returns: `datetime.date`

    Example usage::

        >>> print(tecplot.session.license_expiration())
        1955-11-05
    """
    expire = _tecutil_connector.license_expiration
    if isinstance(expire, datetime.date):
        return expire


def connect(host='localhost', port=7600, timeout=10, quiet=False):
    """Connect this PyTecplot to a running instance of Tecplot 360.

    Parameters:
        host (`str`, optional): The host name or IP address of the machine
            running Tecplot 360 with the :ref:`TecUtil Server <TecUtilServer>`
            addon loaded and listening. (default: localhost)
        port (`int`, optional): The port used by the running Tecplot 360
            instance. (default:  7600)
        timeout (`int`, optional): Number of seconds to wait before giving up.
            (default: 10)
        quiet (`bool`, optional): Suppress status messages sent to the console.
            Exception messages will still be presented on errors. (default:
            `False`)

    This will connect the running python script to Tecplot 360, sending
    requests over the network. The :ref:`TecUtil Server <TecUtilServer>` addon
    must be loaded and the server must be accepting requests. To turn on the
    server in Tecplot 360, go to the main menu, click on "Scripting ->
    PyTecplot Connections...", and finally check the option to "Accept
    connections." Make sure the same port is used in both Tecplot 360 and the
    python script. For more information, see :ref:`Requirements for Connecting
    to Tecplot 360 GUI <connections>` Example usage::

        >>> tecplot.session.connect(port=7600)
        Connecting to Tecplot 360 TecUtil Server on:
            tcp://localhost:7600
        Connection established.

    To activate the :ref:`TecUtil Server <TecUtilServer>` addon in Tecplot 360
    on start-up, first create a macro file, named something like:
    *startTecUtilServer.mcr*, with the following content:

    .. code-block:: none

        #!MC 1410
        $!EXTENDEDCOMMAND
            COMMANDPROCESSORID = "TecUtilServer"
            COMMAND = R"(
                AcceptRequests = Yes
                ListenOnAddress = localhost
                ListenOnPort = 7600
            )"

    Then run Tecplot 360 from a command console with this file as one of the
    arguments::

        > tec360 startTecUtilServer.mcr

    .. warning::

        Adding the macro command above may cause a port binding conflict when
        using multiple instances of Tecplot 360. A single port can only be
        bound to one instance of the :ref:`TecUtil Server <TecUtilServer>`. You
        may still add this to the ``tecplot.add`` file which will be run
        everytime, but it must only be activated when Tecplot 360 is running
        interactively, i.e. not in batch mode. To do this, check the value of
        ``|INBATCHMODE|``:

        .. code-block:: none

            $!IF |INBATCHMODE| == 0
                $!EXTENDEDCOMMAND
                    COMMANDPROCESSORID = "TecUtilServer"
                    COMMAND = R"(
                        AcceptRequests = Yes
                        ListenOnAddress = localhost
                        ListenOnPort = 7600
                    )"
            $!ENDIF

    .. versionadded:: 2017.3
        PyTecplot connections requires Tecplot 360 2017 R3 or later.
    """
    _tecutil_connector.connect(host, port, timeout, quiet)


def connected(timeout=5):
    """Check if PyTecplot is connected to a running instance of Tecplot 360.

    This method sends a handshake message to the :ref:`TecUtil Server
    <TecUtilServer>` and waits for a successful reply, timing out in the number
    of seconds specified.

    Parameters:
        timeout (`int`, optional): Number of seconds to wait before giving up.
            (default: 5)

    .. versionadded:: 2017.3 of Tecplot 360
        PyTecplot connections requires Tecplot 360 2017 R3 or later.
    """
    if _tecutil_connector.connected:
        return _tecutil_connector.client.is_server_listening(timeout)
    else:
        return False


def disconnect(quit=False):
    """Disconnect from a running instance of Tecplot 360.

    Parameters:
        quit (`bool`, optional): Attempt to quit and close the instance of
            Tecplot 360 before disconnecting.

    .. versionadded:: 2017.3
        PyTecplot connections requires Tecplot 360 2017 R3 or later.
    """
    if connected():
        if quit:
            _tecutil_connector.client.quit()
        _tecutil_connector.disconnect()


@contextlib.contextmanager
def suspend():
    """Suspend the Tecplot engine and graphical interface.

    This context may speed up several types of operations including the
    creation of zones, filling or alterating the underlying data and the setup
    of complex styles. It will put Tecplot 360 into a "suspended" state such
    that the engine (in batch mode) or the graphical interface (in connected
    mode) will not try to keep up with the operations issued from Python. Upon
    exit of this context, the Tecplot 360 will be notified of any data
    alterations that have occured and the interface will be updated
    accordingly.

    See the `state change` section for more information about how the |Tecplot
    360| is updated when style or data is changed from a PyTecplot script.

    Example usage where `data` is some user-provided data -- see the examples
    under ``pytecplot/examples/working_with_datasets`` folder within the Teplot
    360 installation for more information.::

        fr = tp.active_frame()
        with tp.session.suspend():
            ds = fr.create_dataset('Data', ['x', 'y', 'z'])
            zn = ds.add_ordered_zone('Zone', (10, 10, 10))
            zn.values('x')[:] = data[0]
            zn.values('y')[:] = data[1]
            zn.values('z')[:] = data[2]
        fr.plot_type = tp.constant.PlotType.Cartesian3D

    .. versionadded:: 2018.2
        The suspend context, when used in connected mode, requires Tecplot 360
        2018 R2 or later to realize the full performance benefits though this
        will still provide some performance improvements with older versions of
        Tecplot 360.
    """
    if _tecutil_connector.suspended:
        yield
    else:
        _tecutil_connector.suspended = True
        _tecutil_connector._state_changes = {}
        _tecutil_connector._delete_caches = []
        try:
            if _tecutil_connector.connected:
                with _tecutil_connector.client.suspend_interface():
                    yield
                    _emit_state_changes(_tecutil_connector._state_changes)
            else:
                yield
                _emit_state_changes(_tecutil_connector._state_changes)
        finally:
            for delete_cache in _tecutil_connector._delete_caches:
                delete_cache()
            del _tecutil_connector._state_changes
            _tecutil_connector.suspended = False


def suspend_enter():
    """Free-function equivalent to entering the `suspend` context.

    This is an example of calling *a previously defined function* ``do_work()``
    within a suspend context, using ``try/finally`` to ensure the context is
    properly cleared:

        >>> try:
        >>>     tp.session.suspend_enter()
        >>>     do_work()
        >>> finally:
        >>>     tp.session.suspend_exit()
    """
    if not hasattr(_tecutil_connector, 'suspend_context'):
        _tecutil_connector.suspend_context = suspend()
    _tecutil_connector.suspend_context.__enter__()


def suspend_exit():
    """Free-function equivalent to exiting the `suspend` context.

    This must only be used following a call to
    `tecplot.session.suspend_enter()` and cannot be used within a
    `tecplot.session.suspend()` context block.
    """
    if not hasattr(_tecutil_connector, 'suspend_context'):
        raise TecplotLogicError('not in suspend context')
    _tecutil_connector.suspend_context.__exit__(None, None, None)
    delattr(_tecutil_connector, 'suspend_context')


def clear_suspend():
    """Break out of suspended mode when connected to Tecplot 360.

    Forcibly clears the suspend state of the Tecplot 360 interface. This will
    cause the :ref:`TecUtil Server <TecUtilServer>` to break out of a suspended
    state which may have been the result of a script not properly exiting from
    a `suspend()` context, possibly due to a segmentation fault. Example
    usage::

        tecplot.session.connect()
        tecplot.session.clear_suspend()
    """
    assert not _tecutil_connector.suspended, 'Can not clear in suspend context'
    assert _tecutil_connector.connected, 'Not connected to TecUtil Server'
    _tecutil_connector.client.clear_suspend_interface()


"""BUG: Resource Cleanup on MacOS Virtual Machines

There is a problem releasing the Qt Application on MacOS when running in a
virtual machine. This is a work-around to ensure the license is released on
exit of Python, though temporary files created by the Tecplot Engine may still
remain. When running on a bare-metal MacOS machine, a call to `tecplot.stop()`
will release the license and clean up any temporary files though it will likely
crash Python when run in a virtual machine.
"""
if platform.system() == 'Darwin':
    atexit.register(release_license)
else:
    atexit.register(stop)
