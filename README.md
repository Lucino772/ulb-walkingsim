# INFO-F308 - Walking simulator - Group G2C

## Install Chrono

You first need to install [Conda](https://docs.conda.io/en/main/index.html) either with [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) or [Miniconda](https://docs.conda.io/en/main/miniconda.html).

The following command will create a virtual environment named `infof308-chrono` and install `pychrono` with all of its dependencies.

```shell
conda env create -f environment.yml
```

To update the environment, you can run the following command:

```shell
conda env update -n infof308-chrono -f environment.yml --prune
```

## Run the simulation

```shell
python -m walkingsim <environment> <creature>
```

All the available environments are contained in the `environments/` directory and all the available creatures are contained in the `creatures/` directory.

For example, to run a simulation in the **default** environment and with the **bipede** creature, you can simply run the following command:

```shell
python -m walkingsim default bipede
```

If you run the command without passing any value, those are the default values.

## Format

[`black`](https://github.com/psf/black) and [`isort` ](https://github.com/PyCQA/isort) are used to format the code. You can manually format the code using the following commands:
```
isort .
black .
```
