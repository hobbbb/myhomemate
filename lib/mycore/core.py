import asyncio
import logging
import threading

from async_timeout import timeout

_LOGGER = logging.getLogger(__name__)
TIMEOUT_EVENT_START = 15


def callback(func):
    """Annotation to mark method as safe to call from within the event loop."""
    setattr(func, '_hass_callback', True)
    return func


class MyHomeMate:
    """Root object of the Home Assistant home automation."""

    def __init__(self, loop=None):
        """Initialize new Home Assistant object."""
        self.loop = loop or asyncio.get_event_loop()

        # executor_opts = {'max_workers': None}  # type: Dict[str, Any]
        # if sys.version_info[:2] >= (3, 6):
        #     executor_opts['thread_name_prefix'] = 'SyncWorker'

        # self.executor = ThreadPoolExecutor(**executor_opts)
        # self.loop.set_default_executor(self.executor)
        # self.loop.set_exception_handler(async_loop_exception_handler)
        self._pending_tasks = []
        self._track_task = True
        # self.bus = EventBus(self)
        # self.services = ServiceRegistry(self)
        # self.states = StateMachine(self.bus, self.loop)
        # self.config = Config()  # type: Config
        # self.components = loader.Components(self)
        # self.helpers = loader.Helpers(self)
        # # This is a dictionary that any component can store any data on.
        # self.data = {}  # type: dict
        # self.state = CoreState.not_running
        self.exit_code = 0
        # self.config_entries = None  # type: Optional[ConfigEntries]
        # # If not None, use to signal end-of-loop
        self._stopped = None

    async def async_run(self, *, attach_signals=True):
        """Home Assistant main entry point.

        Start Home Assistant and block until stopped.

        This method is a coroutine.
        """
        # if self.state != CoreState.not_running:
        #     raise RuntimeError("HASS is already running")

        # _async_stop will set this instead of stopping the loop
        self._stopped = asyncio.Event()

        await self.async_start()
        # if attach_signals:
        #     from homeassistant.helpers.signal \
        #             import async_register_signal_handling
        #     async_register_signal_handling(self)

        await self._stopped.wait()
        return self.exit_code

    async def async_start(self):
        """Finalize startup from inside the event loop.

        This method is a coroutine.
        """
        _LOGGER.info("Starting Home Assistant")
        # self.state = CoreState.starting

        setattr(self.loop, '_thread_ident', threading.get_ident())
        # self.bus.async_fire(EVENT_HOMEASSISTANT_START)

        try:
            # Only block for EVENT_HOMEASSISTANT_START listener
            self.async_stop_track_tasks()
            with timeout(TIMEOUT_EVENT_START):
                await self.async_block_till_done()
        except asyncio.TimeoutError:
            _LOGGER.warning(
                'Something is blocking Home Assistant from wrapping up the '
                'start up phase. We\'re going to continue anyway. Please '
                'report the following info at http://bit.ly/2ogP58T : %s',
                ', '.join(self.config.components))

        # Allow automations to set up the start triggers before changing state
        await asyncio.sleep(0)

        # if self.state != CoreState.starting:
        #     _LOGGER.warning(
        #         'Home Assistant startup has been interrupted. '
        #         'Its state may be inconsistent.')
        #     return

        # self.state = CoreState.running
        # _async_create_timer(self)
        _LOGGER.warning('1111')

    @callback
    def async_stop_track_tasks(self):
        """Stop track tasks so you can't wait for all tasks to be done."""
        self._track_task = False

    async def async_block_till_done(self):
        """Block till all pending work is done."""
        # To flush out any call_soon_threadsafe
        await asyncio.sleep(0)

        while self._pending_tasks:
            pending = [task for task in self._pending_tasks if not task.done()]
            self._pending_tasks.clear()
            if pending:
                await asyncio.wait(pending)
            else:
                await asyncio.sleep(0)
