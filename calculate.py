import interaction_force


from config import load_parameters
from interaction_force import generate_force_csv


config = load_parameters("parameters.txt")


generate_force_csv(
    start_m=config["start_m"], 
    end_m=config["end_m"], 
    step_m=config["step_m"],
    filename=config["filename"],
    B_z=config["B_z"],
    h=config["h"],
    r_in=config["r_in"],
    r_out=config["r_out"]
)