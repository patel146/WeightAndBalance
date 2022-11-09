from CSV_Handler import inputs


def log_inputs():
    print(inputs.loc[:, ["Value", "units"]])


def log_results(results):
    print(results)
