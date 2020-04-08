# -*- coding: utf-8 -*-
import sys
import os
import multiprocessing
import threading
import _thread as thread
import time
import gc
from random import randint
import json
import math
from plup.indicators.Indicator import Indicator
from plup.Helpers.Vacuum import vacuum
from plup.Helpers.LogEvents import LogEvents
from django.db import transaction
from plup.models import Amenities

class Module:
    def __init__(self, user, scenario, extra_dict_arguments=None):
        self.__user = user
        self.__scenario = scenario

    def run(self):
        try:
            error = True
            count = 0
            while error and count < 3:
                self.__Indicator = Indicator(self.__user)
                db = self.__Indicator.get_up_calculator_connection()
                try:
                    amenity_classes = []
                    amenity_classes.append("high_school_capacity")
                    amenity_classes_array="'{"+",".join(amenity_classes)+"}'"
                    query = """
                        select urbper_indicator_high_school_capacity({scenario},'highschool_capacity'::varchar(30),{fclass_array})
                            """.format(scenario=self.__scenario, fclass_array=amenity_classes_array)
                    LogEvents(
                        "highschool capacity",
                        "highschool capacity module started: " + query,
                        self.__scenario,
                        self.__user
                    )
                    with transaction.atomic():
                        db.execute(query)
                except Exception as e:
                    error = True
                    count += 1
                    time.sleep(randint(1, 3))
                    db.close()
                    LogEvents(
                        "highschool capacity",
                        "highschool capacity module failed " +
                        str(count) + ": " + str(e) ,
                        self.__scenario,
                        self.__user
                    )
                else:
                    error = False
                    db.close()
                    LogEvents(
                        "highschool capacity",
                        "highschool capacity module finished",
                        self.__scenario,
                        self.__user
                    )
        except Exception as e:
            LogEvents(
                "highschool capacity",
                "unknown error " +
                str(e),
                self.__scenario,
                self.__user
            )
