## convert_main.py

The script will convert high mass YAML data to the format accepted by plotting
tool.

## Run

```bash
# get help
./convert_main.py
./convert_main.py -h
./convert_main.py --help
#
# basic run
./convert_main.py input.yaml output.yaml
#
# verbose run
./convert_main.py -v input.yaml output.yaml
#
# overwrite output file if one exists (default: do NO overwrite)
./convert_main.py -f input.yaml output.yaml
```

## How it works

The script reads input file which is expected to be a set of lines:

    X: [expected, y_sigma_down, y_sigma_up, y_2sigma_down, y_2sigma_up, observed]

and will write in output file converted data in format:

    X: [expected, sigma_up, sigma_down, 2sigma_up, 2sigma_down, observed]

note the swap of sgiam UP and DOWN values in output

## Example

**input**

```
10: [50, 40, 60, 30, 70, 55]
15: [45, 40, 50, 35, 55, 44]
```

**output**

```
10: [50, 10, -10, 20, -20, 55]
15: [45, 5, -5, 10, -10, 44]
```
