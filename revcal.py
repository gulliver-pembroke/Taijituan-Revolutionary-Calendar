# -*- coding: utf-8 -*-
from datetime import date, time, datetime
from unicodedata import normalize
__all__ = ['MONTH_NAMES', 'WEEKDAY_NAMES', 'Calendar']

# global variables for constant values
REVOLUTION = date(year=2014, month=8, day=26)
BIMONTH_LENGTH = 61
LEAPDAY = 31
CITOYENIDES = 11
WEEK_LENGTH = 10
HOURS_PER_DAY = 10
MINUTES_PER_HOUR = 100
SECONDS_PER_MINUTE = 100
SECONDS_PER_GREGORIAN_DAY = 24 * 60 * 60

MONTH_NAMES = [
	u'',
	u'Ventaire',
	u'Aquaire',
	u'Boisaire',
	u'Orôse',
	u'Gaïôse',
	u'Umbrôse',
	u'Tonnerral',
	u'Ignal',
	u'Sidéral',
	u'Lacidor',
	u'Cielidor',
	u'Lumidor'
]

WEEKDAY_NAMES = [
	u'',
	u'Primidi',
	u'Dromidi',
	u'Isidi',
	u'Novidi',
	u'Jocidi',
	u'Contidi',
	u'Adelphidi',
	u'Vocidi',
	u'Milidi',
	u'Ecclésidi',
	u'Citoyenide'
]

class Calendar:
	def __init__(self, year=1, month=1, day=1, hour=10, minute=0, second=0):
		if not isinstance(year, int) or not year >= 1:
			raise ValueError("year must be an integer greater than 0")
		if month not in range(1,len(MONTH_NAMES)):
			raise ValueError("month must be in 1..12")
		if day not in range(1, 32 if (month % 2 == 0 and (month != 12 or self._is_leap_year(year))) else 31):
			raise ValueError("day is out of range for month")
		if hour not in range(1,11):
			raise ValueError("hour must be in 1..10")
		if minute not in range(0,100):
			raise ValueError("minute must be in 0..99")
		if second not in range(0,100):
			raise ValueError("second must be in 0..99")
		self.year = year
		self.month = month
		self.day = day
		self.hour = hour
		self.minute = minute
		self.second = second
	
	@classmethod	
	def today(cls):
		"""return the revolutionary calendar time for midnight today"""
		return cls.convert(date.today())
		
	@classmethod
	def now(cls):
		"""return the revolutionary calendar time for right now"""
		return cls.convert(datetime.now())
		
	@classmethod
	def convert(cls, gregorian):
		"""convert a Gregorian date or datetime into a revolutionary calendar time"""
		# check if given datetime is valid
		if not isinstance(gregorian, datetime):
			if isinstance(gregorian, date):
				gregorian = datetime.combine(gregorian, time.min)
			else:
				raise TypeError("gregorian must be a date or datetime")
		gregorian_date = gregorian.date()
		if gregorian_date < REVOLUTION:
			raise ValueError("the given date is before the Glorious Revolution!")
		
		# calculate current revolutionary year
		this_new_year = REVOLUTION.replace(year=gregorian.year)
		last_new_year = REVOLUTION.replace(year=gregorian.year - 1)
		if gregorian_date >= this_new_year:
			days = (gregorian_date - this_new_year).days
			year = gregorian.year - REVOLUTION.year + 1
		else:
			days = (gregorian_date - last_new_year).days
			year = gregorian.year - REVOLUTION.year
			
		# calculate revolutionary month and day
		bimonth = days / BIMONTH_LENGTH
		bimonth_half = BIMONTH_LENGTH / 2
		bimonth_day = days % BIMONTH_LENGTH
		month = bimonth * 2 + (1 if bimonth_day >= bimonth_half else 0) + 1
		day = bimonth_day + 1 if bimonth_day < bimonth_half else bimonth_day - bimonth_half + 1
		
		# calculate revolutionary time of day
		midnight = gregorian.replace(hour=0, minute=0, second=0, microsecond=0)
		seconds = (gregorian - midnight).seconds
		seconds_per_hour = (MINUTES_PER_HOUR * SECONDS_PER_MINUTE)
		seconds = seconds * (HOURS_PER_DAY * seconds_per_hour) / SECONDS_PER_GREGORIAN_DAY
		hour = seconds / seconds_per_hour
		hour = 10 if hour == 0 else hour
		minute = seconds % seconds_per_hour / SECONDS_PER_MINUTE
		second = seconds % seconds_per_hour % SECONDS_PER_MINUTE
		
		# return a new instance of a revolutionary calendar time
		return cls(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
		
	@property
	def weekday(self):
		"""returns the numeric index of the current day of the revolutionary week"""
		if self.day == LEAPDAY:
			return CITOYENIDES
		else:
			return (self.day - 1) % WEEK_LENGTH + 1
	
	def _is_leap_year(self, year=None):
		if year:
			year = year + REVOLUTION.year
		else:
			year = self.year + REVOLUTION.year
		return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
		
	def __unicode__(self):
		weekday = WEEKDAY_NAMES[self.weekday]
		month = MONTH_NAMES[self.month]
		fields = (weekday, self.day, month, self.year, self.hour, self.minute, self.second)
		return "%s, %d %s, AR %d, %02d:%02d:%02d" % fields
		
	def __str__(self):
		return normalize('NFKD', self.__unicode__()).encode('ascii', 'ignore')