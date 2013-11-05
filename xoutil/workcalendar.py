import sys, os

#try:
#    sys.path.remove(os.path.abspath('.'))
#except :
#    pass
#sys.path.reverse()

import datetime
import calendar
from dateutil import easter

class workcalendar:

    def __init__(self, contract_begin_date, fiscal_year_begin_month, law='Autrement',
                 used_holidays=[], requested_holidays=[], confirmed_holidays=[], extra_work_days=[]):

        self.contract_begin_date = contract_begin_date
        self.fiscal_year_begin_month = fiscal_year_begin_month
        self.law = law
        self.used_holidays = used_holidays
        self.requested_holidays = requested_holidays
        self.confirmed_holidays = confirmed_holidays
        self.extra_work_days = extra_work_days

    def create_date(self, str_day):
        return datetime.datetime.strptime(str_day, "%Y-%m-%d")

    def get_period_begin_date(self, day):
        """
        Given a day, return the period's begin date, which may be in the same year
        or the previous, according to the fiscal year

        Examples:

            >>> import workcalendar
            >>> import datetime
            >>> c = datetime.datetime.strptime("2010-01-01", "%Y-%m-%d")
            >>> wc = workcalendar.workcalendar(c, 10)
            >>> d = datetime.datetime.strptime("2012-10-07", "%Y-%m-%d")
            >>> pbd = wc.get_period_begin_date(d)
            >>> pbd == datetime.datetime.strptime("2012-10-01", "%Y-%m-%d")
            True

            >>> d = datetime.datetime.strptime("2012-06-07", "%Y-%m-%d")
            >>> pbd = wc.get_period_begin_date(d)
            >>> pbd == datetime.datetime.strptime("2011-10-01", "%Y-%m-%d")
            True

            >>> d = datetime.datetime.strptime("2010-09-07", "%Y-%m-%d")
            >>> pbd = wc.get_period_begin_date(d)
            >>> pbd == datetime.datetime.strptime("2010-01-01", "%Y-%m-%d")
            True

        """
        if day.month >= self.fiscal_year_begin_month:
            year = day.year
        else:
            year = day.year-1
        return max(self.create_date(str(year)+"-"+str(self.fiscal_year_begin_month)+"-01"), self.contract_begin_date)

    def get_prev_period_begin_date(self, day):
        """
        Given a day, return the previous period's begin date, which may be in
        the same year or the previous, according to the fiscal year;

        Examples:

            >>> import workcalendar
            >>> import datetime
            >>> c = datetime.datetime.strptime("2010-01-01", "%Y-%m-%d")
            >>> wc = workcalendar.workcalendar(c, 10)
            >>> d = datetime.datetime.strptime("2012-10-07", "%Y-%m-%d")
            >>> pbd = wc.get_prev_period_begin_date(d)
            >>> pbd == datetime.datetime.strptime("2011-10-01", "%Y-%m-%d")
            True

            >>> d = datetime.datetime.strptime("2012-06-07", "%Y-%m-%d")
            >>> pbd = wc.get_prev_period_begin_date(d)
            >>> pbd == datetime.datetime.strptime("2010-10-01", "%Y-%m-%d")
            True

            >>> d = datetime.datetime.strptime("2010-09-07", "%Y-%m-%d")
            >>> pbd = wc.get_prev_period_begin_date(d)
            >>> pbd == None
            True

        """
        this_period_first_date	= self.get_period_begin_date(day)
        if this_period_first_date == self.contract_begin_date:
            return None
        prev_period_last_date  	= this_period_first_date - datetime.timedelta(1)
        return self.get_period_begin_date(prev_period_last_date)

    def get_worked_months(self, date1, date2):
        """
        Given two dates in a fiscal year, return the complete worked months
        between them;

        Examples:

            >>> import workcalendar
            >>> wc = workcalendar.workcalendar(None, 1)
            >>> import datetime
            >>> d1 = datetime.datetime.strptime("2011-12-05", "%Y-%m-%d")
            >>> d2 = datetime.datetime.strptime("2012-01-07", "%Y-%m-%d")
            >>> wc.get_worked_months(d1, d2)
            0

            >>> d1 = datetime.datetime.strptime("2011-12-01", "%Y-%m-%d")
            >>> d2 = datetime.datetime.strptime("2012-01-07", "%Y-%m-%d")
            >>> wc.get_worked_months(d1, d2)
            1

            >>> d1 = datetime.datetime.strptime("2011-12-05", "%Y-%m-%d")
            >>> d2 = datetime.datetime.strptime("2012-01-31", "%Y-%m-%d")
            >>> wc.get_worked_months(d1, d2)
            1

            >>> d1 = datetime.datetime.strptime("2011-12-01", "%Y-%m-%d")
            >>> d2 = datetime.datetime.strptime("2012-01-31", "%Y-%m-%d")
            >>> wc.get_worked_months(d1, d2)
            2

        """
        worked_months = date2.month - date1.month
        if worked_months < 0:
            worked_months = (12 - date1.month) + date2.month
        worked_months -= 1 # solo cuentan los meses trabajados completos
        if date1.day == 1: # si el primer mes se trabaja desde el primer dia
            worked_months += 1
        if date2.day == calendar.monthrange(date2.year, date2.month)[1]: # si es el ultimo dia del ultimo mes
            worked_months += 1
        return max(0, worked_months)

    def get_worked_months_in_period(self, day):
        """
        Given a day, return the complete worked months in the period;

        Examples:

            >>> import workcalendar
            >>> import datetime
            >>> c = datetime.datetime.strptime("2010-01-01", "%Y-%m-%d")
            >>> wc = workcalendar.workcalendar(c, 10)
            >>> d = datetime.datetime.strptime("2012-10-07", "%Y-%m-%d")
            >>> wc.get_worked_months_in_period(d)
            0

            >>> d = datetime.datetime.strptime("2012-06-07", "%Y-%m-%d")
            >>> wc.get_worked_months_in_period(d)
            8

            >>> d = datetime.datetime.strptime("2010-09-07", "%Y-%m-%d")
            >>> wc.get_worked_months_in_period(d)
            8
        """
        return self.get_worked_months(self.get_period_begin_date(day), day)

    def get_worked_months_in_prev_period(self, day):
        """
        Given a day, return the complete worked months in the period;

        Examples:

            >>> import workcalendar
            >>> import datetime
            >>> c = datetime.datetime.strptime("2010-01-01", "%Y-%m-%d")
            >>> wc = workcalendar.workcalendar(c, 10)
            >>> d = datetime.datetime.strptime("2012-10-07", "%Y-%m-%d")
            >>> wc.get_worked_months_in_prev_period(d)
            12

            >>> d = datetime.datetime.strptime("2012-06-07", "%Y-%m-%d")
            >>> wc.get_worked_months_in_prev_period(d)
            12

            >>> d = datetime.datetime.strptime("2011-06-07", "%Y-%m-%d")
            >>> wc.get_worked_months_in_prev_period(d)
            9

            >>> d = datetime.datetime.strptime("2010-09-07", "%Y-%m-%d")
            >>> wc.get_worked_months_in_prev_period(d)
            0

        """

        prev_period_begin_date = self.get_prev_period_begin_date(day)
        if prev_period_begin_date:
            return self.get_worked_months(prev_period_begin_date, self.get_period_begin_date(day) - datetime.timedelta(1))
        return 0

    def get_accum_holidays(self, day):
        """
        Given a day, holidays accumuulated in the previous period

        Examples:

            >>> import workcalendar
            >>> import datetime
            >>> c = datetime.datetime.strptime("2010-01-01", "%Y-%m-%d")
            >>> wc = workcalendar.workcalendar(c, 10)
            >>> d = datetime.datetime.strptime("2012-10-07", "%Y-%m-%d")
            >>> wc.get_accum_holidays(d)
            30.0

            >>> d = datetime.datetime.strptime("2012-06-07", "%Y-%m-%d")
            >>> wc.get_accum_holidays(d)
            30.0

            >>> d = datetime.datetime.strptime("2011-06-07", "%Y-%m-%d")
            >>> wc.get_accum_holidays(d)
            22.5

            >>> d = datetime.datetime.strptime("2010-09-07", "%Y-%m-%d")
            >>> wc.get_accum_holidays(d)
            0.0
        """
        return 2.5 * self.get_worked_months_in_prev_period(day)

    def get_remnant_holidays(self, day):
        """
        Given a day, return the remnant holidays, i.e. the accumulated holidays minus
        already used used, requested or confirmed holidays, and holidays taken in advance
        in the previous period.

        Example:

            >>> import workcalendar
            >>> import datetime
            >>> c = datetime.datetime.strptime("2011-02-01", "%Y-%m-%d")
            >>> def create_date_list(str_day, duration):
            ...   return [datetime.datetime.strptime(str_day, "%Y-%m-%d") + datetime.timedelta(days=x) for x in range(0, duration) ]
            >>> used_holidays = create_date_list("2011-05-29", 6)
            >>> wc = workcalendar.workcalendar(c, 6, 'Autrement', used_holidays)
            >>> d = datetime.datetime.strptime("2011-11-03", "%Y-%m-%d")
            >>> wc.get_remnant_holidays(d)
            4.0

            >>> wc.used_holidays += create_date_list("2011-11-5", 10)
            >>> d = datetime.datetime.strptime("2011-12-03", "%Y-%m-%d")
            >>> wc.get_remnant_holidays(d)
            -3.0

            >>> d = datetime.datetime.strptime("2012-06-03", "%Y-%m-%d")
            >>> wc.get_remnant_holidays(d)
            27.0

            >>> wc.used_holidays += create_date_list("2012-04-30", 1)
            >>> wc.get_remnant_holidays(d)
            25.0

        """

        acumm_holidays       = self.get_accum_holidays(day)
        requested_holidays   = self.get_requested_holidays(day)
        confirmed_holidays   = self.get_confirmed_holidays(day)
        used_holidays        = self.get_used_holidays(day)
        prev_period_last_day = self.get_period_begin_date(day) - datetime.timedelta(1)
        prev_used_holidays   = self.get_prev_used_holidays(prev_period_last_day)

        return min(acumm_holidays - used_holidays - requested_holidays - confirmed_holidays- prev_used_holidays, 30)

    def get_prev_used_holidays(self, day):
        """
        Recursively calculate de holidays used in advance in previous periods
        """
        period_begin_date = self.get_period_begin_date(day)
        prev_period_last_day = period_begin_date - datetime.timedelta(1)
        if period_begin_date == self.contract_begin_date:
            a = self.get_used_holidays(day)
            return a
        b = self.get_used_holidays(day)
        c = self.get_accum_holidays(day)
        d = self.get_prev_used_holidays(prev_period_last_day)
        return max(d + b - c, 0)

    def get_requested_holidays(self, day):
        return 0

    def get_confirmed_holidays(self, day):
        return 0

    def get_used_holidays(self, day):
        """
        Return the used holidays in day's period, skiping free days (saturday,
        sundays and festivity days). Fridays and prior festivity days are
        penalized.
        """
        period_begin_day = self.get_period_begin_date(day)
        count = 0
        for holiday in self.used_holidays:
            if period_begin_day <= holiday <= day and not self.is_free_day(holiday):
                count += 1
                if self.is_penalty_day(holiday):
                    count += 1
        return count

    def is_free_day(self, day):
        return self.is_weekend(day) or self.is_festivity_day(day)

    def is_weekend(self, day):
        return day.weekday() > 4

    def is_festivity_day(self, day):
        """
        Given a day, return whether if is a festivity day, according to the law
        """
        festivities = []
        if self.law == 'Francesa': # Francia
            p = easter.easter(day.year)
            festivities.append(datetime.datetime.strptime(str(day.year)+"-01-01", "%Y-%m-%d"))
            festivities.append(p + datetime.timedelta(1)) # lunes de pascua
            festivities.append(p + datetime.timedelta(39)) # jueves de ascencion
            festivities.append(p + datetime.timedelta(50)) # lunes pentecostes
            festivities.append(datetime.datetime.strptime(str(day.year)+"-05-01", "%Y-%m-%d"))
            festivities.append(datetime.datetime.strptime(str(day.year)+"-05-08", "%Y-%m-%d"))
            festivities.append(datetime.datetime.strptime(str(day.year)+"-07-14", "%Y-%m-%d"))
            festivities.append(datetime.datetime.strptime(str(day.year)+"-08-15", "%Y-%m-%d"))
            festivities.append(datetime.datetime.strptime(str(day.year)+"-11-01", "%Y-%m-%d"))
            festivities.append(datetime.datetime.strptime(str(day.year)+"-11-11", "%Y-%m-%d"))
            festivities.append(datetime.datetime.strptime(str(day.year)+"-12-25", "%Y-%m-%d"))
        elif self.law == 'Autrement': # Cuba
            festivities.append(datetime.datetime.strptime(str(day.year)+"-01-01", "%Y-%m-%d"))
            festivities.append(datetime.datetime.strptime(str(day.year)+"-02-01", "%Y-%m-%d"))
            festivities.append(datetime.datetime.strptime(str(day.year)+"-05-01", "%Y-%m-%d"))
            festivities.append(datetime.datetime.strptime(str(day.year)+"-07-25", "%Y-%m-%d"))
            festivities.append(datetime.datetime.strptime(str(day.year)+"-07-26", "%Y-%m-%d"))
            festivities.append(datetime.datetime.strptime(str(day.year)+"-07-27", "%Y-%m-%d"))
            festivities.append(datetime.datetime.strptime(str(day.year)+"-10-10", "%Y-%m-%d"))
            festivities.append(datetime.datetime.strptime(str(day.year)+"-12-25", "%Y-%m-%d"))
            festivities.append(datetime.datetime.strptime(str(day.year)+"-12-31", "%Y-%m-%d"))

        return day in festivities

    def is_penalty_day(self, day):
        """
        Return True if day is a friday or next day is a festivity day
        """
        if day.weekday() == 4:
            return True
        return self.is_festivity_day(day + datetime.timedelta(1))

    def reserve_holidays(self, day, duration):
        if duration > 30:
            return "Error: debe reservar menos de 30 dias"
        # alguna regla para reservar? por ejemplo, para reservar sin dias disponibles. Se pueden reservar mas de 30 dias?

    def get_accum_compensatory_days(self, day):
        count = 0
        for extra_day in self.extra_days:
            if self.is_festivity_day(extra_day) and  datetime.timedelta(0) < day - extra_day < datetime.timedelta(31):
                count += 1
            elif self.is_weekend(extra_day) and datetime.timedelta(0) < day - extra_day < datetime.timedelta(7):
                count += 1
        return count

#def print_values(day):
#
##    print "contract        ", contract_begin_date
##    print "today           ", day
##    print "period bdate    ", get_period_begin_date(day)
##    print "pperiod bdate   ", get_prev_period_begin_date(day)
##    print "period wmonths  ", get_worked_months_in_period(day)
##    print "pperiod wmonths ", get_worked_months_in_prev_period(day)
##    print "accum days      ", get_accum_holidays(day)
##    print "used holidays   ", get_used_holidays(day)
##    print "remnant days    ", get_remnant_holidays(day)
##    print "compensat days  ", get_accum_compensatory_days(day)
##
##    print "-----"
#    pass
#
## ===================================================
#
##d1 = datetime.datetime.strptime("2013-05-29", "%Y-%m-%d")
##
##d2 = datetime.datetime.strptime("2013-10-02", "%Y-%m-%d")
##
##used_holidays 		= []
##base				= datetime.datetime.strptime("2013-02-5", "%Y-%m-%d")
##used_holidays 		= [ base - datetime.timedelta(days=x) for x in range(0,10) ]
##
##reserved_holidays 	= []
##requested_holidays 	= []
#
####### test case 1
#
#
#def create_date_list(str_day, duration):
#    return [datetime.datetime.strptime(str_day, "%Y-%m-%d") + datetime.timedelta(days=x) for x in range(0, duration) ]
#
#contract_begin_date	= create_date("2011-02-01")
#
## vacaciones tomadas
#used_holidays       = create_date_list("2011-05-29", 6) + create_date_list("2011-12-25", 10) + create_date_list("2012-12-25", 20)
#
## dias no laborables trabajados
#extra_days          = [create_date("2012-05-27"), create_date("2012-05-20"), create_date("2012-05-01")]
## domingo de esa semana, domingo de la anterior, 1 de mayo
#
#d = create_date("2012-06-01")
#print_values(d)
#
## ====================================================
#
## TODO:
## get_available_free_days: los dias que quedan de vacaciones mas los dias compensatorios
## reservar dias
## pedir dias
## trabajar dias extras
## saldo de dias extras
## tema de los dias extras cubanos, aqui arreglar el penalty si es preciso

if __name__ == "__main__":
    import doctest
    doctest.testmod()