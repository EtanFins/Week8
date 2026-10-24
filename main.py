import random
import re
import time
from pathlib import Path
from urllib.request import urlretrieve


def sensor_test():
    random.seed(42)

    readings = [random.uniform(18, 30) for i in range(100000)]
    new_readings = [random.uniform(18, 30) for i in range(240)]

    first_before = readings[0]
    last_before = readings[-1]

    start = time.perf_counter()
    for value in new_readings:
        readings.append(value)
    insert_time = (time.perf_counter() - start) * 1000000 / 240

    first_after = readings[0]
    last_after = readings[-1]

    start = time.perf_counter()
    for i in range(100000):
        first = readings[0]
        last = readings[-1]
    find_time = (time.perf_counter() - start) * 1000000 / 200000

    test_readings = readings.copy()

    start = time.perf_counter()
    for i in range(240):
        test_readings.pop()
    delete_time = (time.perf_counter() - start) * 1000000 / 240

    print("\nSituation 1: Sensor measurements")
    print("Starting readings:", 100000)
    print("New readings:", 240)
    print("Total readings:", len(readings))
    print("First reading before:", first_before)
    print("Last reading before:", last_before)
    print("First reading after:", first_after)
    print("Last reading after:", last_after)
    print(f"Find time: {find_time:.4f} microseconds")
    print(f"Insert time: {insert_time:.4f} microseconds")
    print(f"Delete time: {delete_time:.4f} microseconds")

    return [
        f"Sensor find: {find_time:.4f} microseconds",
        f"Sensor insert: {insert_time:.4f} microseconds",
        f"Sensor delete: {delete_time:.4f} microseconds"
    ]


def employee_test():
    file = Path(__file__).resolve().parent / "load_employees.dump"

    if not file.exists():
        print("\nDownloading employee dataset")
        url = "https://raw.githubusercontent.com/datacharmer/test_db/master/load_employees.dump"

        try:
            urlretrieve(url, file)
        except Exception as error:
            print("Could not download employee data:", error)
            return ["Employee test could not run"]

    employees = []
    pattern = re.compile(r"\((\d+),'([^']*)','([^']*)','([^']*)','([MF])','([^']*)'\)")

    with open(file, "r", encoding="utf-8") as data:
        for line in data:
            for match in pattern.finditer(line):
                number, birth, first, last, gender, hired = match.groups()
                employees.append((int(number), first, last, birth, hired, gender))

    if len(employees) == 0:
        print("No employee records found")
        return ["Employee test could not run"]

    original_count = len(employees)
    next_id = max(person[0] for person in employees) + 1

    for i in range(max(0, 1000000 - original_count)):
        person = employees[i % original_count]
        employees.append((next_id + i,) + person[1:])

    start = time.perf_counter()

    employee_index = {}

    for person in employees:
        last_name = person[2].lower()

        if last_name not in employee_index:
            employee_index[last_name] = {}

        employee_index[last_name][person[0]] = person

    build_time = time.perf_counter() - start

    search_name = employees[0][2].lower()

    start = time.perf_counter()
    for i in range(100000):
        found = employee_index.get(search_name)
    find_time = (time.perf_counter() - start) * 1000000 / 100000

    new_employees = []

    for i in range(10000):
        new_employees.append((next_id + 1000000 + i, "Test", search_name,
                              "1990-01-01", "2020-01-01", "M"))

    start = time.perf_counter()
    for person in new_employees:
        employee_index[search_name][person[0]] = person
    insert_time = (time.perf_counter() - start) * 1000000 / 10000

    start = time.perf_counter()
    for person in new_employees:
        del employee_index[search_name][person[0]]
    delete_time = (time.perf_counter() - start) * 1000000 / 10000

    print("\nSituation 2: Employee records")
    print("Original employees:", original_count)
    print("Simulated employees added:", len(employees) - original_count)
    print("Total employees:", len(employees))
    print("Last name searched:", search_name)
    print("Matching employees:", len(found))
    print(f"Index build time: {build_time:.4f} seconds")
    print(f"Find time: {find_time:.4f} microseconds")
    print(f"Insert time: {insert_time:.4f} microseconds")
    print(f"Delete time: {delete_time:.4f} microseconds")

    return [
        f"Original employees: {original_count}",
        f"Total employees: {len(employees)}",
        f"Index build: {build_time:.4f} seconds",
        f"Employee find: {find_time:.4f} microseconds",
        f"Employee insert: {insert_time:.4f} microseconds",
        f"Employee delete: {delete_time:.4f} microseconds"
    ]


sensor_results = sensor_test()
employee_results = employee_test()

results = sensor_results + [""] + employee_results

file = Path(__file__).resolve().parent / "Week8_TimingResults.txt"
file.write_text("\n".join(results))

print("\nsaved")