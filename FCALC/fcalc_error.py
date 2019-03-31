# coding: utf8

class Fcalc_error(Exception):
    def __init__(self, message):
        self.message = message
        def __str__(self):
            return self.message

class Fcalc_error_stacktoosmall(Fcalc_error):
    def __init__(self, nb_args, stack_len):
        self.message = "Stack too small : need %s vs %s in th stack."%(nb_args, stack_len)
