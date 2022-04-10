import requests
import json

METHOD_WORLD_MUSLIM_LEAGUE = 3
PREFERRED_SCHOOL = 0
PRAYERS_TO_REMOVE = ['Sunrise', 'Sunset', "Imsak", "Midnight"]


class Updater:
    def __init__(self):
        return

    def get_prayer_times_by_address(self, address, year):
        params = {
            "address": address,
            "month": 1,
            "year": year,
            "annual": "true",
            "method": METHOD_WORLD_MUSLIM_LEAGUE,
            "school": PREFERRED_SCHOOL
        }
        r = requests.get('http://api.aladhan.com/v1/calendarByAddress', params=params)
        data = json.loads(r.text)['data']
        for month in data.keys():
            days = data[month]
            for day in days:
                date = day['date']['gregorian']['date']
                timings = day['timings']
                for prayer_to_remove in PRAYERS_TO_REMOVE:
                    timings.pop(prayer_to_remove)
                for time in timings:
                    timings[time] = timings[time][0:5]
                print('date: {}\n timings: {}'.format(date, timings))
                with open('./prayer_timings/{}.json'.format(date), 'w') as outfile:
                    json.dump(timings, outfile)




if __name__ == '__main__':
    u = Updater()
    u.get_prayer_times_by_address("2/1 world's end close, 10 high street, edinburgh, eh11td", 2022)

