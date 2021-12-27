import datetime
import logging
import os
import shutil
from typing import Type

from databases.database import Database


class Backup:

    def __init__(self, logger: logging.Logger, original_file_path: str, backup_dir_name: str = "Backup",
                 date_format: str = "%Y-%m-%d %H%M%S") -> None:
        """
        A class that can create backups of files

        logger -- a logger that allows for logging the success or failure of creating the backup
        original_file_path -- the path to the original file for which a backup is to be created
        backup_dir_name -- the name of the directory in which the backup of the original file is to be stored
        date_format -- the format with which the date which is part of the file_name for the backup will be formatted
        """

        self.logger = logger
        self.original_db_file_path = original_file_path
        self.original_db_file_name = os.path.split(original_file_path)[-1]
        self.original_db_path = os.path.dirname(original_file_path)

        self.date_format = date_format
        self.backup_dir = os.path.join(self.original_db_path, backup_dir_name)

    def create_backup(self) -> None:
        """Create a copy of the original database in the backup directory"""

        try:
            pre_01 = "Backup"
            pre_02 = datetime.datetime.now().strftime(self.date_format)
            file_name = f"{pre_01} {pre_02} {self.original_db_file_name}"
            destination = os.path.join(self.backup_dir, file_name)

            shutil.copy2(src=self.original_db_file_path, dst=destination)

        except Exception as e:
            self.logger.exception(f"Could not create backup for database {self.original_db_file_name}.")

        else:
            self.logger.info(f"Backup for {self.original_db_file_name} created under {destination}.")


if __name__ == '__main__':
    pass

