#!/usr/bin/env python3
"""
Printing routines for seaplan
"""
# STANDARD LIBRARIES
from datetime import datetime, timedelta
import math

# CONSTANTS
comment_len = 40
action_len = 40


def print_results(event_list, parameter_file, params, stations, used_stations):
    """
    Print a table in reStructuredText

    :param event_list: list of Events
    :param parameter_file:
    :param params:
    """
    show_comments = params['printout']['show_comments']
    if show_comments:
        # Shorten comment columns if possible
        maxlen = max([len(x.get('comment', '')) for x in event_list])
        global comment_len
        comment_len = min([comment_len, maxlen])
    # Shorten action columns if possible
    maxlen = max([len(x.get('action', '')) for x in event_list])
    global action_len
    action_len = min([action_len, maxlen])

    t = _pre_table(parameter_file, params)
    t += _table_header(params)
    prev_arrival = event_list[0]['arrival']['time']
    day_mesg = make_day_mesg(prev_arrival, show_comments, True)
    trans_accum = dict(h=0., nm=0.)
    for event in event_list:
        if event['hours'] or params['printout']['print_waypoints']:
            arrival = event['arrival']['time']
            departure = event['departure']['time']
            if arrival.day != prev_arrival.day:
                day_mesg = make_day_mesg(arrival, show_comments)
            if (params['printout']['print_past']
                    or (departure > datetime.now())):
                if day_mesg:
                    t += day_mesg
                    day_mesg = ''
                t += _table_row(event, trans_accum, show_comments)
            prev_arrival = arrival
            trans_accum = dict(h=0., nm=0.)
        else:
            trans_accum['h'] += event['transit_hours']
            trans_accum['nm'] += event['dist_from_previous']
    t += _table_footer(show_comments)
    t += _post_table(stations, used_stations)
    return t


def _pre_table(parameter_file, params):
    t = ''
    if params['description'] is not None:
        t = f"**{params['description'].upper()}**\n\n"
    t += "- **Created on**: {}\n".format(
         datetime.now().strftime('%Y-%m-%d %H:%M local'))
    t += f'- **Station file**: "{params["station_file"]["name"]}"\n'
    t += f'- **Parameter file**: "{parameter_file}"\n'
    t += '\n'
    t += f'  - **Boat speed (kts)**: {params["timing"]["ship_speed.kn_i"]:d}\n'
    t += f'  - **Boat latency (h)**: {params["timing"]["ship_latency.h"]:g}\n'
    t += '  - **Default Action "hours"**:\n'
    t += '\n'
    return t


def _table_header(params):
    t = ''
    for action, values in params['timing']['action_times.h'].items():
        t += f'    - **{action}**: '
        for name, hours in values.items():
            t += f'"{name}": {hours}, '
        t += '\n'
    t += '\n'
    if params['timing']['ignore_depart_arrive_times']:
        t += '\nIGNORING ALL "arrival_" AND "departure_" TIMES IN YAML FILE!\n'
    if not params['printout']['show_comments']:
        t += "\n"
        t += "+-----------"+action_len*"-"+"-+-----------------------+"\
             "--------------+-------------------------------+\n"
        t += "| EVENT     "+action_len*" "+" | POSITION              |"\
             " TRANSIT      | STATION TIME                  |\n"
        t += "+---------+-"+action_len*"-"+"-+-----------+-----------+"\
             "--------------+-------+-----------+-----------+\n"
        t += "| Station | Action"+(action_len-6)*" "+" | Lat       |"\
             " Lon       | hours(nmiles)| Hours | Arrive    | Depart    |\n"
        t += "+=========+="+action_len*"="+"=+===========+===========+"\
             "==============+=======+===========+===========+\n"
    else:
        t += "\n"
        t += "+-----------"+action_len*"-"+"-+-----------------------+"\
             "--------------+-------------------------------+-"\
             + comment_len*"-"+"-+\n"
        t += "| EVENT     "+action_len*" "+" | POSITION              |"\
             " TRANSIT      | STATION TIME          | COMMENTS "\
             + (comment_len-9)*" "+" |\n"
        t += "+---------+-"+action_len*"-"+"-+-----------+-----------+"\
             "--------------+-------+-----------+-----------+-"\
             + comment_len*"-"+"-+\n"
        t += "| Station | Action"+(action_len-6)*" "+"   | Lat       |"\
             " Lon       | hours(nmiles)| Hours | Arrive    | Depart    | "\
             + comment_len*" "+" |\n"
        t += "+=========+="+action_len*"="+"=+===========+===========+"\
             "==============+=======+===========+===========+="\
             + comment_len*"="+"=+\n"
    return t


def make_day_mesg(the_time, show_comments, no_top=False):
    if show_comments:
        if no_top:
            t = ""
        else:
            t = "+---------+-" + action_len*"-"\
                + "-+-----------+-----------+--------------+-------+"\
                + "-----------+-----------+-" + comment_len*"-" + "-|\n"
        t += "|    {:76s}    ".format(the_time.strftime("*%A, %d %B*"))\
            + (comment_len+action_len)*" " + " |\n"
    else:
        if no_top:
            t = ""
        else:
            t = "+---------+-" + action_len*"-"\
                + "-+-----------+-----------+--------------+-------+"\
                + "-----------+-----------+\n"
        t += "|    {:76s}  ".format(the_time.strftime("*%A, %d %B*"))\
             + (action_len)*" " + " |\n"
    return t


def _table_row(event, trans_accum, show_comments, debug=False):
    sta = event['station']
    act = event.get('action', '')
    lat = __deg_as_degmin(event['lat'])
    lon = __deg_as_degmin(event['lon'])
    trn = event['transit_hours'] + trans_accum['h']
    dst = event['dist_from_previous'] + trans_accum['nm']
    arr = time_str(event['arrival'])
    dep = time_str(event['departure'])
    evtt = (event['departure']['time']
            - event['arrival']['time']) / timedelta(hours=1)
    evtt_s = '{:02d}:{:02d}'.format(int(math.floor(evtt)),
                                    int(60*(evtt-math.floor(evtt))))
    cmt = event['comment']
    if debug:
        print(f"comment={event['comment']}")
    if not show_comments:
        t = "+---------+-"+action_len*"-"+"-+-----------+-----------"\
            "+--------------+-------+-----------+-----------+\n"
        t += "| {:7.7s} | {:" + f"{action_len:d}.{action_len:d}"\
             + "s} | {:>9s} | {:>9s} | {:4.1f} ({:5.1f}) | {:^5s} "\
             + "| {:^9s} | {:^9s} |\n"
        return t.format(sta, act, lat, lon, trn, dst, evtt_s, arr, dep)
    else:
        t = "+---------+-"+action_len*"-"+"-+-----------+-----------"\
            "+--------------+-------+-----------+-----------+-"\
            + comment_len*"-"+"-+\n"
        t += "| {:7.7s} | {:"+f"{action_len:d}.{action_len:d}"+"s} | {:>9s} "\
             "| {:>9s} | {:4.1f} ({:5.1f}) | {:^5s} | {:^9s} | {:^9s} | {:"\
             + f"{comment_len:d}.{comment_len:d}s"+"} |\n"
        return t.format(sta, act, lat, lon, trn, dst, evtt_s, arr, dep, cmt)


def _table_footer(show_comments):
    if show_comments:
        t = "+---------+-"+action_len*"-"+"-+-----------+-----------"\
            "+--------------+-------+-----------+-----------+-"\
            + comment_len*"-" + "-+\n"
    else:
        t = "+---------+-"+action_len*"-"+"-+-----------+-----------"\
            "+--------------+-------+-----------+-----------+\n"
    return t


def time_str(the_time):
    """
    return time string

    :param the_time: dict with 'time' and 'forced' keys

    The output text has different emphasis based on whether it is
    the input time (normal), a forced time in the future (**bold**),
    or a forced time in the past (*italic*)
    """
    emphasis = ''
    if the_time['forced']:
        if the_time['time'] < datetime.now():  # Already passed, no big deal
            emphasis = '*'
        else:                            # Not yet passed, **CONSTRAINT**
            emphasis = '**'
    time_s = emphasis+the_time['time'].strftime("%H:%M") + emphasis
    return time_s


def _post_table(stations, used_stations):
    """
    Print information about which stations were used

    I think this is inefficiently written (no need for sta_dict?)
    :param stations: list of station dictionaries
    :param used_stations: list of the stations visited, in order
    """
    sta_dict = dict()
    for us in used_stations:
        sta_dict[us] = sta_dict.get(us, 0) + 1
    unused = []
    for name in stations.keys():
        if name not in sta_dict.keys():
            unused.append(name)

    t = '\n{:d} of {:d} stations in the station file were used\n'.format(
        len(sta_dict), len(stations))

    # List used stations
    t += "\nUsed:\n"
    for s in sorted(sta_dict):
        t += f"    {s}\n"

    # List unused stations
    t += "\nUnused:\n"
    if len(unused) == 0:
        t +="  None\n"
    else:
        for s in sorted(unused):
            t += f"    {s}\n"

    # If multiple occurences of a station or stations, warn and inform
    iRepeated = 0
    for sta_name in sorted(sta_dict.keys()):
        if sta_dict[sta_name] > 1:
            iRepeated += 1
    if iRepeated:
        if iRepeated == 1:
            t += '\n**1 repeated used station:**\n'
        else:
            t += '\n**{:d} stations were repeated:**\n'.format(iRepeated)
        for sta_name in sorted(sta_dict.keys()):
            if sta_dict[sta_name] > 1:
                t += f"  {sta_name} : {sta_dict[sta_name]:d} times\n"
    else:
        t += "\nNo repeated used stations\n"
    return t


def __deg_as_degmin(degrees, precision=1):
    """
    Return text string containing degrees and minutes

    precision is number of digits after the decimal place to return
    for the minutes field
    """
    if not isinstance(precision, int):
        print('PRECISION IS NOT AN INTEGER')
        return
    if precision < 0:
        print('PRECISION < 0!')
        return
    deg_int = math.trunc(degrees)
    deg_min = abs(60 * (degrees - deg_int))
    field_width = precision + 3
    if precision == 0:
        field_width = 2
    else:
        field_width = precision + 3
    fmt_str = "{:d}d{:0" + "{:d}.{:d}".format(field_width, precision) + "f}m"
    return fmt_str.format(deg_int, deg_min)
