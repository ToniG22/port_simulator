# Port Simulator

This project simulates the operation of a recreational port for electric boats. It models boat energy usage, trip assignments, and charging logic using Python.

## Features

- Define electric boats with battery and motor specs
- Create scheduled trips with distance and time
- Assign trips to boats and simulate energy consumption
- Simulate port-side charging with power constraints
- Modular structure with logging and colored output

## Project Structure

```
port_digital_twin/
├── main.py              # Simulation entry point
├── simulation/
│   ├── port.py          # Port class and logic
│   ├── boat.py          # Boat class and logic
│   ├── trip.py          # Trip scheduling and simulation
│   └── optimizer.py     # (TBD) Optimization logic
├── docs/
│   └── index.html
```

## Requirements

- Python 3.8+
- Install with:

```bash
pip install -r requirements.txt
```

## Usage

Run the simulation:

```bash
python main.py
```

## Docs

Open the index.html file inside docs folder.

## License

TBD
