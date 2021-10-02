#!/bin/env python3

import configparser as cp
import mxreg

if __name__ == "__main__":

    time_sheet = mxreg.TimeSheet()    
    time_sheet.connect()
    time_sheet.update()
    reg_table = time_sheet.query_date("2021-09-18")   
    
    




