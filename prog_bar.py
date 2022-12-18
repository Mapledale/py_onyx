import datetime
import time

from tqdm import tqdm


def is_leap(year: int) -> bool:
    if year % 4 == 0:
        if year % 100 != 0:
            return True
        elif year % 400 == 0:
            return True
    return False


def main():
    today = datetime.date.today()
    year = today.year
    day_first = datetime.date(year, 1, 1)


    day_cnt_today = (today - day_first).days + 1
    if is_leap(year):
        day_cnt_year = 365
    else:
        day_cnt_year = 366

    with tqdm(total=day_cnt_year,
    bar_format='Today within this year: {percentage:3.0f}%|{bar:20}') as pbar:
    # bar_format='Today within this year: {desc} {percentage:3.0f}%|{bar:10}') as pbar:
        for i in range(day_cnt_today):
            time.sleep(0.05)
            pbar.update(1)


if __name__ == '__main__':
    main()
