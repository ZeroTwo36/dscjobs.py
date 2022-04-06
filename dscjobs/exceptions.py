class DSCJobsBaseException(Exception):
    """
    Thrown if something went wrong.
    """

class MalformedRequest(DSCJobsBaseException):
    ...

class UserNotFound(DSCJobsBaseException):
    ...#("[DscJobs API] Hmm, Seems like we were unable to find that User! Please check the User ID and Try Again")

class NoReviewAvailable(DSCJobsBaseException):
    ...#("[DscJobs API] Hmm, Seems like that User does not have any Reviews Available!")
