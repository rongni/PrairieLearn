import unittest
from types import FunctionType
from collections import namedtuple
from pl_helpers import (points, name, save_plot, print_student_code,
                        not_repeated)
from pl_execute import execute_code
from code_feedback import Feedback

# Needed to ensure matplotlib runs on Docker
import matplotlib
matplotlib.use('Agg')


class PrairieLearnTestCase(unittest.TestCase):

    include_plt = False
    student_code_string = 'test_print_student_code'
    student_code_file = 'user_code.py'
    iter_num = 0
    total_iters = 1

    @classmethod
    def setUpClass(cls):
        ref_result, student_result, plot_value = execute_code(
                                                     "filenames/ans.py",
                                                     cls.student_code_file,
                                                     cls.include_plt,
                                                     "output.txt",
                                                     cls.iter_num)
        answerTuple = namedtuple('answerTuple', ref_result.keys())
        cls.ref = answerTuple(**ref_result)
        studentTuple = namedtuple('studentTuple', student_result.keys())
        cls.st = studentTuple(**student_result)
        cls.plt = plot_value
        if cls.include_plt:
            cls.display_plot()


    @classmethod
    def tearDownClass(cls):
        if cls.include_plt:
            cls.plt.close('all')
        cls.iter_num += 1


    @classmethod
    def display_plot(cls):
        axes = cls.plt.gca()
        if axes.get_lines() \
          or axes.collections \
          or axes.patches \
          or axes.images:
            save_plot(cls.plt, cls.iter_num)


    @classmethod
    def get_total_points(cls):
        methods = [y for x, y in cls.__dict__.items()
                   if type(y == FunctionType) and
                      x.startswith('test_') and
                      'points' in y.__dict__]
        if cls.total_iters == 1:
            total = sum([m.__dict__['points'] for m in methods])
        else:
            once = sum([m.__dict__['points'] for m in methods
                       if not m.__dict__.get('__repeated__', True)])
            several = sum([m.__dict__['points'] for m in methods
                          if m.__dict__.get('__repeated__', True)])
            total = cls.total_iters*several + once
        return total


    def setUp(self):
        self.points = None
        Feedback.set_test(self)


    def run(self, result=None):
        test_id = self.id().split('.')[-1]
        if not result.done_grading or test_id == self.student_code_string:
            super(PrairieLearnTestCase, self).run(result)


    @not_repeated
    @points(0)
    @name('Student Code')
    def test_print_student_code(self):
        print_student_code(self.student_code_file)


class PrairieLearnTestCaseWithPlot(PrairieLearnTestCase):

    include_plt = True

    @name('Check plot labels')
    def optional_test_plot_labels(self):
        axes = self.plt.gca()
        title = axes.get_title()
        xlabel = axes.get_xlabel()
        ylabel = axes.get_ylabel()
        points = 0
        if xlabel:
            points += 0.333
            Feedback.add_feedback('Plot has xlabel')
        else:
            Feedback.add_feedback('Plot is missing xlabel')

        if title:
            points += 0.334
            Feedback.add_feedback('Plot has title')
        else:
            Feedback.add_feedback('Plot is missing title')

        if ylabel:
            points += 0.333
            Feedback.add_feedback('Plot has ylabel')
        else:
            Feedback.add_feedback('Plot is missing ylabel')

        Feedback.set_points(points)
