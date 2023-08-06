# -*- coding: utf-8 -*-

from requests import Response, Session


class SafeResponse(object):
    def __init__(self, success, response=None, session=None):
        self.__success: bool = success
        self.__response: Response = response
        self.__session: Session = session

    def __repr__(self):
        if self.success:
            status = "Success: %s" % self.response.status_code
        else:
            status = "Failed"
        return '<SafeResponse [%s]>' % status

    @property
    def success(self):
        return self.__success

    @property
    def response(self):
        if self.success:
            return self.__response
        else:
            return None

    @property
    def status_code(self):
        if self.success:
            return self.__response.status_code
        else:
            return None

    @property
    def session(self):
        if self.success:
            return self.__session
        else:
            return None


class StatusFilter(set):

    def interpret_options(self):
        """ Interpret option set
        1. Parse :class `range`
        2. Make positive list
            range(100,600) if len*(positive) == 0
        :return: positive-set, negative-set
        """
        positive = set()
        negative = set()
        for item in self:

            # Case <range item>
            if type(item) == range:
                if item.start + item.stop > 0:
                    positive |= set(item)
                else:
                    negative |= set(item)

            # Case <int item>
            elif type(item) == int:
                if item >= 100:
                    positive.add(item)
                elif item <= -100:
                    negative.add(item)

            else:
                raise ValueError("Interpret Failed")

        return positive, negative

    def pass_list(self):
        r""" Make include list from options

        :return: list `include list`
        :rtype: list
        """

        positive: set
        negative: set
        positive, negative = self.interpret_options()

        # If positive set is empty, make all-pass-set of status code
        if len(positive) == 0:
            positive = set(range(100, 600))

        # Exclude negative items
        for item in negative:
            while -item in positive:
                positive.remove(-item)

        return list(positive)

    def check(self, status_code):
        r""" Test :param `status_code` is pass

        :param status_code:
        :return: success or fail
        :rtype: bool
        """
        if status_code in self.pass_list():
            return True
        else:
            return False
