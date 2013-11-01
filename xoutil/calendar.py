import datetime, calendar
from dateutil import easter

def get_period_begin_date(day):
    if day.month >= 6:
        year = day.year
    else:
        year = day.year-1
    return max(datetime.datetime.strptime(str(year)+"-06-01", "%Y-%m-%d"), contract_begin_date)

def get_prev_period_begin_date(day):
    this_period_first_date	= get_period_begin_date(day)
    if this_period_first_date == contract_begin_date:
        return None
    prev_period_last_date  	= this_period_first_date - datetime.timedelta(1)
    return get_period_begin_date(prev_period_last_date)

def get_worked_months(date1, date2):
    worked_months = date2.month - date1.month
    if worked_months < 0:
        worked_months = (12 - date1.month) + date2.month
    worked_months -= 1 # solo cuentan los meses trabajados completos
    if date1.day == 1: # si el primer mes se trabaja desde el primer dia
        worked_months += 1
    if date2.day == calendar.monthrange(date2.year, date2.month)[1]: # si es el ultimo dia del ultimo mes
        worked_months +=1
    return max(0, worked_months)

def get_worked_months_in_period(day):
    return get_worked_months(get_period_begin_date(day), day)

def get_worked_months_in_prev_period(day):
    prev_period_begin_date = get_prev_period_begin_date(day)
    if prev_period_begin_date:
        return get_worked_months(prev_period_begin_date, get_period_begin_date(day) - datetime.timedelta(1))
    return 0

def get_accum_holidays(day): # dias acumulados en el periodo anterior
    return 2.5 * get_worked_months_in_prev_period(day)

def get_remnant_holidays(day): # dias disponibles - dias tomados

    acumm_holidays     = get_accum_holidays(day)
    reserved_holidays  = get_reserved_holidays(day)
    requested_holidays = get_requested_holidays(day)
    used_holidays      = get_used_holidays(day)
    prev_period_last_day = get_period_begin_date(day) - datetime.timedelta(1)
    prev_used_holidays = get_prev_used_holidays(prev_period_last_day)

    return min(acumm_holidays - used_holidays - reserved_holidays - requested_holidays - prev_used_holidays, 30)

def get_prev_used_holidays(day):
    period_begin_date = get_period_begin_date(day)
    prev_period_last_day = period_begin_date - datetime.timedelta(1)
    if period_begin_date == contract_begin_date:
        a = get_used_holidays(day)
        return a
    b = get_used_holidays(day)
    c = get_accum_holidays(day)
    d = get_prev_used_holidays(prev_period_last_day)
    return max(d + b - c, 0)

def get_reserved_holidays(day):
    return 0

def get_requested_holidays(day):
    return 0

def get_used_holidays(day):
    period_begin_day = get_period_begin_date(day)
    count = 0
    for holiday in used_holidays:
        if period_begin_day <= holiday <= day and not is_free_day(holiday):
            count += 1
            if is_penalty_day(holiday):
                count += 1

    return count

def is_free_day(day):
    return is_weekend(day) or is_festivity_day(day)

def is_weekend(day):
    return day.weekday() > 4

def is_festivity_day(day):
    festivities = []
    festivities.append(datetime.datetime.strptime(str(day.year)+"-01-01", "%Y-%m-%d"))
    festivities.append(datetime.datetime.strptime(str(day.year)+"-05-01", "%Y-%m-%d"))
    festivities.append(datetime.datetime.strptime(str(day.year)+"-12-25", "%Y-%m-%d"))
    if False: # Francia
        p = easter.easter(day.year)
        festivities.append(p + datetime.timedelta(1)) # lunes de pascua
        festivities.append(p + datetime.timedelta(39)) # jueves de ascencion
        festivities.append(p + datetime.timedelta(50)) # lunes pentecostes
        festivities.append(datetime.datetime.strptime(str(day.year)+"-05-08", "%Y-%m-%d"))
        festivities.append(datetime.datetime.strptime(str(day.year)+"-07-14", "%Y-%m-%d"))
        festivities.append(datetime.datetime.strptime(str(day.year)+"-08-15", "%Y-%m-%d"))
        festivities.append(datetime.datetime.strptime(str(day.year)+"-11-01", "%Y-%m-%d"))
        festivities.append(datetime.datetime.strptime(str(day.year)+"-11-11", "%Y-%m-%d"))
    elif True: # Cuba
        festivities.append(datetime.datetime.strptime(str(day.year)+"-02-01", "%Y-%m-%d"))
        festivities.append(datetime.datetime.strptime(str(day.year)+"-07-25", "%Y-%m-%d"))
        festivities.append(datetime.datetime.strptime(str(day.year)+"-07-26", "%Y-%m-%d"))
        festivities.append(datetime.datetime.strptime(str(day.year)+"-07-27", "%Y-%m-%d"))
        festivities.append(datetime.datetime.strptime(str(day.year)+"-10-10", "%Y-%m-%d"))
        festivities.append(datetime.datetime.strptime(str(day.year)+"-12-31", "%Y-%m-%d"))

    return day in festivities

def is_penalty_day(day):
    if day.weekday() == 4:
        return True
    return is_festivity_day(day + datetime.timedelta(1))

def reserve_holidays(day, duration):
    if duration > 30:
        return "Error: debe reservar menos de 30 dias"
    # alguna regla para reservar? por ejemplo, para reservar sin dias disponibles. Se pueden reservar mas de 30 dias?

def get_accum_compensatory_days(day):
    count = 0
    for extra_day in extra_days:
        if is_festivity_day(extra_day) and  datetime.timedelta(0) < day - extra_day < datetime.timedelta(31):
            count += 1
        elif is_weekend(extra_day) and datetime.timedelta(0) < day - extra_day < datetime.timedelta(7):
            count += 1
    return count

def print_values(day):

    print "contract        ", contract_begin_date
    print "today           ", day
    print "period bdate    ", get_period_begin_date(day)
    print "pperiod bdate   ", get_prev_period_begin_date(day)
    print "period wmonths  ", get_worked_months_in_period(day)
    print "pperiod wmonths ", get_worked_months_in_prev_period(day)
    print "accum days      ", get_accum_holidays(day)
    print "used holidays   ", get_used_holidays(day)
    print "remnant days    ", get_remnant_holidays(day)
    print "compensat days  ", get_accum_compensatory_days(day)

    print "-----"

# ===================================================

#d1 = datetime.datetime.strptime("2013-05-29", "%Y-%m-%d")
#
#d2 = datetime.datetime.strptime("2013-10-02", "%Y-%m-%d")
#
#used_holidays 		= []
#base				= datetime.datetime.strptime("2013-02-5", "%Y-%m-%d")
#used_holidays 		= [ base - datetime.timedelta(days=x) for x in range(0,10) ]
#
#reserved_holidays 	= []
#requested_holidays 	= []

###### test case 1

def create_date(str_day):
    return datetime.datetime.strptime(str_day, "%Y-%m-%d")

def create_date_list(str_day, duration):
    return [datetime.datetime.strptime(str_day, "%Y-%m-%d") + datetime.timedelta(days=x) for x in range(0, duration) ]

contract_begin_date	= create_date("2011-02-01")

# vacaciones tomadas
used_holidays       = create_date_list("2011-05-29", 6) + create_date_list("2011-12-25", 10) + create_date_list("2012-12-25", 20)

# dias no laborables trabajados
extra_days          = [create_date("2012-05-27"), create_date("2012-05-20"), create_date("2012-05-01")]
# domingo de esa semana, domingo de la anterior, 1 de mayo

d = create_date("2012-06-01")
print_values(d)

# ====================================================

# TODO:
# get_available_free_days: los dias que quedan de vacaciones mas los dias compensatorios
# reservar dias
# pedir dias
# trabajar dias extras
# saldo de dias extras
# tema de los dias extras cubanos, aqui arreglar el penalty si es preciso