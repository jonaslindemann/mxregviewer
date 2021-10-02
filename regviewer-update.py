#!/bin/env python3

import time
import mxreg


if __name__ == "__main__":

    print("Connecting to time sheet...")
    time_sheet = mxreg.TimeSheet()
    time_sheet.connect()

    while True:
        print("Updating data...")
        time_sheet.update()
        print("Sleeping...")
        time.sleep(60)


