import fastf1
from fastf1.plotting import setup_mpl
import matplotlib.pyplot as plt

# Enable caching to avoid re-downloading
fastf1.Cache.enable_cache('cache')

# Load a session
session = fastf1.get_session(2024, 'Silverstone', 'Q')
session.load()

# Pick two drivers
ver = session.laps.pick_driver('VER').pick_fastest()
ham = session.laps.pick_driver('HAM').pick_fastest()

# Get telemetry
ver_tel = ver.get_car_data().add_distance()
ham_tel = ham.get_car_data().add_distance()

# Plot speed vs distance
plt.plot(ver_tel['Distance'], ver_tel['Speed'], label='VER')
plt.plot(ham_tel['Distance'], ham_tel['Speed'], label='HAM')
plt.xlabel('Distance (m)')
plt.ylabel('Speed (km/h)')
plt.legend()
plt.title('Speed Comparison: VER vs HAM - Silverstone Qualifying')
plt.show()
