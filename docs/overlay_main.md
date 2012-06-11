## overlay_main.py

Given _at threshold_ and _boosted_ limits data (in the yaml format) plot these
together on the same graph with expected and observed limits, error bands and
theoretical curve.

## Run

```bash
# get help
./overlay_main.py
./overlay_main.py -h
./overlay_main.py --help
#
# basic run
./overlay_main.py --type narrow low_mass_narrow.yaml high_mass_narrow.yaml
#
# verbose run (useful for debug)
./overlay_main.py -v --type narrow low_mass_narrow.yaml high_mass_narrow.yaml
```

## How it works

The script reads input file which is expected to be a set of lines:

    X: [expected, sigma_up, sigma_down, 2sigma_up, 2sigma_down, observed]

and plot expected, observed curves with error bands and theory line.

**Hint**: _use convert_main.py for **boosted** data to the above format_
