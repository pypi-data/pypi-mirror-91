from assertman.objects.assertable_string import AssertableString
from assertman.objects.assertable_list import AssertableList
from assertman.objects.assertable_dict import AssertableDict
from assertman.objects.assertable_int import AssertableInt
from assertman.objects.assertable_float import AssertableFloat
from assertman.objects.assertable_datetime import AssertableDatetime
from assertman.objects.assertable_bool import AssertableBool
import datetime


def make_assertable_object(arg):
    if isinstance(arg, (bool, AssertableBool)):
        return AssertableBool(arg)
    if isinstance(arg, str):
        return AssertableString(arg)
    elif isinstance(arg, int):
        return AssertableInt(arg)
    elif isinstance(arg, float):
        return AssertableFloat(arg)
    elif isinstance(arg, list):
        return AssertableList(arg)
    elif isinstance(arg, dict):
        return AssertableDict(arg)
    elif isinstance(arg, datetime.datetime):
        return AssertableDatetime(arg)
    raise ValueError(f"Для переданнного типа даннных <{type(arg)}> нет маппинга")