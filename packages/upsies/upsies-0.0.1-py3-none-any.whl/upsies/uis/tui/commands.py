"""
CLI subcommands

A command provides a :attr:`~CommandBase.jobs` property that returns a
sequence of :class:`~.jobs.base.JobBase` instances.

It is important that the jobs are only instantiated once and the
:attr:`~CommandBase.jobs` property doesn't create new jobs every time it is
accessed. The easiest way to achieve this is with the
:func:`~functools.cached_property` decorator.

CLI arguments are available as :attr:`~.CommandBase.args` and configuration
files as :attr:`~.CommandBase.config`. These should be used to create arguments
for jobs.

The docstrings of :class:`CommandBase` subclasses are used as the description in
the ``--help`` output.
"""

import abc

from ... import jobs as _jobs
from ... import trackers
from ...utils import btclients, cached_property, fs, imghosts, webdbs

import logging  # isort:skip
_log = logging.getLogger(__name__)


class CommandBase(abc.ABC):
    """Base class for all commands"""

    def __init__(self, args, config):
        self._args = args
        self._config = config

    names = NotImplemented
    """
    Sequence of command names

    The first name is the full name and the rest are aliases.
    """

    @property
    @abc.abstractmethod
    def jobs(self):
        """
        Sequence of :class:`~.jobs.base.JobBase` objects

        For convenience, the sequence may also contain `None` instead.
        """

    @property
    def jobs_active(self):
        """Same as :attr:`jobs` but without `None` values"""
        return [j for j in self.jobs if j is not None]

    @property
    def args(self):
        """CLI arguments as a :class:`argparse.Namespace` object"""
        return self._args

    @property
    def config(self):
        """Config file options as :class:`~.configfiles.ConfigFiles` object"""
        return self._config


class search_webdb(CommandBase):
    """
    Search online database like IMDb to get an ID

    Pressing ``Enter`` searches for the current query. Pressing ``Enter`` again without
    changing the query selects the focused search result.

    The focused search result can be opened in the default web browser with
    ``Alt-Enter``.
    """

    names = ('id',)

    @cached_property
    def jobs(self):
        return (
            _jobs.webdb.SearchWebDbJob(
                home_directory=fs.projectdir(self.args.CONTENT),
                ignore_cache=self.args.ignore_cache,
                content_path=self.args.CONTENT,
                db=webdbs.webdb(self.args.DB),
            ),
        )


class release_name(CommandBase):
    """
    Generate properly formatted release name

    IMDb is searched to get the correct title, year and alternative title if
    applicable.

    Audio and video information is detected with mediainfo.

    Missing required information is highlighted with placeholders,
    e.g. "UNKNOWN_RESOLUTION"
    """

    names = ('release-name', 'rn')

    @cached_property
    def jobs(self):
        return (self.imdb_job, self.release_name_job)

    @cached_property
    def release_name_job(self):
        return _jobs.release_name.ReleaseNameJob(
            home_directory=fs.projectdir(self.args.CONTENT),
            ignore_cache=self.args.ignore_cache,
            content_path=self.args.CONTENT,
        )

    @cached_property
    def imdb_job(self):
        # To be able to fetch the original title, year, etc, we need to prompt
        # for an ID first. IMDb seems to be best.
        imdb_job = _jobs.webdb.SearchWebDbJob(
            home_directory=fs.projectdir(self.args.CONTENT),
            ignore_cache=self.args.ignore_cache,
            content_path=self.args.CONTENT,
            db=webdbs.webdb('imdb'),
        )
        imdb_job.signal.register('output', self.release_name_job.fetch_info)
        return imdb_job


class create_torrent(CommandBase):
    """Create torrent file and optionally add it or move it"""

    names = ('create-torrent', 'ct')

    @cached_property
    def create_torrent_job(self):
        return _jobs.torrent.CreateTorrentJob(
            home_directory=fs.projectdir(self.args.CONTENT),
            ignore_cache=self.args.ignore_cache,
            content_path=self.args.CONTENT,
            tracker=trackers.tracker(
                name=self.args.TRACKER.lower(),
                config=self.config['trackers'][self.args.TRACKER.lower()],
            ),
        )

    @cached_property
    def add_torrent_job(self):
        if self.args.add_to:
            add_torrent_job = _jobs.torrent.AddTorrentJob(
                home_directory=fs.projectdir(self.args.CONTENT),
                ignore_cache=self.args.ignore_cache,
                client=btclients.client(
                    name=self.args.add_to,
                    **self.config['clients'][self.args.add_to],
                ),
                download_path=fs.dirname(self.args.CONTENT),
            )
            # Pass CreateTorrentJob output to AddTorrentJob input.
            self.create_torrent_job.signal.register('output', add_torrent_job.enqueue)
            # Tell AddTorrentJob to finish the current upload and then finish.
            self.create_torrent_job.signal.register('finished', add_torrent_job.finalize)
            return add_torrent_job

    @cached_property
    def copy_torrent_job(self):
        if self.args.copy_to:
            copy_torrent_job = _jobs.torrent.CopyTorrentJob(
                home_directory=fs.projectdir(self.args.CONTENT),
                ignore_cache=self.args.ignore_cache,
                destination=self.args.copy_to,
            )
            # Pass CreateTorrentJob output to CopyTorrentJob input.
            self.create_torrent_job.signal.register('output', copy_torrent_job.enqueue)
            # Tell CopyTorrentJob to finish when CreateTorrentJob is done.
            self.create_torrent_job.signal.register('finished', copy_torrent_job.finalize)
            return copy_torrent_job

    @cached_property
    def jobs(self):
        return (
            self.create_torrent_job,
            self.add_torrent_job,
            self.copy_torrent_job,
        )


class add_torrent(CommandBase):
    """Add torrent file to BitTorrent client"""

    names = ('add-torrent', 'at')

    @cached_property
    def jobs(self):
        return (
            _jobs.torrent.AddTorrentJob(
                ignore_cache=self.args.ignore_cache,
                client=btclients.client(
                    name=self.args.CLIENT,
                    **self.config['clients'][self.args.CLIENT],
                ),
                download_path=self.args.download_path,
                enqueue=self.args.TORRENT,
            ),
        )


class screenshots(CommandBase):
    """Create screenshots and optionally upload them"""

    names = ('screenshots', 'ss')

    @cached_property
    def screenshots_job(self):
        return _jobs.screenshots.ScreenshotsJob(
            home_directory=fs.projectdir(self.args.CONTENT),
            ignore_cache=self.args.ignore_cache,
            content_path=self.args.CONTENT,
            timestamps=self.args.timestamps,
            number=self.args.number,
        )

    @cached_property
    def upload_screenshots_job(self):
        if self.args.upload_to:
            imghost_job = _jobs.imghost.ImageHostJob(
                home_directory=fs.projectdir(self.args.CONTENT),
                ignore_cache=self.args.ignore_cache,
                imghost=imghosts.imghost(
                    name=self.args.upload_to,
                    **self.config['imghosts'][self.args.upload_to],
                ),
            )
            # Timestamps are calculated in a subprocess, we have to wait for
            # that until we can set the number of expected screenhots.
            self.screenshots_job.signal.register(
                'timestamps',
                lambda timestamps: imghost_job.set_images_total(len(timestamps)),
            )
            # Pass ScreenshotsJob's output to ImageHostJob input.
            self.screenshots_job.signal.register('output', imghost_job.enqueue)
            # Tell imghost_job to finish the current upload and then finish.
            self.screenshots_job.signal.register('finished', imghost_job.finalize)
            return imghost_job

    @cached_property
    def jobs(self):
        return (
            self.screenshots_job,
            self.upload_screenshots_job,
        )


class upload_images(CommandBase):
    """Upload images to image hosting service"""

    names = ('upload-images', 'ui')

    @cached_property
    def jobs(self):
        return (
            _jobs.imghost.ImageHostJob(
                ignore_cache=self.args.ignore_cache,
                imghost=imghosts.imghost(
                    name=self.args.IMAGEHOST,
                    **self.config['imghosts'][self.args.IMAGEHOST],
                ),
                enqueue=self.args.IMAGE,
            ),
        )


class mediainfo(CommandBase):
    """
    Print mediainfo of first file with irrelevant paths removed

    Directories are recursively searched for the first video file in natural
    order, e.g. "File1.mp4" comes before "File10.mp4".

    Any irrelevant leading parts in the file path are removed from the output.
    """

    names = ('mediainfo', 'mi')

    @cached_property
    def jobs(self):
        return (
            _jobs.mediainfo.MediainfoJob(
                home_directory=fs.projectdir(self.args.CONTENT),
                ignore_cache=self.args.ignore_cache,
                content_path=self.args.CONTENT,
            ),
        )


class submit(CommandBase):
    """Generate all required metadata and upload to tracker"""

    names = ('submit',)

    @cached_property
    def jobs(self):
        submit_job = _jobs.submit.SubmitJob(
            home_directory=fs.projectdir(self.args.CONTENT),
            ignore_cache=self.args.ignore_cache,
            tracker=self.tracker,
            tracker_jobs=self.tracker_jobs,
        )
        return (
            tuple(self.tracker_jobs.jobs_before_upload)
            + (submit_job,)
            + tuple(self.tracker_jobs.jobs_after_upload)
        )

    @cached_property
    def tracker_name(self):
        """Lower-case abbreviation of tracker name"""
        return self.args.TRACKER.lower()

    @cached_property
    def tracker_config(self):
        """Dictionary of :attr:`tracker_name` section in trackers configuration file"""
        return self.config['trackers'][self.tracker_name]

    @cached_property
    def tracker(self):
        """
        :class:`~.trackers.base.TrackerBase` instance from one of the submodules of
        :mod:`.trackers`
        """
        return trackers.tracker(
            name=self.tracker_name,
            config=self.tracker_config,
        )

    @cached_property
    def tracker_jobs(self):
        """
        :class:`~.trackers.base.TrackerJobsBase` instance from one of the submodules
        of :mod:`.trackers`
        """
        return self.tracker.TrackerJobs(
            content_path=self.args.CONTENT,
            tracker=self.tracker,
            image_host=self._get_imghost(),
            bittorrent_client=self._get_btclient(),
            torrent_destination=self._get_torrent_destination(),
            common_job_args={
                'home_directory': fs.projectdir(self.args.CONTENT),
                'ignore_cache': self.args.ignore_cache,
            },
        )

    def _get_imghost(self):
        imghost_name = self.tracker_config.get('image_host', None)
        if imghost_name:
            return imghosts.imghost(
                name=imghost_name,
                **self.config['imghosts'][imghost_name],
            )

    def _get_btclient(self):
        btclient_name = (getattr(self.args, 'add_to', None)
                         or self.tracker_config.get('add-to', None)
                         or None)
        if btclient_name:
            return btclients.client(
                name=btclient_name,
                **self.config['clients'][btclient_name],
            )

    def _get_torrent_destination(self):
        return (getattr(self.args, 'copy_to', None)
                or self.tracker_config.get('copy-to', None)
                or None)

class set(CommandBase):
    """
    Change or show configuration file options

    Without any arguments, all options are listed with their current values.

    The first segment in the option name is the file name without the
    extension. The second segment is the section name in that file. The third
    segment is the option name.

    List values must be given as separate arguments. If non-list values are
    given as multiple arguments, they are concatenated with single spaces.
    """

    names = ('set',)

    @cached_property
    def jobs(self):
        return (
            _jobs.config.SetJob(
                config=self.config,
                option=self.args.OPTION,
                # VALUE is a list. The Config class should convert lists to
                # strings (and vice versa) depending on the default type.
                value=self.args.VALUE,
                reset=self.args.reset,
            ),
        )
