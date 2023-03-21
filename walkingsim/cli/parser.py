from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace

from walkingsim.cli.train import train_ga, train_ppo
from walkingsim.cli.vis import visualize_ga, visualize_ppo
from walkingsim.fitness import fitnesses
from walkingsim.loader import EnvironmentProps


class WalkingSimArgumentParser:
    def __init__(self):
        self.parser = ArgumentParser(
            prog="walkingsim", formatter_class=ArgumentDefaultsHelpFormatter
        )
        self.ns = Namespace()
        self.available_algorithms = ["ga", "ppo"]
        self.available_fitnesses = list(fitnesses.keys())
        self.env_loader = EnvironmentProps("./environments")

        self.commands = self.parser.add_subparsers(
            title="Command", required=True
        )
        self.setup_train_parser()
        self.setup_vis_parser()
        self.setup_env_parser()

    # Setup Parser
    def setup_train_parser(self):
        train_parser = self.commands.add_parser(
            "train",
            help="Train a model",
            aliases=["t"],
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        train_parser.set_defaults(command="train")

        # General Options
        general_options = train_parser.add_argument_group("General Options")
        general_options.add_argument(
            "--creature",
            "-c",
            dest="creature",
            default="quadrupede",
            help="Creature to use in simulation",
        )
        general_options.add_argument(
            "--target",
            "-t",
            dest="target",
            default="walking-v0",
            choices=self.available_fitnesses,
            help="The fitness function to use",
        )
        general_options.add_argument(
            "--environment",
            "-e",
            dest="environment",
            default="default",
            help="Environment in which the simulation will be executed",
        )
        general_options.add_argument(
            "--algorithm",
            "-a",
            dest="algorithm",
            default="ga",
            choices=self.available_algorithms,
            help="The algorithm to use to train the model",
        )
        general_options.add_argument(
            "--timestep",
            dest="timestep",
            default=1e-2,
            type=float,
            help="The duration of a timestep",
        )
        general_options.add_argument(
            "--duration",
            "-d",
            dest="duration",
            default=5,
            type=int,
            help="The maximum duration of a single simulation",
        )
        render_group = general_options.add_mutually_exclusive_group()
        render_group.add_argument(
            "--render",
            action="store_true",
            dest="render",
            help="Do render while training",
        )
        render_group.add_argument(
            "--no-render",
            action="store_false",
            dest="render",
            help="Do not render while training",
        )

        # Genetic Algorithm Options
        ga_algo_options = train_parser.add_argument_group(
            "Genetic Algorithm Options"
        )
        ga_algo_options.add_argument(
            "--generations",
            dest="generations",
            type=int,
            help="Number of generations",
        )
        ga_algo_options.add_argument(
            "--population",
            dest="population",
            type=int,
            help="Size of population",
        )
        ga_algo_options.add_argument(
            "--cycle-timesteps",
            dest="cycle_timesteps",
            type=int,
            default=500,
            help="Number of timesteps per cycle",
        )

        # RL Algorithm Options
        rl_algo_options = train_parser.add_argument_group(
            "RL Algorithms Options"
        )
        rl_algo_options.add_argument(
            "--timesteps",
            dest="timesteps",
            type=int,
            help="Number of timesteps",
        )

    def setup_vis_parser(self):
        vis_parser = self.commands.add_parser(
            "visualize",
            help="Visualize a trained model",
            aliases=["vis", "v"],
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        vis_parser.set_defaults(command="visualize")

        vis_parser.add_argument(
            "date", nargs="?", help="The date of when the model was trained"
        )

        # General Options
        general_options = vis_parser.add_argument_group("General Options")
        general_options.add_argument(
            "--algorithm",
            "-a",
            dest="algorithm",
            default="ga",
            choices=self.available_algorithms,
            help="The algorithm to visualize",
        )
        general_options.add_argument(
            "--timestep",
            dest="timestep",
            default=1e-2,
            type=float,
            help="The duration of a timestep",
        )
        general_options.add_argument(
            "--delay",
            "-d",
            dest="delay",
            type=int,
            default=0,
            help=" Amount of seconds to wait when simulation is done",
        )

    def setup_env_parser(self):
        env_parser = self.commands.add_parser(
            "env",
            help="Manage envs",
            aliases=["e"],
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        env_parser.set_defaults(command="env")

        env_commands = env_parser.add_subparsers(
            title="Env Commands", dest="env_command"
        )
        env_commands.add_parser(
            "list", help="List all the available environments", aliases=["l"]
        )

    # Handle Commands
    def handle_train(self):
        if self.ns.algorithm == "ga":
            if self.ns.generations is None or self.ns.population is None:
                self.parser.error(
                    "When using GA algorithm, you must pass --generations and --population"
                )

            train_ga(
                creature=self.ns.creature,
                env=self.ns.env,
                visualize=self.ns.render,
                timestep=self.ns.timestep,
                duration=self.ns.duration,
                timesteps=self.ns.cycle_timesteps,
                population_size=self.ns.population,
                num_generations=self.ns.generations,
            )
        elif self.ns.algorithm == "ppo":
            if self.ns.timesteps is None:
                self.parser.error(
                    "When using any RL algorithms, you must pass --timesteps"
                )

            train_ppo(
                creature=self.ns.creature,
                env=self.ns.env,
                visualize=self.ns.render,
                duration=self.ns.duration,
                timestep=self.ns.timestep,
                timesteps=self.ns.timesteps,
            )

    def handle_visualize(self):
        if self.ns.algorithm == "ga":
            visualize_ga(
                date=self.ns.date,
                timestep=self.ns.timestep,
                delay=self.ns.delay,
            )
        elif self.ns.algorithm == "ppo":
            visualize_ppo(
                date=self.ns.date,
                timestep=self.ns.timestep,
                delay=self.ns.delay,
            )

    def handle_env(self):
        if self.ns.env_command == "list":
            envs = self.env_loader.list()
            for env, description in envs.items():
                print(f"{env}: {description}")

    # Run
    def run(self):
        self.parser.parse_args(namespace=self.ns)
        if self.ns.command == "train":
            try:
                self.ns.env = self.env_loader.load(self.ns.environment)
            except FileNotFoundError:
                self.parser.error(
                    f"Invalid environment '{self.ns.environment}'"
                )

            self.handle_train()
        elif self.ns.command == "visualize":
            self.handle_visualize()
        elif self.ns.command == "env":
            self.handle_env()
