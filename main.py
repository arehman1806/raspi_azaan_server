import json
import os
import sched
import schedule
import time

from player import Player


class AzaanServer:
    def __init__(self):

        self.host = self.parse_config()
        self.player = Player(self.host, "{}/azaans".format(os.getcwd()))
        self.setup_azaans_for_the_day()
        # self.create_daily_scheduler()

        while True:
            schedule.run_pending()
            time.sleep(1)

    def create_daily_scheduler(self):
        schedule.every().day.at("00:01").do(self.setup_azaans_for_the_day)

    def setup_azaans_for_the_day(self):
        schedule.clear()
        day = str(time.localtime().tm_mday).zfill(2)
        month = str(time.localtime().tm_mon).zfill(2)
        year = str(time.localtime().tm_year).zfill(2)
        file_name = "{}-{}-{}.json".format(day, month, year)
        # file_name = "01-01-2022.json"
        with open("prayer_timings/{}".format(file_name), 'r') as infile:
            timings = json.load(infile)
            print(timings)

        for prayer_time in timings.keys():
            if prayer_time != 'Fajr':
                schedule.every().day.at(timings[prayer_time]).do(self.play_azaan_normal)
            else:
                schedule.every().day.at(timings[prayer_time]).do(self.play_azaan_fajr)
            print('scheduled {} at {}'.format(prayer_time, timings[prayer_time]))
        self.create_daily_scheduler()

    def play_azaan_fajr(self):
        self.player.play(True)
        return schedule.CancelJob

    def play_azaan_normal(self):
        self.player.play(False)
        return schedule.CancelJob

    def parse_config(self):
        with open("config/config.json", "r") as infile:
            config = json.load(infile)
            host = config['host']
        return host


if __name__ == '__main__':
    a = AzaanServer()
