import sys
import shutil
import logging

from pathlib import Path
from getpass import getpass
from urllib.parse import urlparse
from distutils.version import StrictVersion

from yt_dlp.utils import determine_ext

from moodle_dl.utils import cutie
from moodle_dl.utils.logger import Log
from moodle_dl.config_service.config_helper import ConfigHelper
from moodle_dl.state_recorder.course import Course
from moodle_dl.state_recorder.state_recorder import StateRecorder
from moodle_dl.moodle_connector import login_helper
from moodle_dl.moodle_connector import sso_token_receiver
from moodle_dl.moodle_connector.cookie_handler import CookieHandler
from moodle_dl.moodle_connector.results_handler import ResultsHandler
from moodle_dl.moodle_connector.pages_handler import PagesHandler
from moodle_dl.moodle_connector.forums_handler import ForumsHandler
from moodle_dl.moodle_connector.folders_handler import FoldersHandler
from moodle_dl.moodle_connector.quizzes_handler import QuizzesHandler
from moodle_dl.moodle_connector.lessons_handler import LessonsHandler
from moodle_dl.moodle_connector.workshops_handler import WorkshopsHandler
from moodle_dl.moodle_connector.databases_handler import DatabasesHandler
from moodle_dl.moodle_connector.assignments_handler import AssignmentsHandler
from moodle_dl.moodle_connector.first_contact_handler import FirstContactHandler
from moodle_dl.moodle_connector.request_helper import RequestRejectedError, RequestHelper


class MoodleService:
    def __init__(
        self,
        config_helper: ConfigHelper,
        storage_path: str,
        skip_cert_verify: bool = False,
        log_responses: bool = False,
    ):
        self.config_helper = config_helper
        self.storage_path = storage_path
        self.recorder = StateRecorder(Path(storage_path) / 'moodle_state.db')
        self.skip_cert_verify = skip_cert_verify

        self.log_responses_to = None
        if log_responses:
            self.log_responses_to = str(Path(storage_path) / 'responses.log')

    def interactively_acquire_token(
        self, use_stored_url: bool = False, username: str = None, password: str = None
    ) -> str:
        """
        Walks the user through executing a login into the Moodle-System to get
        the Token and saves it.
        @return: The Token for Moodle.
        """

        automated = False
        stop_automatic_generation = False
        if username is not None and password is not None:
            automated = True

        if not automated:
            print('[The following Credentials are not saved, it is only used temporarily to generate a login token.]')

        moodle_token = None
        while moodle_token is None:
            if stop_automatic_generation and automated:
                break

            if not use_stored_url:
                moodle_url = input('URL of Moodle:   ')

                use_http = False
                if moodle_url.startswith('http://'):
                    Log.error(
                        'Warning: You have entered an insecure URL! Are you sure that the Moodle is'
                        + ' not accessible via `https://`? All your data will be transferred'
                        + ' insecurely! If your Moodle is accessible via `https://`, then run'
                        + ' the process again using `https://` to protect your data.'
                    )
                    use_http = True
                elif not moodle_url.startswith('https://'):
                    Log.error('The url of your moodle must start with `https://`')
                    continue

                moodle_uri = urlparse(moodle_url)

                moodle_domain, moodle_path = self._split_moodle_uri(moodle_uri)

            else:
                moodle_domain = self.config_helper.get_moodle_domain()
                moodle_path = self.config_helper.get_moodle_path()
                use_http = self.config_helper.get_use_http()

            if username is not None:
                moodle_username = username
                stop_automatic_generation = True
            else:
                moodle_username = input('Username for Moodle:   ')

            if password is not None:
                moodle_password = password
            else:
                moodle_password = getpass('Password for Moodle [no output]:   ')

            try:
                moodle_token, moodle_privatetoken = login_helper.obtain_login_token(
                    moodle_username,
                    moodle_password,
                    moodle_domain,
                    moodle_path,
                    self.skip_cert_verify,
                    use_http,
                )

            except RequestRejectedError as error:
                Log.error(f'Login Failed! ({error}) Please try again.')
            except (ValueError, RuntimeError) as error:
                Log.error(f'Error while communicating with the Moodle System! ({error}) Please try again.')
            except ConnectionError as error:
                Log.error(str(error))

        if automated is True and moodle_token is None:
            sys.exit(1)

        # Saves the created token and the successful Moodle parameters.
        self.config_helper.set_property('token', moodle_token)
        if moodle_privatetoken is not None:
            self.config_helper.set_property('privatetoken', moodle_privatetoken)
        self.config_helper.set_property('moodle_domain', moodle_domain)
        self.config_helper.set_property('moodle_path', moodle_path)
        if use_http is True:
            self.config_helper.set_property('use_http', use_http)

        return moodle_token

    def interactively_acquire_sso_token(self, use_stored_url: bool = False) -> str:
        """
        Walks the user through the receiving of a SSO token for the
        Moodle-System and saves it.
        @return: The Token for Moodle.
        """
        if not use_stored_url:

            moodle_url = input('URL of Moodle:   ')

            moodle_uri = urlparse(moodle_url)

            moodle_domain, moodle_path = self._split_moodle_uri(moodle_uri)

        else:
            moodle_domain = self.config_helper.get_moodle_domain()
            moodle_path = self.config_helper.get_moodle_path()

        use_http = self.config_helper.get_use_http()
        scheme = 'https://'
        if use_http:
            scheme = 'http://'

        atomatic_procedure_warning = (
            'Between version 3.8.1 and 3.8.2 a change was added to'
            + ' Moodle so that automatic copying of the SSO token'
            + ' might not work.'
        )
        allow_automatic = True
        try:
            version = RequestHelper(
                moodle_domain,
                moodle_path,
                skip_cert_verify=self.skip_cert_verify,
                use_http=use_http,
            ).get_simple_moodle_version()

            if StrictVersion(version) > StrictVersion("3.8.1") and StrictVersion(version) <= StrictVersion("3.8.2"):
                Log.warning(atomatic_procedure_warning + '\nYou can still try it, your version is: ' + str(version))
            if StrictVersion(version) > StrictVersion("3.8.2"):
                Log.warning(
                    'For your Moodle version there is currently no automatic way to copy the SSO token implemented,'
                    + f' your version is: {str(version)}. You will have to proceed manually.'
                )
                allow_automatic = False

        except ConnectionError:
            Log.warning(
                atomatic_procedure_warning
                + '\nThe version of your Moodle could not be detected, you can still try the automatic procedure.'
            )

        do_automatic = False
        if allow_automatic:
            print(' If you want to copy the login-token manual, you will be guided through the manual copy process.')
            do_automatic = cutie.prompt_yes_or_no('Do you want to try to receive the SSO token automatically?')

        print('Please log into Moodle on this computer and then visit the following address in your web browser: ')

        if do_automatic:
            print(
                scheme
                + moodle_domain
                + moodle_path
                + 'admin/tool/mobile/launch.php?service='
                + 'moodle_mobile_app&passport=12345&'
                + 'urlscheme=http%3A%2F%2Flocalhost'
            )
            moodle_token = sso_token_receiver.receive_token()
        else:
            print(
                scheme
                + moodle_domain
                + moodle_path
                + 'admin/tool/mobile/launch.php?service='
                + 'moodle_mobile_app&passport=12345&urlscheme=moodledownloader'
            )

            print(
                'If you open the link in the browser, no web page should'
                + ' load, instead an error will occur. Open the'
                + ' developer console (press F12) and go to the Network Tab,'
                + ' if there is no error, reload the web page.'
            )

            print(
                'Copy the link address of the website that could not be'
                + ' loaded (right click, then click on Copy, then click'
                + ' on copy link address).'
            )

            print(
                'The script expects a URL that looks something like this:'
                + '`moodledownloader://token=$apptoken`.'
                + ' Where $apptoken looks random. In reality it is a Base64'
                + ' encoded hash and the token we need to access moodle.'
            )

            token_address = input('Then insert the address here:   ')

            moodle_token, moodle_privatetoken = sso_token_receiver.extract_token(token_address)
            if moodle_token is None:
                raise ValueError('Invalid URL!')

        # Saves the created token and the successful Moodle parameters.
        self.config_helper.set_property('token', moodle_token)
        if moodle_privatetoken is not None:
            self.config_helper.set_property('privatetoken', moodle_privatetoken)
        self.config_helper.set_property('moodle_domain', moodle_domain)
        self.config_helper.set_property('moodle_path', moodle_path)

        return moodle_token

    def fetch_state(self) -> [Course]:
        """
        Gets the current status of the configured Moodle account and compares
        it with the last known status for changes. It does not change the
        known state, nor does it download the files.
        @return: List with detected changes
        """
        logging.debug('Fetching current Moodle State...')

        token = self.config_helper.get_token()
        privatetoken = self.config_helper.get_privatetoken()
        moodle_domain = self.config_helper.get_moodle_domain()
        moodle_path = self.config_helper.get_moodle_path()
        use_http = self.config_helper.get_use_http()

        request_helper = RequestHelper(
            moodle_domain,
            moodle_path,
            token,
            self.skip_cert_verify,
            self.log_responses_to,
            use_http,
        )
        first_contact_handler = FirstContactHandler(request_helper)
        results_handler = ResultsHandler(request_helper, moodle_domain, moodle_path)

        download_course_ids = self.config_helper.get_download_course_ids()
        download_public_course_ids = self.config_helper.get_download_public_course_ids()
        dont_download_course_ids = self.config_helper.get_dont_download_course_ids()
        download_submissions = self.config_helper.get_download_submissions()
        download_databases = self.config_helper.get_download_databases()
        download_forums = self.config_helper.get_download_forums()
        download_quizzes = self.config_helper.get_download_quizzes()
        download_lessons = self.config_helper.get_download_lessons()
        download_workshops = self.config_helper.get_download_workshops()
        download_also_with_cookie = self.config_helper.get_download_also_with_cookie()

        courses = []
        filtered_courses = []
        cookie_handler = None

        print('\rDownloading account information\033[K', end='')

        userid, version = self.config_helper.get_userid_and_version()
        if userid is None or version is None:
            userid, version = first_contact_handler.fetch_userid_and_version()
        else:
            first_contact_handler.version = version
        assignments_handler = AssignmentsHandler(request_helper, version)
        databases_handler = DatabasesHandler(request_helper, version)
        forums_handler = ForumsHandler(request_helper, version)
        quizzes_handler = QuizzesHandler(request_helper, version)
        lessons_handler = LessonsHandler(request_helper, version)
        workshops_handler = WorkshopsHandler(request_helper, version)
        pages_handler = PagesHandler(request_helper, version)
        folders_handler = FoldersHandler(request_helper, version)

        results_handler.setVersion(version)

        if download_also_with_cookie:
            # generate a new cookie if necessary
            cookie_handler = CookieHandler(request_helper, version, self.storage_path)
            cookie_handler.check_and_fetch_cookies(privatetoken, userid)

        courses_list = first_contact_handler.fetch_courses(userid)
        courses = []
        # Filter unselected courses
        for course in courses_list:
            if ResultsHandler.should_download_course(course.id, download_course_ids, dont_download_course_ids):
                courses.append(course)

        public_courses_list = first_contact_handler.fetch_courses_info(download_public_course_ids)
        for course in public_courses_list:
            courses.append(course)

        assignments = assignments_handler.fetch_assignments(courses)
        if download_submissions:
            assignments = assignments_handler.fetch_submissions(userid, assignments)

        databases = databases_handler.fetch_databases(courses)
        if download_databases:
            databases = databases_handler.fetch_database_files(databases)

        forums = forums_handler.fetch_forums(courses)
        if download_forums:
            last_timestamps_per_forum = self.recorder.get_last_timestamps_per_forum()
            forums = forums_handler.fetch_forums_posts(forums, last_timestamps_per_forum)

        quizzes = quizzes_handler.fetch_quizzes(courses)
        if download_quizzes:
            quizzes = quizzes_handler.fetch_quizzes_files(userid, quizzes)

        lessons = lessons_handler.fetch_lessons(courses)
        if download_lessons:
            lessons = lessons_handler.fetch_lessons_files(userid, lessons)

        workshops = workshops_handler.fetch_workshops(courses)
        if download_workshops:
            workshops = workshops_handler.fetch_workshops_files(userid, workshops)

        pages = pages_handler.fetch_pages(courses)

        folders = folders_handler.fetch_folders(courses)

        courses = self.add_options_to_courses(courses)
        index = 0
        for course in courses:
            index += 1

            # to limit the output to one line
            limits = shutil.get_terminal_size()

            shorted_course_name = course.fullname
            if len(course.fullname) > 17:
                shorted_course_name = course.fullname[:15] + '..'

            into = '\rDownloading course information'

            status_message = into + f' {index:3d}/{len(courses):3d} [{shorted_course_name:<17}|{course.id:6}]'

            if len(status_message) > limits.columns:
                status_message = status_message[0 : limits.columns]

            print(status_message + '\033[K', end='')

            course_fetch_addons = {
                'assign': assignments.get(course.id, {}),
                'data': databases.get(course.id, {}),
                'forum': forums.get(course.id, {}),
                'quiz': quizzes.get(course.id, {}),
                'lesson': lessons.get(course.id, {}),
                'workshop': workshops.get(course.id, {}),
                'page': pages.get(course.id, {}),
                'folder': folders.get(course.id, {}),
            }
            results_handler.set_fetch_addons(course_fetch_addons)
            course.files = results_handler.fetch_files(course)

            filtered_courses.append(course)
        print('')

        logging.debug('Checking for changes...')
        changes = self.recorder.changes_of_new_version(filtered_courses)

        # Filter changes
        changes = self.add_options_to_courses(changes)
        changes = self.filter_courses(changes, self.config_helper, cookie_handler, courses_list + public_courses_list)

        return changes

    def add_options_to_courses(self, courses: [Course]):
        """
        Updates a array of courses with its options
        """
        options_of_courses = self.config_helper.get_options_of_courses()
        for course in courses:
            options = options_of_courses.get(str(course.id), None)
            if options is not None:
                course.overwrite_name_with = options.get('overwrite_name_with', None)
                course.create_directory_structure = options.get('create_directory_structure', True)
                course.excluded_sections = options.get("excluded_sections", [])

        return courses

    @staticmethod
    def filter_courses(
        changes: [Course],
        config_helper: ConfigHelper,
        cookie_handler: CookieHandler = None,
        courses_list: [Course] = None,
    ) -> [Course]:
        """
        Filters the changes course list from courses that
        should not get downloaded
        @param config_helper: ConfigHelper to obtain all the diffrent filter configs
        @param cookie_handler: CookieHandler to check if the cookie is valid
        @param courses_list: A list of all courses that are available online
        @return: filtered changes course list
        """

        download_course_ids = config_helper.get_download_course_ids()
        download_public_course_ids = config_helper.get_download_public_course_ids()
        dont_download_course_ids = config_helper.get_dont_download_course_ids()
        download_submissions = config_helper.get_download_submissions()
        download_descriptions = config_helper.get_download_descriptions()
        download_links_in_descriptions = config_helper.get_download_links_in_descriptions()
        download_databases = config_helper.get_download_databases()
        download_quizzes = config_helper.get_download_quizzes()
        download_lessons = config_helper.get_download_lessons()
        download_workshops = config_helper.get_download_workshops()
        exclude_file_extensions = config_helper.get_exclude_file_extensions()
        download_also_with_cookie = config_helper.get_download_also_with_cookie()
        if cookie_handler is not None:
            download_also_with_cookie = cookie_handler.test_cookies()

        filtered_changes = []

        for course in changes:
            if not ResultsHandler.should_download_course(
                course.id, download_course_ids + download_public_course_ids, dont_download_course_ids
            ):
                # Filter courses that should not be downloaded
                continue

            if courses_list is not None:
                not_online = True
                # Filter courses that are not available online
                for online_course in courses_list:
                    if online_course.id == course.id:
                        not_online = False
                        break
                if not_online:
                    Log.warning(f'The Moodle course with id {course.id} is no longer available online.')
                    logging.warning('The Moodle course with id %d is no longer available online.', course.id)
                    continue

            course_files = []
            for file in course.files:
                # Filter Files based on options
                if (
                    # Filter Assignment Submission Files
                    (download_submissions or (not (file.module_modname.endswith('assign') and file.deleted)))
                    # Filter Description Files (except the forum posts)
                    and (
                        download_descriptions
                        or file.content_type != 'description'
                        or (
                            file.module_modname == 'forum'
                            and file.content_type == 'description'
                            and file.content_filename != 'Forum intro'
                        )
                    )
                    # Filter Database Files
                    and (download_databases or file.content_type != 'database_file')
                    # Filter Quiz Files
                    and (download_quizzes or (not (file.module_modname.endswith('quiz') and file.deleted)))
                    # Filter Lesson Files
                    and (download_lessons or (not (file.module_modname.endswith('lesson') and file.deleted)))
                    # Filter Workshops Files
                    and (download_workshops or (not (file.module_modname.endswith('workshop') and file.deleted)))
                    # Filter Files that requiere a Cookie
                    and (download_also_with_cookie or (not file.module_modname.startswith('cookie_mod-')))
                    # Exclude files whose file extension is blacklisted
                    and (determine_ext(file.content_filename) not in exclude_file_extensions)
                    # Exclude files that are in excluded sections
                    and (ResultsHandler.should_download_section(file.section_id, course.excluded_sections))
                ):
                    course_files.append(file)
            course.files = course_files

            # Filter Description URLs
            course_files = []
            for file in course.files:
                if not file.content_type == 'description-url':
                    course_files.append(file)

                elif download_links_in_descriptions:
                    add_description_url = True
                    for test_file in course.files:
                        if file.content_fileurl == test_file.content_fileurl:
                            if test_file.content_type != 'description-url':
                                # If a URL in a description also exists as a real link in the course,
                                # then ignore this URL
                                add_description_url = False
                                break
                            elif file.module_id > test_file.module_id:
                                # Always use the link from the older description.
                                add_description_url = False
                                break

                    if add_description_url:
                        course_files.append(file)
            course.files = course_files

            if len(course.files) > 0:
                filtered_changes.append(course)

        return filtered_changes

    @staticmethod
    def _split_moodle_uri(moodle_uri: str):
        """
        Splits a given Moodle-Uri into the domain and the installation path
        @return: moodle_domain, moodle_path as strings
        """

        moodle_domain = moodle_uri.netloc
        moodle_path = moodle_uri.path
        if not moodle_path.endswith('/'):
            moodle_path = moodle_path + '/'

        if moodle_path == '':
            moodle_path = '/'

        return moodle_domain, moodle_path
