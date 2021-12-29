class ReportCreationError(Exception):
    pass


class DateFormatException(ReportCreationError):
    pass


class ReportCreationException(Exception):
    pass

class InsufficientTimeTrackingData(Exception):
    pass