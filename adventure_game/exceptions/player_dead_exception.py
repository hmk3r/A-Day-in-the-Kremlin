class PlayerDeadException(Exception):

    def __init__(self, cause_of_death):
        message = "You're going to GULAG! {0}".format(cause_of_death)
        Exception.__init__(self, message)
