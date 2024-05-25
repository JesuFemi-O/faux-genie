from database.db_utils import start_application
from faux.simulator.sim_utils import create_simulation
from faux.database.db_utils import write_to_sink

if __name__ == "__main__":
    start_application()
    sim_data = create_simulation(n=100)
    write_to_sink(data=sim_data)
