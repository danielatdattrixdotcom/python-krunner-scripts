#!/usr/bin/env python

import krunner_bridge
import datetime

# Accepts query with three letter month abbreviation, day and optional year followed by a +/- operator and how many days to adjust.

@krunner_bridge.match_handler
def match(query):
    try:
        month_starters = {
            "jan": 1,
            "feb": 2,
            "mar": 3,
            "apr": 4,
            "may": 5,
            "jun": 6,
            "jul": 7,
            "aug": 8,
            "sep": 9,
            "oct": 10,
            "nov": 11,
            "dec": 12,
        }

        operation = "+"

        if query.find("+") == -1:
            operation = "-"

        query_split = query.split(operation)

        if len(query_split) != 2:
            raise ValueError

        parts = [part.lower() for part in query_split[0].split(" ") if part != ""]

        if parts[0][:3] not in month_starters.keys():
            raise ValueError

        month = month_starters[parts[0][:3]]

        day = int(parts[1])

        if len(parts) == 3:
            year = int(parts[2])
        else:
            year = datetime.datetime.now().year

        adjust_days = int(query_split[1].strip())
        if operation == "-":
            adjust_days *= -1

        adjusted_date = datetime.date(year, month, day) + datetime.timedelta(
            days=adjust_days
        )

        if isinstance(adjusted_date, (datetime.date,)):
            return krunner_bridge.datasource(
                text=adjusted_date.strftime("%m/%d/%Y"),
                icon="appointment-new",
                category="Relative Date",
            )
    except:
        pass


if __name__ == "__main__":
    krunner_bridge.exec()
