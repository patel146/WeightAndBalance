from CSV_Handler import inputs
from datetime import datetime
import csv
import pandas


def log_inputs():
    print(inputs.loc[:, ["Value", "units"]])


def log_results(results):
    print(results)


def log_weights(aircraft):
    for name, system in aircraft.systems.items():
        print(system.name, system.weight, system.loc, sep='\t')


def get_var_name(variable):
    globals_dict = globals()

    return [var_name for var_name in globals_dict if globals_dict[var_name] is variable]


def create_log_file(results, aircraft):
    now = str(datetime.now())
    now = now.replace(' ', '')
    now = now.replace(':', '-')
    file_name = "Logs\\" + now + '.csv'
    input_df = inputs.loc[:, ["Value", "units"]]
    input_df.to_csv(file_name)
    with open(file_name, 'a', newline='') as log_file:
        writer = csv.writer(log_file, dialect='excel-tab')
        writer.writerow(["System", "Weight [lbf]", "Location [% lf]"])
        for name, system in aircraft.systems.items():
            writer.writerow([system.name, system.weight, system.loc])

        writer.writerow(["Result", "Value", "Units"])
        for name, value in results.items():
            writer.writerow([name, value[0], value[1]])
