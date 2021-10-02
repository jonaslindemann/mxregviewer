#!/bin/env python3

from datetime import datetime
from tabulate import tabulate

import configparser as cp

import json, os, sys, time

import gspread

class TimeSheet:
    def __init__(self):

        print('Reading configuration')

        config = cp.ConfigParser()
        config.read('/etc/mx-registration.conf')

        gsheet_document = ""
        db_cache_filename = ""

        if config.has_option('google', 'gsheet_document'):
            gsheet_document = config['google']['gsheet_document'][1:-1]

        if config.has_option('app', 'db_cache_filename'):
            db_cache_filename = config['app']['db_cache_filename'][1:-1]

        print("gsheet_document   :", gsheet_document)
        print("db_cache_filename :", db_cache_filename)

        self.secret_filename = '/etc/mx-registration.json'
        self.gsheet_document = gsheet_document
        self.db_cache_filename = db_cache_filename

        current_date = datetime.now()

        self.date_str = current_date.strftime("%Y-%m-%d")

    def connect(self):
        print("Connecting to service...")
        self.gc = gspread.service_account(filename=self.secret_filename)
        
        print("Opening Sheet...")
        self.sheet = self.gc.open(self.gsheet_document)
      
        print("Getting worksheet...")
        self.worksheet = self.sheet.sheet1

    def update(self):
        print("Checking for sheet update time...")
        updated = self.sheet.lastUpdateTime
        last_update = ""
        
        with open("/var/lib/mxreg/mxreg.stamp", "r") as stamp_file:
            last_update = stamp_file.read().strip()

        if last_update == updated:
            print("No update required.")
            return

        print("Sheet updated. Remember update time...")

        with open("/var/lib/mxreg/mxreg.stamp", "w") as stamp_file:
            stamp_file.write(updated.strip())

        print("Getting all records...")
        db = self.worksheet.get_all_records()

        self.registration_dict = {}
        
        for row in db:
            time_stamp = row["Timestamp"]
            date = datetime.strptime(time_stamp, '%m/%d/%Y %H:%M:%S')
            date_str = date.strftime("%Y-%m-%d")
            if not date_str in self.registration_dict:
                self.registration_dict[date_str] = {}
                
            time_str = date.strftime("%H:%M:%S")
            self.registration_dict[date_str][time_str] = row

        with open(self.db_cache_filename, "w") as db_file:
            json.dump(self.registration_dict, db_file)

    def query_date(self, date_str):

        print("Querying:", date_str)

        # Do we have a cached database

        if os.path.exists(self.db_cache_filename):
            with open(self.db_cache_filename, "r") as db_file:
                self.registration_dict = json.load(db_file)

        registration_table = []

        if date_str in self.registration_dict:
            date_regs = self.registration_dict[date_str]

            header = None

            for time_str in date_regs.keys():
                values = []
                header = list(date_regs[time_str].keys())
                for key in date_regs[time_str].keys():
                    values.append(date_regs[time_str][key])

                registration_table.append(values)
            
            registration_table.insert(0, header)

            #print(tabulate(registration_table[1:], headers=header))

            return registration_table
        else:
            return []
    
    




