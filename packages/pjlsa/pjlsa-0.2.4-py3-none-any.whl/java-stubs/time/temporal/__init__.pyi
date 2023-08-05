from typing import Any as _py_Any
from typing import List as _py_List
from typing import TypeVar as _py_TypeVar
from typing import Type as _py_Type
from typing import ClassVar as _py_ClassVar
from typing import Generic as _py_Generic
from typing import overload
import java.io
import java.lang
import java.time
import java.time.chrono
import java.time.format
import java.util
import java.util.function


class IsoFields:
    DAY_OF_QUARTER: _py_ClassVar['TemporalField'] = ...
    QUARTER_OF_YEAR: _py_ClassVar['TemporalField'] = ...
    WEEK_OF_WEEK_BASED_YEAR: _py_ClassVar['TemporalField'] = ...
    WEEK_BASED_YEAR: _py_ClassVar['TemporalField'] = ...
    WEEK_BASED_YEARS: _py_ClassVar['TemporalUnit'] = ...
    QUARTER_YEARS: _py_ClassVar['TemporalUnit'] = ...

class JulianFields:
    JULIAN_DAY: _py_ClassVar['TemporalField'] = ...
    MODIFIED_JULIAN_DAY: _py_ClassVar['TemporalField'] = ...
    RATA_DIE: _py_ClassVar['TemporalField'] = ...

class TemporalAccessor:
    def get(self, temporalField: 'TemporalField') -> int: ...
    def getLong(self, temporalField: 'TemporalField') -> int: ...
    def isSupported(self, temporalField: 'TemporalField') -> bool: ...
    _query__R = _py_TypeVar('_query__R')  # <R>
    def query(self, temporalQuery: 'TemporalQuery'[_query__R]) -> _query__R: ...
    def range(self, temporalField: 'TemporalField') -> 'ValueRange': ...

class TemporalAdjuster:
    def adjustInto(self, temporal: 'Temporal') -> 'Temporal': ...

class TemporalAdjusters:
    @classmethod
    def dayOfWeekInMonth(cls, int: int, dayOfWeek: java.time.DayOfWeek) -> TemporalAdjuster: ...
    @classmethod
    def firstDayOfMonth(cls) -> TemporalAdjuster: ...
    @classmethod
    def firstDayOfNextMonth(cls) -> TemporalAdjuster: ...
    @classmethod
    def firstDayOfNextYear(cls) -> TemporalAdjuster: ...
    @classmethod
    def firstDayOfYear(cls) -> TemporalAdjuster: ...
    @classmethod
    def firstInMonth(cls, dayOfWeek: java.time.DayOfWeek) -> TemporalAdjuster: ...
    @classmethod
    def lastDayOfMonth(cls) -> TemporalAdjuster: ...
    @classmethod
    def lastDayOfYear(cls) -> TemporalAdjuster: ...
    @classmethod
    def lastInMonth(cls, dayOfWeek: java.time.DayOfWeek) -> TemporalAdjuster: ...
    @classmethod
    def next(cls, dayOfWeek: java.time.DayOfWeek) -> TemporalAdjuster: ...
    @classmethod
    def nextOrSame(cls, dayOfWeek: java.time.DayOfWeek) -> TemporalAdjuster: ...
    @classmethod
    def ofDateAdjuster(cls, unaryOperator: java.util.function.UnaryOperator[java.time.LocalDate]) -> TemporalAdjuster: ...
    @classmethod
    def previous(cls, dayOfWeek: java.time.DayOfWeek) -> TemporalAdjuster: ...
    @classmethod
    def previousOrSame(cls, dayOfWeek: java.time.DayOfWeek) -> TemporalAdjuster: ...

class TemporalAmount:
    def addTo(self, temporal: 'Temporal') -> 'Temporal': ...
    def get(self, temporalUnit: 'TemporalUnit') -> int: ...
    def getUnits(self) -> java.util.List['TemporalUnit']: ...
    def subtractFrom(self, temporal: 'Temporal') -> 'Temporal': ...

class TemporalField:
    _adjustInto__R = _py_TypeVar('_adjustInto__R', bound='Temporal')  # <R>
    def adjustInto(self, r: _adjustInto__R, long: int) -> _adjustInto__R: ...
    def getBaseUnit(self) -> 'TemporalUnit': ...
    def getDisplayName(self, locale: java.util.Locale) -> str: ...
    def getFrom(self, temporalAccessor: TemporalAccessor) -> int: ...
    def getRangeUnit(self) -> 'TemporalUnit': ...
    def isDateBased(self) -> bool: ...
    def isSupportedBy(self, temporalAccessor: TemporalAccessor) -> bool: ...
    def isTimeBased(self) -> bool: ...
    def range(self) -> 'ValueRange': ...
    def rangeRefinedBy(self, temporalAccessor: TemporalAccessor) -> 'ValueRange': ...
    def resolve(self, map: java.util.Map['TemporalField', int], temporalAccessor: TemporalAccessor, resolverStyle: java.time.format.ResolverStyle) -> TemporalAccessor: ...
    def toString(self) -> str: ...

class TemporalQueries:
    @classmethod
    def chronology(cls) -> 'TemporalQuery'[java.time.chrono.Chronology]: ...
    @classmethod
    def localDate(cls) -> 'TemporalQuery'[java.time.LocalDate]: ...
    @classmethod
    def localTime(cls) -> 'TemporalQuery'[java.time.LocalTime]: ...
    @classmethod
    def offset(cls) -> 'TemporalQuery'[java.time.ZoneOffset]: ...
    @classmethod
    def precision(cls) -> 'TemporalQuery'['TemporalUnit']: ...
    @classmethod
    def zone(cls) -> 'TemporalQuery'[java.time.ZoneId]: ...
    @classmethod
    def zoneId(cls) -> 'TemporalQuery'[java.time.ZoneId]: ...

_TemporalQuery__R = _py_TypeVar('_TemporalQuery__R')  # <R>
class TemporalQuery(_py_Generic[_TemporalQuery__R]):
    def queryFrom(self, temporalAccessor: TemporalAccessor) -> _TemporalQuery__R: ...

class TemporalUnit:
    _addTo__R = _py_TypeVar('_addTo__R', bound='Temporal')  # <R>
    def addTo(self, r: _addTo__R, long: int) -> _addTo__R: ...
    def between(self, temporal: 'Temporal', temporal2: 'Temporal') -> int: ...
    def getDuration(self) -> java.time.Duration: ...
    def isDateBased(self) -> bool: ...
    def isDurationEstimated(self) -> bool: ...
    def isSupportedBy(self, temporal: 'Temporal') -> bool: ...
    def isTimeBased(self) -> bool: ...
    def toString(self) -> str: ...

class UnsupportedTemporalTypeException(java.time.DateTimeException):
    @overload
    def __init__(self, string: str): ...
    @overload
    def __init__(self, string: str, throwable: java.lang.Throwable): ...

class ValueRange(java.io.Serializable):
    def checkValidIntValue(self, long: int, temporalField: TemporalField) -> int: ...
    def checkValidValue(self, long: int, temporalField: TemporalField) -> int: ...
    def equals(self, object: _py_Any) -> bool: ...
    def getLargestMinimum(self) -> int: ...
    def getMaximum(self) -> int: ...
    def getMinimum(self) -> int: ...
    def getSmallestMaximum(self) -> int: ...
    def hashCode(self) -> int: ...
    def isFixed(self) -> bool: ...
    def isIntValue(self) -> bool: ...
    def isValidIntValue(self, long: int) -> bool: ...
    def isValidValue(self, long: int) -> bool: ...
    @classmethod
    @overload
    def of(cls, long: int, long2: int) -> 'ValueRange': ...
    @classmethod
    @overload
    def of(cls, long: int, long2: int, long3: int) -> 'ValueRange': ...
    @classmethod
    @overload
    def of(cls, long: int, long2: int, long3: int, long4: int) -> 'ValueRange': ...
    def toString(self) -> str: ...

class WeekFields(java.io.Serializable):
    ISO: _py_ClassVar['WeekFields'] = ...
    SUNDAY_START: _py_ClassVar['WeekFields'] = ...
    WEEK_BASED_YEARS: _py_ClassVar[TemporalUnit] = ...
    def dayOfWeek(self) -> TemporalField: ...
    def equals(self, object: _py_Any) -> bool: ...
    def getFirstDayOfWeek(self) -> java.time.DayOfWeek: ...
    def getMinimalDaysInFirstWeek(self) -> int: ...
    def hashCode(self) -> int: ...
    @classmethod
    @overload
    def of(cls, dayOfWeek: java.time.DayOfWeek, int: int) -> 'WeekFields': ...
    @classmethod
    @overload
    def of(cls, locale: java.util.Locale) -> 'WeekFields': ...
    def toString(self) -> str: ...
    def weekBasedYear(self) -> TemporalField: ...
    def weekOfMonth(self) -> TemporalField: ...
    def weekOfWeekBasedYear(self) -> TemporalField: ...
    def weekOfYear(self) -> TemporalField: ...

class ChronoField(java.lang.Enum['ChronoField'], TemporalField):
    NANO_OF_SECOND: _py_ClassVar['ChronoField'] = ...
    NANO_OF_DAY: _py_ClassVar['ChronoField'] = ...
    MICRO_OF_SECOND: _py_ClassVar['ChronoField'] = ...
    MICRO_OF_DAY: _py_ClassVar['ChronoField'] = ...
    MILLI_OF_SECOND: _py_ClassVar['ChronoField'] = ...
    MILLI_OF_DAY: _py_ClassVar['ChronoField'] = ...
    SECOND_OF_MINUTE: _py_ClassVar['ChronoField'] = ...
    SECOND_OF_DAY: _py_ClassVar['ChronoField'] = ...
    MINUTE_OF_HOUR: _py_ClassVar['ChronoField'] = ...
    MINUTE_OF_DAY: _py_ClassVar['ChronoField'] = ...
    HOUR_OF_AMPM: _py_ClassVar['ChronoField'] = ...
    CLOCK_HOUR_OF_AMPM: _py_ClassVar['ChronoField'] = ...
    HOUR_OF_DAY: _py_ClassVar['ChronoField'] = ...
    CLOCK_HOUR_OF_DAY: _py_ClassVar['ChronoField'] = ...
    AMPM_OF_DAY: _py_ClassVar['ChronoField'] = ...
    DAY_OF_WEEK: _py_ClassVar['ChronoField'] = ...
    ALIGNED_DAY_OF_WEEK_IN_MONTH: _py_ClassVar['ChronoField'] = ...
    ALIGNED_DAY_OF_WEEK_IN_YEAR: _py_ClassVar['ChronoField'] = ...
    DAY_OF_MONTH: _py_ClassVar['ChronoField'] = ...
    DAY_OF_YEAR: _py_ClassVar['ChronoField'] = ...
    EPOCH_DAY: _py_ClassVar['ChronoField'] = ...
    ALIGNED_WEEK_OF_MONTH: _py_ClassVar['ChronoField'] = ...
    ALIGNED_WEEK_OF_YEAR: _py_ClassVar['ChronoField'] = ...
    MONTH_OF_YEAR: _py_ClassVar['ChronoField'] = ...
    PROLEPTIC_MONTH: _py_ClassVar['ChronoField'] = ...
    YEAR_OF_ERA: _py_ClassVar['ChronoField'] = ...
    YEAR: _py_ClassVar['ChronoField'] = ...
    ERA: _py_ClassVar['ChronoField'] = ...
    INSTANT_SECONDS: _py_ClassVar['ChronoField'] = ...
    OFFSET_SECONDS: _py_ClassVar['ChronoField'] = ...
    _adjustInto__R = _py_TypeVar('_adjustInto__R', bound='Temporal')  # <R>
    def adjustInto(self, r: _adjustInto__R, long: int) -> _adjustInto__R: ...
    def checkValidIntValue(self, long: int) -> int: ...
    def checkValidValue(self, long: int) -> int: ...
    def getBaseUnit(self) -> TemporalUnit: ...
    def getDisplayName(self, locale: java.util.Locale) -> str: ...
    def getFrom(self, temporalAccessor: TemporalAccessor) -> int: ...
    def getRangeUnit(self) -> TemporalUnit: ...
    def isDateBased(self) -> bool: ...
    def isSupportedBy(self, temporalAccessor: TemporalAccessor) -> bool: ...
    def isTimeBased(self) -> bool: ...
    def range(self) -> ValueRange: ...
    def rangeRefinedBy(self, temporalAccessor: TemporalAccessor) -> ValueRange: ...
    def toString(self) -> str: ...
    _valueOf_0__T = _py_TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @classmethod
    @overload
    def valueOf(cls, class_: _py_Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @classmethod
    @overload
    def valueOf(cls, string: str) -> 'ChronoField': ...
    @classmethod
    def values(cls) -> _py_List['ChronoField']: ...

class ChronoUnit(java.lang.Enum['ChronoUnit'], TemporalUnit):
    NANOS: _py_ClassVar['ChronoUnit'] = ...
    MICROS: _py_ClassVar['ChronoUnit'] = ...
    MILLIS: _py_ClassVar['ChronoUnit'] = ...
    SECONDS: _py_ClassVar['ChronoUnit'] = ...
    MINUTES: _py_ClassVar['ChronoUnit'] = ...
    HOURS: _py_ClassVar['ChronoUnit'] = ...
    HALF_DAYS: _py_ClassVar['ChronoUnit'] = ...
    DAYS: _py_ClassVar['ChronoUnit'] = ...
    WEEKS: _py_ClassVar['ChronoUnit'] = ...
    MONTHS: _py_ClassVar['ChronoUnit'] = ...
    YEARS: _py_ClassVar['ChronoUnit'] = ...
    DECADES: _py_ClassVar['ChronoUnit'] = ...
    CENTURIES: _py_ClassVar['ChronoUnit'] = ...
    MILLENNIA: _py_ClassVar['ChronoUnit'] = ...
    ERAS: _py_ClassVar['ChronoUnit'] = ...
    FOREVER: _py_ClassVar['ChronoUnit'] = ...
    _addTo__R = _py_TypeVar('_addTo__R', bound='Temporal')  # <R>
    def addTo(self, r: _addTo__R, long: int) -> _addTo__R: ...
    def between(self, temporal: 'Temporal', temporal2: 'Temporal') -> int: ...
    def getDuration(self) -> java.time.Duration: ...
    def isDateBased(self) -> bool: ...
    def isDurationEstimated(self) -> bool: ...
    def isSupportedBy(self, temporal: 'Temporal') -> bool: ...
    def isTimeBased(self) -> bool: ...
    def toString(self) -> str: ...
    _valueOf_0__T = _py_TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @classmethod
    @overload
    def valueOf(cls, class_: _py_Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @classmethod
    @overload
    def valueOf(cls, string: str) -> 'ChronoUnit': ...
    @classmethod
    def values(cls) -> _py_List['ChronoUnit']: ...

class Temporal(TemporalAccessor):
    @overload
    def isSupported(self, temporalUnit: TemporalUnit) -> bool: ...
    @overload
    def isSupported(self, temporalField: TemporalField) -> bool: ...
    @overload
    def minus(self, temporalAmount: TemporalAmount) -> 'Temporal': ...
    @overload
    def minus(self, long: int, temporalUnit: TemporalUnit) -> 'Temporal': ...
    @overload
    def plus(self, long: int, temporalUnit: TemporalUnit) -> 'Temporal': ...
    @overload
    def plus(self, temporalAmount: TemporalAmount) -> 'Temporal': ...
    def until(self, temporal: 'Temporal', temporalUnit: TemporalUnit) -> int: ...
