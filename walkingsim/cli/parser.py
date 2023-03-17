from argparse import Action, ArgumentParser

from loguru import logger

from walkingsim.cli.train import GA_Train, GYM_Train
from walkingsim.cli.vis import GA_Vis, GYM_Vis
from walkingsim.loader import EnvironmentProps


class EnvironmentArgumentAction(Action):
    """This is a custom Action for argparse. It automatically loads the environment props"""

    def __init__(
        self, option_strings, dest, required=False, help=None, metavar=None
    ) -> None:
        default_env_props = EnvironmentProps("./environments").load("default")
        super().__init__(
            option_strings,
            dest,
            None,
            None,
            default_env_props,
            str,
            ["default", "moon", "mars"],
            required,
            help,
            metavar,
        )

    def __call__(
        self, parser: ArgumentParser, namespace, values, option_string=None
    ) -> None:
        env_props = EnvironmentProps("./environments").load(values)
        setattr(namespace, self.dest, env_props)


class WalkingSimArgumentParser:
    def __init__(self) -> None:
        self.parser = ArgumentParser()
        self.commands = self.parser.add_subparsers(title="Commands")
        self._setup_train_parser()
        self._setup_vis_parser()

    def _setup_train_parser(self):
        parser = self.commands.add_parser("train")
        parser.set_defaults(func=self.train)
        parser.add_argument("creature", type=str)

        # General Options
        general_options = parser.add_argument_group("General Options")
        general_options.add_argument(
            "--environment",
            "-e",
            action=EnvironmentArgumentAction,
            dest="environment",
        )
        general_options.add_argument(
            "--target", "-t", default="walk", type=str, dest="target"
        )
        general_options.add_argument(
            "--render", action="store_true", default=False, dest="do_render"
        )
        general_options.add_argument(
            "--use-gym", action="store_true", default=False, dest="use_gym"
        )

        # Genetic Algorithm options
        ga_options = parser.add_argument_group("Genetic Algorithm Options")
        ga_options.add_argument(
            "--process", action="store_true", dest="use_multiprocessing"
        )
        ga_options.add_argument(
            "--workers", "-w", default=None, type=str, dest="workers"
        )
        ga_options.add_argument(
            "--generations", type=int, dest="num_generations"
        )
        ga_options.add_argument(
            "--population", type=int, dest="population_size"
        )

        # Gym Options
        gym_options = parser.add_argument_group("Gym Options")
        gym_options.add_argument(
            "--algo", default="PPO", type=str, dest="gym_algo"
        )
        gym_options.add_argument("--timesteps", type=int, dest="gym_timesteps")
        gym_options.add_argument(
            "--progress", action="store_true", dest="gym_progress_bar"
        )

    def _setup_vis_parser(self):
        parser = self.commands.add_parser("vis")
        parser.set_defaults(func=self.visualize)

        # General Options
        general_options = parser.add_argument_group("General Options")
        parser.add_argument("--date", type=str, default=None, dest="date")
        general_options.add_argument(
            "--ending-delay", type=int, default=0, dest="ending_delay"
        )  # in secs
        general_options.add_argument(
            "--use-gym", action="store_true", dest="use_gym", default=False
        )

    def train(self, args):
        if not args.use_gym:
            if args.population_size is None or args.num_generations is None:
                logger.error(
                    "When using the genetic algorithm, you must pass the --population and --generations argument"
                )
                return -1

            return GA_Train(
                creature=args.creature,
                env=args.environment,
                population_size=args.population_size,
                num_generations=args.num_generations,
                workers=args.workers,
                use_multiprocessing=args.use_multiprocessing,
                visualize=args.do_render,
            ).run()
        else:
            if args.gym_timesteps is None:
                logger.error(
                    "When using gym, you must pass the --timesteps argument"
                )
                return -1

            return GYM_Train(
                creature=args.creature,
                env=args.environment,
                timesteps=args.gym_timesteps,
                algo=args.gym_algo,
                show_progress=args.gym_progress_bar,
                visualize=args.do_render,
            ).run()

    def visualize(self, args):
        if args.use_gym:
            return GYM_Vis(args.date).run()
        else:
            return GA_Vis(args.date, args.ending_delay).run()

    def run(self):
        args = self.parser.parse_args()
        if args.func is None:
            raise RuntimeError("An error occured !")

        return args.func(args)
