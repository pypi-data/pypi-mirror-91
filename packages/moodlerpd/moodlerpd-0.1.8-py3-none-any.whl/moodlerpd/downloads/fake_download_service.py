import os
import platform
import logging
from pathlib import Path

from moodlerpd.state.course import Course
from moodlerpd.utils.path_tools import PathTools
from moodlerpd.downloads.download_service import DownloadService
from moodlerpd.client.client_service import ClientService


class FakeDownloadService:
    """
    FakeDownloadService fakes a DownloadService.
    This way a local database of Moodle's current files
    can be created without actually downloading the files.
    """

    def __init__(self, courses: [Course], client_service: ClientService, storage_path: str):
        """
        Initiates the FakeDownloadService with all files that
        need to be downloaded (saved in the database).
        @param courses: A list of courses that contains all modified files.
        @param client_service: A reference to the moodle_service, currently
                               only to get to the state_recorder.
        @param storage_path: The location where the files would be saved.
        """

        self.courses = courses
        self.state_recorder = client_service.recorder
        self.storage_path = storage_path

        # delete files, that should be deleted
        self.state_recorder.batch_delete_files(self.courses)

        # Prepopulate queue with any files that were given
        for course in self.courses:
            for file in course.files:
                if file.deleted is False:

                    save_destination = DownloadService.gen_path(self.storage_path, course, file)

                    filename = PathTools.to_valid_name(file.content_filename)

                    file.saved_to = str(Path(save_destination) / filename)

                    if file.module_modname.startswith('url'):
                        file.saved_to = str(Path(save_destination) / (filename + '.desktop'))
                        if os.name == 'nt' or platform.system() == "Darwin":
                            file.saved_to = str(Path(save_destination) / (filename + '.URL'))

                    if file.content_type == 'description':
                        file.saved_to = str(Path(save_destination) / (filename + '.md'))

                    self.state_recorder.save_file(file, course.id, course.fullname)

    @staticmethod
    def run():
        """Dummy function"""
        logging.info('All files stored in the Database!')
