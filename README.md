## exo\_limits

Take at threshold and boosted Exotica search inputs (cross-section vs mass with
one and two sigma bands) and plot combined limits plot.

## Dependencies

[PyYAML](http://pyyaml.org/)
[SciPy](http://www.scipy.org/)

## Usage

```bash
./overlay_main.py --type narrow yaml/lm_narrow.yaml yaml/hm_narrow.yaml
# turn off data smoothing
./overlay_main.py --type narrow yaml/lm_narrow.yaml yaml/hm_narrow.yaml --no-smooth
# get help
./overlay_main.py --type narrow yaml/lm_narrow.yaml yaml/hm_narrow.yaml -h
```

## Input

The input files are passed in YAML format and expected to be of the form:

```yaml
# mass: [central, +sigma, -sigma, +2sigma, -2sigma, observed]
500: [3.01, +1.48, -0.64,  +3.05, -0.83,  2.32]
600: [1.89, +0.80, -0.45,  +1.78, -0.56,  2.37]
```

In some cases the input YAML has asbsolute values, e.g.:

```yaml
# mass: [central, central-sigma, central-sigma, central-2sigma, central+2sigma, observed]
1000: [0.52, 0.38, 0.75, 0.30, 1.07, 0.33]
1050: [0.47, 0.33, 0.63, 0.30, 0.90, 0.31]
```

in this case the latter format can be converted to the accepted one with
script ```convert_main.py```, e.g.:

```bash
convert_main.py input_raw.yaml output.yaml
```

An example YAML files are available in the **yaml** folder.
