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

## Usage

```plaintext
usage: walkingsim [-h] {train,t,visualize,vis,v,env,e} ...

optional arguments:
  -h, --help            show this help message and exit

Command:
  {train,t,visualize,vis,v,env,e}
    train (t)           Train a model
    visualize (vis, v)  Visualize a trained model
    env (e)             Manage envs
```

To train a model, you wan use the `train` command:
```plaintext
usage: walkingsim train [-h] [--creature CREATURE] [--target {walking-v0,walking-v1}]
                        [--environment ENVIRONMENT] [--algorithm {ga,ppo}] [--render | --no-render]
                        [--generations GENERATIONS] [--population POPULATION] [--timesteps TIMESTEPS]

optional arguments:
  -h, --help            show this help message and exit

General Options:
  --creature CREATURE, -c CREATURE
                        Creature to use in simulation (default: quadrupede)
  --target {walking-v0,walking-v1}, -t {walking-v0,walking-v1}
                        The fitness function to use (default: walking-v0)
  --environment ENVIRONMENT, -e ENVIRONMENT
                        Environment in which the simulation will be executed (default: default)
  --algorithm {ga,ppo}, -a {ga,ppo}
                        The algorithm to use to train the model (default: ga)
  --render              Do render while training (default: False)
  --no-render           Do not render while training (default: True)

Genetic Algorithm Options:
  --generations GENERATIONS
                        Number of generations (default: None)
  --population POPULATION
                        Size of population (default: None)

RL Algorithms Options:
  --timesteps TIMESTEPS
                        Number of timesteps (default: None)
```

To visualize a trained model, use the `visualize` command:
```plaintext
usage: walkingsim visualize [-h] [--algorithm {ga,ppo}] [--delay DELAY] [date]

positional arguments:
  date                  The date of when the model was trained (default: None)

optional arguments:
  -h, --help            show this help message and exit

General Options:
  --algorithm {ga,ppo}, -a {ga,ppo}
                        The algorithm to visualize (default: ga)
  --delay DELAY, -d DELAY
                        Amount of seconds to wait when simulation is done (default: 0)
```

If you want to see a list of all the available environment, use the `env` command:
```plaintext
usage: walkingsim env [-h] {list,l} ...

optional arguments:
  -h, --help  show this help message and exit

Env Commands:
  {list,l}
    list (l)  List all the available environments
```

## Format

[`black`](https://github.com/psf/black) and [`isort` ](https://github.com/PyCQA/isort) are used to format the code. You can manually format the code using the following commands:
```
isort .
black .
```
