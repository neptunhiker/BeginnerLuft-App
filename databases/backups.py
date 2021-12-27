


class Backup:

    def __init__(self, original_db_file_path: str, backup_dir: str = "Backup", date_format: str = "%Y-%m-%d %H:%M:%S"):
        self.original_db_file_path = original_db_file_path

        self.backup_dir = backup_dir
        self.date_format = date_format

    def create_backup(self):
        """Create a copy of the original database in the backup directory"""

        file_name = self.original_db_file_path.rfind()
