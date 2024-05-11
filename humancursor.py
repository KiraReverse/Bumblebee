import random
import math
import numpy as np
import pytweening
import time
from initinterception import move_to, mouse_position

import ctypes
import ctypes.wintypes

# These ctypes structures are for Win32 INPUT, MOUSEINPUT, KEYBDINPUT, and HARDWAREINPUT structures,
# used by SendInput and documented here: http://msdn.microsoft.com/en-us/library/windows/desktop/ms646270(v=vs.85).aspx
# Thanks to BSH for this StackOverflow answer: https://stackoverflow.com/questions/18566289/how-would-you-recreate-this-windows-api-structure-with-ctypes
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ('dx', ctypes.wintypes.LONG),
        ('dy', ctypes.wintypes.LONG),
        ('mouseData', ctypes.wintypes.DWORD),
        ('dwFlags', ctypes.wintypes.DWORD),
        ('time', ctypes.wintypes.DWORD),
        ('dwExtraInfo', ctypes.POINTER(ctypes.wintypes.ULONG)),
    ]
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ('wVk', ctypes.wintypes.WORD),
        ('wScan', ctypes.wintypes.WORD),
        ('dwFlags', ctypes.wintypes.DWORD),
        ('time', ctypes.wintypes.DWORD),
        ('dwExtraInfo', ctypes.POINTER(ctypes.wintypes.ULONG)),
    ]
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ('uMsg', ctypes.wintypes.DWORD),
        ('wParamL', ctypes.wintypes.WORD),
        ('wParamH', ctypes.wintypes.DWORD)
    ]
class INPUT(ctypes.Structure):
    class _I(ctypes.Union):
        _fields_ = [
            ('mi', MOUSEINPUT),
            ('ki', KEYBDINPUT),
            ('hi', HARDWAREINPUT),
        ]
    _anonymous_ = ('i', )
    _fields_ = [
        ('type', ctypes.wintypes.DWORD),
        ('i', _I),
    ]
# End of the SendInput win32 data structures.






class HumanizeMouseTrajectory:
    def __init__(self, from_point, to_point, **kwargs):
        self.from_point = from_point
        self.to_point = to_point
        self.points = self.generate_curve(**kwargs)

    def generate_curve(self, **kwargs):
        """Generates the curve based on arguments below, default values below are automatically modified to cause randomness"""
        offset_boundary_x = kwargs.get("offset_boundary_x", 80)
        offset_boundary_y = kwargs.get("offset_boundary_y", 80)
        left_boundary = (
            kwargs.get("left_boundary", min(self.from_point[0], self.to_point[0]))
            - offset_boundary_x
        )
        right_boundary = (
            kwargs.get("right_boundary", max(self.from_point[0], self.to_point[0]))
            + offset_boundary_x
        )
        down_boundary = (
            kwargs.get("down_boundary", min(self.from_point[1], self.to_point[1]))
            - offset_boundary_y
        )
        up_boundary = (
            kwargs.get("up_boundary", max(self.from_point[1], self.to_point[1]))
            + offset_boundary_y
        )
        knots_count = kwargs.get("knots_count", 2)
        distortion_mean = kwargs.get("distortion_mean", 1)
        distortion_st_dev = kwargs.get("distortion_st_dev", 1)
        distortion_frequency = kwargs.get("distortion_frequency", 0.5)
        tween = kwargs.get("tweening", pytweening.easeOutQuad)
        target_points = kwargs.get("target_points", 100)

        internalKnots = self.generate_internal_knots(
            left_boundary, right_boundary, down_boundary, up_boundary, knots_count
        )
        points = self.generate_points(internalKnots)
        points = self.distort_points(
            points, distortion_mean, distortion_st_dev, distortion_frequency
        )
        points = self.tween_points(points, tween, target_points)
        return points

    def generate_internal_knots(
        self, l_boundary, r_boundary, d_boundary, u_boundary, knots_count
    ):
        """Generates the internal knots of the curve randomly"""
        if not (
            self.check_if_numeric(l_boundary)
            and self.check_if_numeric(r_boundary)
            and self.check_if_numeric(d_boundary)
            and self.check_if_numeric(u_boundary)
        ):
            raise ValueError("Boundaries must be numeric values")
        if not isinstance(knots_count, int) or knots_count < 0:
            knots_count = 0
        if l_boundary > r_boundary:
            raise ValueError(
                "left_boundary must be less than or equal to right_boundary"
            )
        if d_boundary > u_boundary:
            raise ValueError(
                "down_boundary must be less than or equal to upper_boundary"
            )
        try:
            knotsX = np.random.choice(range(l_boundary, r_boundary) or l_boundary, size=knots_count)
            knotsY = np.random.choice(range(d_boundary, u_boundary) or d_boundary, size=knots_count)
        except TypeError:
            knotsX = np.random.choice(
                range(int(l_boundary), int(r_boundary)), size=knots_count
            )
            knotsY = np.random.choice(
                range(int(d_boundary), int(u_boundary)), size=knots_count
            )
        knots = list(zip(knotsX, knotsY))
        return knots

    def generate_points(self, knots):
        """Generates the points from BezierCalculator"""
        if not self.check_if_list_of_points(knots):
            raise ValueError("knots must be valid list of points")

        midPtsCnt = max(
            abs(self.from_point[0] - self.to_point[0]),
            abs(self.from_point[1] - self.to_point[1]),
            2,
        )
        knots = [self.from_point] + knots + [self.to_point]
        return BezierCalculator.calculate_points_in_curve(int(midPtsCnt), knots)

    def distort_points(
        self, points, distortion_mean, distortion_st_dev, distortion_frequency
    ):
        """Distorts points by parameters of mean, standard deviation and frequency"""
        if not (
            self.check_if_numeric(distortion_mean)
            and self.check_if_numeric(distortion_st_dev)
            and self.check_if_numeric(distortion_frequency)
        ):
            raise ValueError("Distortions must be numeric")
        if not self.check_if_list_of_points(points):
            raise ValueError("points must be valid list of points")
        if not (0 <= distortion_frequency <= 1):
            raise ValueError("distortion_frequency must be in range [0,1]")

        distorted = []
        for i in range(1, len(points) - 1):
            x, y = points[i]
            delta = (
                np.random.normal(distortion_mean, distortion_st_dev)
                if random.random() < distortion_frequency
                else 0
            )
            distorted += ((x, y + delta),)
        distorted = [points[0]] + distorted + [points[-1]]
        return distorted

    def tween_points(self, points, tween, target_points):
        """Modifies points by tween"""
        if not self.check_if_list_of_points(points):
            raise ValueError("List of points not valid")
        if not isinstance(target_points, int) or target_points < 2:
            raise ValueError("target_points must be an integer greater or equal to 2")

        res = []
        for i in range(target_points):
            index = int(tween(float(i) / (target_points - 1)) * (len(points) - 1))
            res += (points[index],)
        return res

    @staticmethod
    def check_if_numeric(val):
        """Checks if value is proper numeric value"""
        return isinstance(val, (float, int, np.int32, np.int64, np.float32, np.float64))

    def check_if_list_of_points(self, list_of_points):
        """Checks if list of points is valid"""
        if not isinstance(list_of_points, list):
            return False
        try:
            point = lambda p: (
                (len(p) == 2)
                and self.check_if_numeric(p[0])
                and self.check_if_numeric(p[1])
            )
            return all(map(point, list_of_points))
        except (KeyError, TypeError):
            return False


class BezierCalculator:
    @staticmethod
    def binomial(n, k):
        """Returns the binomial coefficient "n choose k" """
        return math.factorial(n) / float(math.factorial(k) * math.factorial(n - k))

    @staticmethod
    def bernstein_polynomial_point(x, i, n):
        """Calculate the i-th component of a bernstein polynomial of degree n"""
        return BezierCalculator.binomial(n, i) * (x**i) * ((1 - x) ** (n - i))

    @staticmethod
    def bernstein_polynomial(points):
        """
        Given list of control points, returns a function, which given a point [0,1] returns
        a point in the Bézier curve described by these points
        """

        def bernstein(t):
            n = len(points) - 1
            x = y = 0
            for i, point in enumerate(points):
                bern = BezierCalculator.bernstein_polynomial_point(t, i, n)
                x += point[0] * bern
                y += point[1] * bern
            return x, y

        return bernstein

    @staticmethod
    def calculate_points_in_curve(n, points):
        """
        Given list of control points, returns n points in the Bézier curve,
        described by these points
        """
        curvePoints = []
        bernstein_polynomial = BezierCalculator.bernstein_polynomial(points)
        for i in range(n):
            t = i / (n - 1)
            curvePoints += (bernstein_polynomial(t),)
        return curvePoints











#############################################################################################











# import math
# from selenium.webdriver import Chrome, Edge, Firefox, Safari
# import pytweening
# import random


def calculate_absolute_offset(element, list_of_x_and_y_offsets):
    """Calculates exact number of pixel offsets from relative values"""
    dimensions = element.size
    width, height = dimensions["width"], dimensions["height"]
    x_final = width * list_of_x_and_y_offsets[0]
    y_final = height * list_of_x_and_y_offsets[1]

    return [int(x_final), int(y_final)]


def generate_random_curve_parameters(driver, pre_origin, post_destination):
    """Generates random parameters for the curve, the tween, number of knots, distortion, target points and boundaries"""
    web = False
    # if isinstance(driver, (Chrome, Firefox, Edge, Safari)):
    #     web = True
    #     viewport_width, viewport_height = driver.get_window_size().values()
    # else:
        # viewport_width, viewport_height = driver.size()
    viewport_width, viewport_height = driver.size()
    min_width, max_width = viewport_width * 0.15, viewport_width * 0.85
    min_height, max_height = viewport_height * 0.15, viewport_height * 0.85

    tween_options = [
        pytweening.easeOutExpo,
        pytweening.easeInOutQuint,
        pytweening.easeInOutSine,
        pytweening.easeInOutQuart,
        pytweening.easeInOutExpo,
        pytweening.easeInOutCubic,
        pytweening.easeInOutCirc,
        pytweening.linear,
        pytweening.easeOutSine,
        pytweening.easeOutQuart,
        pytweening.easeOutQuint,
        pytweening.easeOutCubic,
        pytweening.easeOutCirc,
    ]

    tween = random.choice(tween_options)
    offset_boundary_x = random.choice(
        random.choices(
            [range(20, 45), range(45, 75), range(75, 100)], [0.2, 0.65, 15]
        )[0]
    )
    offset_boundary_y = random.choice(
        random.choices(
            [range(20, 45), range(45, 75), range(75, 100)], [0.2, 0.65, 15]
        )[0]
    )
    knots_count = random.choices(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [0.15, 0.36, 0.17, 0.12, 0.08, 0.04, 0.03, 0.02, 0.015, 0.005],
    )[0]

    distortion_mean = random.choice(range(80, 110)) / 100
    distortion_st_dev = random.choice(range(85, 110)) / 100
    distortion_frequency = random.choice(range(25, 70)) / 100

    if web:
        target_points = random.choice(
            random.choices(
                [range(35, 45), range(45, 60), range(60, 80)], [0.53, 0.32, 0.15]
            )[0]
        )
    else:
        target_points = max(int(math.sqrt((pre_origin[0] - post_destination[0]) ** 2 + (pre_origin[1] - post_destination[1]) ** 2)), 2)

    if (
            min_width > pre_origin[0]
            or max_width < pre_origin[0]
            or min_height > pre_origin[1]
            or max_height < pre_origin[1]
    ):
        offset_boundary_x = 0
        offset_boundary_y = 0
        knots_count = 1
    if (
            min_width > post_destination[0]
            or max_width < post_destination[0]
            or min_height > post_destination[1]
            or max_height < post_destination[1]
    ):
        offset_boundary_x = 0
        offset_boundary_y = 0
        knots_count = 1

    return (
        offset_boundary_x,
        offset_boundary_y,
        knots_count,
        distortion_mean,
        distortion_st_dev,
        distortion_frequency,
        tween,
        target_points,
    )











#######################################################################################################



from time import sleep
# import random
import pyautogui
from typing import List, Tuple

# from humancursor.utilities.human_curve_generator import HumanizeMouseTrajectory
# from humancursor.utilities.calculate_and_randomize import generate_random_curve_parameters



class SystemCursor:
    def __init__(self):
        pyautogui.MINIMUM_DURATION = 0
        pyautogui.MINIMUM_SLEEP = 0
        pyautogui.PAUSE = 0
        self.GLOBALPAUSE = 0

    # @staticmethod
    # def move_to(point: list or tuple, duration: int or float = None, human_curve=None, steady=False):
    def move_to(self, point: list or tuple, duration: int or float = None, human_curve=None, steady=False):
        """Moves to certain coordinates of screen"""
        from_point = pyautogui.position()

        if not human_curve:
            (
                offset_boundary_x,
                offset_boundary_y,
                knots_count,
                distortion_mean,
                distortion_st_dev,
                distortion_frequency,
                tween,
                target_points,
            ) = generate_random_curve_parameters(
                pyautogui, from_point, point
            )
            if steady:
                offset_boundary_x, offset_boundary_y = 10, 10
                distortion_mean, distortion_st_dev, distortion_frequency = 1.2, 1.2, 1
            human_curve = HumanizeMouseTrajectory(
                from_point,
                point,
                offset_boundary_x=offset_boundary_x,
                offset_boundary_y=offset_boundary_y,
                knots_count=knots_count,
                distortion_mean=distortion_mean,
                distortion_st_dev=distortion_st_dev,
                distortion_frequency=distortion_frequency,
                tween=tween,
                target_points=target_points,
            )

        if duration is None:
            # duration = random.uniform(0.5, 2.0)
            # duration = random.uniform(0.5, 1.1)
            duration = random.uniform(0.3, .6)
            print(f'{duration=}')
            # duration = random.uniform(1.99, 2.0)
        # pyautogui.PAUSE = duration / len(human_curve.points)
        self.GLOBALPAUSE = duration / len(human_curve.points)
        # pyautogui.PAUSE = 0.1
        # print(len(human_curve.points))
        for pnt in human_curve.points:
            # pyautogui.moveTo(pnt)
            self.moveTo(pnt)
        # pyautogui.moveTo(point)
        self.moveTo(point)

    def click_on(self, point: list or tuple, clicks: int = 1, click_duration: int or float = 0, steady=False):
        """Clicks a specified number of times, on the specified coordinates"""
        self.move_to(point, steady=steady)
        for _ in range(clicks):
            # pyautogui.mouseDown()
            sleep(click_duration)
            # pyautogui.mouseUp()
            sleep(random.uniform(0.170, 0.280))

    def drag_and_drop(self, from_point: list or tuple, to_point: list or tuple, duration: int or float or List[float, float] or Tuple(float, float) = None, steady=False):
        """Drags from a certain point, and releases to another"""
        if isinstance(duration, (list, tuple)):
            first_duration, second_duration = duration
        elif isinstance(duration, (float, int)):
            first_duration = second_duration = duration / 2
        else:
            first_duration = second_duration = None

        self.move_to(from_point, duration=first_duration)
        # pyautogui.mouseDown()
        self.move_to(to_point, duration=second_duration, steady=steady)
        # pyautogui.mouseUp()

    def moveTo(self, pnt):
        pntx, pnty = int(pnt[0]), int(pnt[1])
        time.sleep(self.GLOBALPAUSE)
        move_to(pntx,pnty)

    def moveTo2(self, pnt):
        pntx, pnty = int(pnt[0]), int(pnt[1])
        time.sleep(self.GLOBALPAUSE)
        # _mouseMoveDrag("move", x, y, 0, 0, duration, tween)        
        # If the duration is small enough, just move the cursor there instantly.
        # steps = [(x, y)]
        # if duration > MINIMUM_DURATION:
        #     # Non-instant moving/dragging involves tweening:
        #     num_steps = max(width, height)
        #     sleep_amount = duration / num_steps
        #     if sleep_amount < MINIMUM_SLEEP:
        #         num_steps = int(duration / MINIMUM_SLEEP)
        #         sleep_amount = duration / num_steps
            # steps = [getPointOnLine(startx, starty, x, y, tween(n / num_steps)) for n in range(num_steps)]
            # Making sure the last position is the actual destination.
            # steps.append((x, y))
        # for tweenX, tweenY in steps:
            # if len(steps) > 1:
            #     # A single step does not require tweening.
            #     time.sleep(sleep_amount)

            # tweenX = int(round(tweenX))
            # tweenY = int(round(tweenY))

            # Do a fail-safe check to see if the user moved the mouse to a fail-safe position, but not if the mouse cursor
            # moved there as a result of this function. (Just because tweenX and tweenY aren't in a fail-safe position
            # doesn't mean the user couldn't have moved the mouse cursor to a fail-safe position.)
            # if (tweenX, tweenY) not in FAILSAFE_POINTS:
            #     failSafeCheck()

            # if moveOrDrag == "move":
            #     platformModule._moveTo(tweenX, tweenY)
            # elif moveOrDrag == "drag":
            #     platformModule._dragTo(tweenX, tweenY, button)
            # else:
            #     raise NotImplementedError("Unknown value of moveOrDrag: {0}".format(moveOrDrag))
        ctypes.windll.user32.SetCursorPos(pntx, pnty)        
        # pyautogui.leftClick(tweenX,tweenY)
        x,y=pyautogui.position()
        # width, height = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
        width, height = 1920, 1080
        convertedX = 65536 * x // width + 1
        convertedY = 65536 * y // height + 1
        ctypes.windll.user32.mouse_event(0x0002, ctypes.c_long(convertedX), ctypes.c_long(convertedY), 0, 0)
        time.sleep(.0001)
        ctypes.windll.user32.mouse_event(0x0004, ctypes.c_long(convertedX), ctypes.c_long(convertedY), 0, 0)
        time.sleep(.0001)