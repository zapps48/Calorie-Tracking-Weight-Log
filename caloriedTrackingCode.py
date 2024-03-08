import datetime


sex_dic = {'M': 5, 'm': 5, 'F': -166, 'f': -166}
activity_dict = {'S': 1.2, 'LA': 1.375, 'MA': 1.55, 'A': 1.725, 'VA': 1.9}
words = ['Underweight', 'Normal Weight', 'Overweight', 'Obese']


class Point:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2


def main():
    path = input("Calculate Calories (C) or Estimate Weight Loss (WL)\n")
    if 'C' == path:
        final_cals = calc_cals_print(0)
        print(f"\033[31mYour estimated maintenance calories is: {final_cals.num1}\n")
        print(f"\033[31mYour estimated BMI is: {final_cals.num2} ({get_bmi_category(final_cals.num2)})\n")

        exit()
    if 'WL' == path:
        create_weight_log()
        exit()
    else:
        print("INVALID INPUT")
        exit()


def get_bmi_category(bmi):
    if bmi <= 18.5:
        return words[0]
    if 18.5 < bmi < 25:
        return words[1]
    if 25 <= bmi < 30:
        return words[2]
    else:
        return words[3]


def calc_cals_print(n):
    sex_val = sex_dic[input("Enter Sex (M/F):\n")]
    activity_val = activity_dict[input(
        "Enter Activity Level:\nSedentary (S)\nLightly Active (AC)\n"
        "Moderately Active (MA)\nActive (A)\nVery Active (VA)\n")]
    height_val = input("Height (cm or in):\n")
    if n == 0:
        weight_val = input("Weight (lbs or kg):\n")
    else:
        weight_val = n
    age_val = input("Age:\n")
    bmi = round((convert_weight(weight_val) / (((convert_height(height_val)) / 100)**2)), 2)
    final_cal = round(calculate_cals(sex_val, activity_val, height_val, weight_val, age_val))
    return Point(final_cal, bmi)


def calculate_cals(sex, activity, height, weight, age):
    return ((10 * convert_weight(weight)) + (6.25 * convert_height(height))
            - (5 * float(age)) - float(sex)) * float(activity)


def convert_weight(weight):
    if 'lbs' in weight.strip():
        return float(weight.strip().replace('lbs', '')) * 0.45359237
    return float(weight.strip().replace('kg', ''))


def convert_height(height):
    if 'in' in height.strip():
        return float(height.strip().replace('in', '')) * 2.539999962
    return float(height.strip().replace('cm', ''))


def calculate_weight_per_day(sw_val, gw_val, length):
    return (convert_weight(gw_val) - convert_weight(sw_val)) / float(length)


def get_valid_date(prompt):
    while True:
        try:
            date_str = input(prompt + " (YYYY-MM-DD):\n")
            year, month, day = map(int, date_str.split('-'))
            return datetime.date(year, month, day)
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")


def create_weight_log():
    sw_val = input("Starting Weight (kg or lbs)\n")
    gw_val = input("Goal Weight (kg or lbs)\n")
    start_date = get_valid_date("Enter the start date")
    end_date = get_valid_date("Enter the end date")
    date_difference = end_date - start_date
    increment = calculate_weight_per_day(sw_val, gw_val, date_difference.days)
    daily_weight = convert_weight(sw_val)
    current_date = start_date

    if 'Y' in input("Do you want the calorie deficit per day? (Y/N)\n"):
        final_cals = calc_cals_print(sw_val)

        for i in range(date_difference.days + 1):
            print(f"Day {str(i).zfill(3)} ({current_date.strftime('%B %d, %Y')}): "
                  f"Weight: {round(daily_weight, 3)} kg ({round(daily_weight * 2.20462, 3)} lbs)")
            daily_weight += increment
            current_date += datetime.timedelta(days=1)
        print(f"You need to loose {round(abs(increment), 3)} kg ({abs(round((increment * 2.20462), 3))} lbs) every day\n"
              f"({round((abs(increment) * 7), 3)} kg or {round((abs(increment * 2.20462) * 7), 3)} a week)\n"
              f"\nDaily caloric deficit: {round(abs(3500 * increment * 2.20462), 3)} per day"
              f"\n(Eating {round((final_cals.num1 - abs(3500 * increment * 2.20462)), 3)} calories a day)")
    else:
        for i in range(date_difference.days + 1):
            print(f"Day {str(i).zfill(3)} ({current_date.strftime('%B %d, %Y')}): "
                  f"Weight: {round(daily_weight, 3)} kg ({round(daily_weight * 2.20462, 3)} lbs)")
            daily_weight += increment
            current_date += datetime.timedelta(days=1)
        print(f"You need to loose {round(abs(increment), 3)} kg ({abs(round((increment * 2.20462), 3))} lbs) every day\n"
              f"({round((abs(increment) * 7), 3)} kg or {round((abs(increment * 2.20462) * 7), 3)} a week)\n")


if __name__ == "__main__":
    main()
