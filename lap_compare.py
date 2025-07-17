import fastf1
import matplotlib.pyplot as plt

def main():
    """
    Main function to run the F1 Lap Comparison tool.
    
    Guides the user through selecting a season year, Grand Prix event,
    session type, drivers to compare, and telemetry data type. Then loads
    and visualizes the selected telemetry data.
    """
    fastf1.Cache.enable_cache('cache')
    print("Welcome to the unofficial F1 Lap Comparison tool, powered by the fastf1 python library.")

    year_input=select_year()
    grand_prix_input=select_grand_prix(year_input)
    session_type_input=select_session_type()
    session_input, drivers_input= load_session(year_input, grand_prix_input, session_type_input)
    driver_codes_input=select_drivers(drivers_input, session_input)
    compared_input, compared_unit_input = select_comparison ()

    plot_telemetry(driver_codes_input, session_input, compared_input, compared_unit_input)
    plot_comparison(compared_input, grand_prix_input, year_input, session_type_input, driver_codes_input)  

def select_year():
    """
    Prompt the user to enter a valid F1 season year (2018–2024).
    
    Returns:
        int: The selected year.
    """
    year=int(input("\nStart by inputting Year (2018-2024):"))
    while year<2018 or year>2024:
        year=int(input("Please ensure your selected year is within the accepted range of years (2018-2024)\n>"))
    return year

def select_grand_prix(year):
    """
    Display a list of Grand Prix events for a given year and prompt user selection.
    
    Args:
        year (int): The F1 season year.
    
    Returns:
        str: The selected Grand Prix name.
    """
    grand_prix_list=sorted(fastf1.get_event_schedule(year)['EventName'].unique())
    print(f"\nSelect one of {year}'s Grand Prixs:")
    for i, name in enumerate(grand_prix_list, 1):
        print(f"[{i}] {name}")
    grand_prix_selection=(input(">"))
    while True:
        try:
            grand_prix=grand_prix_list[int(grand_prix_selection)-1]
            print(f"{grand_prix} selected.")
            break
        except:
            grand_prix_selection=input("Please ensure that your selection is the number associated with your desired Grand Prix\n>")
    return grand_prix

def select_session_type():
    """
    Prompt the user to select the session type (FP1, FP2, Q, or R).
    
    Returns:
        str: The selected session type code.
    """
    session_types=["FP1", "FP2", "Q", "R"]
    session_type_selection=input("\nWhat session type?\n[1] Free Practice 1 (FP1)\n[2] Free Practice 2 (FP2)\n[3] Qualifying (Q)\n[4] Race (R)\n>")
    while session_type_selection not in ("1", "2", "3", "4"):
        session_type_selection=input("Please ensure that your selection is the number associated with your desired session type\n>")
    session_type=session_types[int(session_type_selection)-1]
    return session_type

def load_session(year, grand_prix, session_type):
    """
    Load an F1 session and retrieve the list of drivers for the session.
    
    Args:
        year (int): The F1 season year.
        grand_prix (str): The Grand Prix event name.
        session_type (str): The session type (FP1, FP2, Q, or R).
    
    Returns:
        tuple: A tuple containing the loaded FastF1 session object and list of driver codes.
    """
    print(f"Loading session for {grand_prix} in {year} ({session_type})...\n")
    session = fastf1.get_session(year, grand_prix, session_type)
    try:
        session.load()
        laps = session.laps
        if laps.empty:
            print("\nNo lap data available for this session. Try a different Grand Prix or session.")
            exit()
    except Exception as e:
        print(f"\nFailed to load session data: {e}")
        exit()
    drivers = sorted(session.laps['Driver'].unique())
    return session, drivers

def select_drivers(drivers, session):
    """
    Display available drivers and prompt the user to select drivers to compare.
    
    Args:
        drivers (list): List of driver codes.
        session (Session): Loaded FastF1 session object.
    
    Returns:
        list: List of selected driver codes.
    """
    print("\nNow it's time to choose your racers to compare.\nHere are the available racers: ")
    for code in drivers:
        try:
            name = session.get_driver(code)['FullName']
            print(f"{name} - {code}")
        except:
            print(f"{code}")
    while True:
        driver_codes = [code.strip().upper() for code in input("\nEnter driver codes, separated by commas:\n>").split(",")]
        if all(code in drivers for code in driver_codes):
            break
        else:
            print("One or more driver codes are invalid. Please try again.")
    return driver_codes

def select_comparison():
    """
    Prompt the user to choose a telemetry metric to compare (e.g., Speed, Throttle).
    
    Returns:
        tuple: A tuple containing the selected metric and its units.
    """
    compareds=["Speed", "Throttle", "Brake", "Gear"]
    compared_units=["km/h", "%", "on/off-1/0","gear number"]
    compared_selection=input("\nNow enter what you'd like to compare:\n[1] Speed\n[2] Throttle\n[3] Brake\n[4] Gear\n>")
    while compared_selection not in ("1", "2", "3", "4"):
        compared_selection=input("Please ensure that your selection is the number associated with what you would like to compare.\n>")
    compared_selection=int(compared_selection)
    compared=compareds[compared_selection-1]
    compared_unit=compared_units[compared_selection-1]
    return compared, compared_unit

def plot_telemetry(driver_codes, session, compared, compared_unit):
    """
    Plot telemetry data for each selected driver based on the chosen metric.
    
    Args:
        driver_codes (list): List of driver codes.
        session (Session): Loaded FastF1 session.
        compared (str): The telemetry metric to compare.
        compared_unit (str): Unit of the telemetry metric.
    """
    print("\nPlotting telemetry data..")
    for driver in driver_codes:
        tel=session.laps.pick_driver(driver).pick_fastest().get_car_data().add_distance()
        plt.plot(tel['Distance'], tel[compared], label=driver)
        plt.xlabel('Distance (m)')
        plt.ylabel(f'{compared} ({compared_unit})')

def plot_comparison(compared, grand_prix, year, session_type, driver_codes):
    """
    Display the final plot comparing telemetry data between selected drivers.
    
    Args:
        compared (str): The telemetry metric being compared.
        grand_prix (str): The selected Grand Prix name.
        year (int): The F1 season year.
        session_type (str): The session type (FP1, FP2, Q, R).
        driver_codes (list): List of selected driver codes.
    """
    plt.legend()
    plt.title(f"{compared} Comparison - {grand_prix} {year} ({session_type})\nDrivers: {', '.join(driver_codes)}")
    plt.show()

if __name__=="__main__":
    main()