import json
import pickle
import sys
import numpy as np
import requests
from collections import ChainMap

# source: https://github.com/mpld3/mpld3/issues/434#issuecomment-340255689
# fix for the NumPy array is not JSON serializable
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj: object) -> None:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class Grader:
    """Student side grader class
    ...
    Attributes
    ----------
    submission_url : str
        API url to fetch data
    assignmentKey : str
        test-case filename
    cases : dict
        Contains data to be validated with test case functions
    Methods
    -------
    add_case(test_key_value)
        Saves assignemnt result on the cases variable
    submit("email","token")
        Send email and session token along with
        student assignment result in parts variableW
        and filename of test case in assignmentKey variable
    """

    def __init__(self, assignment_key: str, submission_url: str) -> None:
        self.submission_url = submission_url
        self.assignment_key = assignment_key
        self.cases: dict = {}
        self.errors: list = []

    def __validate(self):
        errors: list = []
        try:
            assert type(self.submission_url) == str, "Invalid submission URL."
            assert type(self.assignment_key) == str, "Invalid assignment key."
            assert len(self.assignment_key) > 1, "Invalid assignment key."
            assert "http" in self.submission_url, "Invalid submission URL."
            assert type(self.cases) == dict, "Invalid test data."

        except AssertionError as e:
            errors.append(e)
        return errors

    def add_case(self, test_key_value: dict) -> None:
        try:
            assert isinstance(test_key_value, dict), "Invalid test data."
            key_of_function = list(test_key_value.keys())[0]
            key_of_function_val = list(test_key_value.values())[0]
            assert key_of_function_val is not None, "Invalid test case values."
            assert isinstance(
                key_of_function_val, dict
            ), "Test case values should be dict."
            assert (
                len(key_of_function_val) > 0
            ), "Test case values should be non empty dict."
            assert isinstance(key_of_function, str), "Invalid test case name."
            self.cases[key_of_function] = key_of_function_val

        except AssertionError as e:
            sys.stdout.write(str(e))
            return False

    def submit(self, email: str, token: str) -> str:
        errors = self.__validate()
        if errors:
            return {"Error": [x for x in errors]}

        submission = {
            "assignment_key": self.assignment_key,
            "student_email": email,
            "secret": token,
            "parts": [self.cases],
        }

        try:
            request = requests.post(
                self.submission_url,
                data=json.dumps(submission, cls=NumpyEncoder),
                headers={"content-type": "application/json"},
            )

            # get response form api
            response = request.json()
            response = response["msg"]
            sys.stdout.write(str(response))
            return "Now you can check your submission status."

        except Exception as e:
            sys.stdout.write("There was an error on the server:" + str(e))
            return "Please re-submit the assignment or contact the administrator."

    def make_pickle(self):
        pickle_file = dict(ChainMap(*list(self.cases.values())))
        with open(self.assignment_key + "-source" + ".pkl", "wb") as f:
            pickle.dump(pickle_file, f)
