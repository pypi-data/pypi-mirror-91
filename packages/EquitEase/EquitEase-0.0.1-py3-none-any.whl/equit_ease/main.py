#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
import argparse
from PyInquirer import prompt
import os
from pathlib import Path
import sys

import PyInquirer
from equit_ease.reader.read import Reader
from equit_ease.parser.parse import QuoteParser, UserConfigParser
from equit_ease.displayer.display import QuoteDisplayer, TrendsDisplayer


# __version__="0.0.1"


def init_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """
    instantiate the parser object with the necessary arguments.

    :param parser -> ``argparse.ArgumentParser``: a parser object with no arguments added.

    :returns parser -> ``argparse.ArgumentParser``: a parser object containing the needed arguments.
    """
    parser.add_argument(
        "config",
        type=str,
        nargs="?",
        help="""Create a named list of stocks. Run ``equity config`` to create a list and then ``equity --list [LIST]``\nor ``equity -l [LIST]`` to retrieve data for each stock in that list. EXAMPLE:\n>>> equity config\n? List Name: My First List\n? Equities to include in list: CRM, AAPL, MSFT\n>>> equity --list 'My First List'\n[CRM result]\n[AAPL result]\n[MSFT result]"""
    )

    parser.add_argument(
        "--force",
        "-f",
        type=str,
        default="True",
        help="""Deaults to `True`. If `False`, shows a list of all equities returned from the reverse lookup and\nlets you choose which one to display data for. This is useful if you do not know the ticker symbol\nand want to ensure the correct data is displayed. If `True`, sends a request matching the first\nticker returned from the reverse lookup. EXAMPLE:\n>>>equity --name Bitcoin --force False\n? Select The Correct Equity:\n> BTC-USD [return]\n  GBTC\n  BTCUSD=X\n  BTC-CAD\n  BTC-EUR\n\n[BTC-USD result]\n\n>>> equity --name Bitcoin\n\n[BTC-USD result]\t\t\t(defaults to --force True)\n\n""",
    )

    parser.add_argument(
        "--name", 
        "-n",
        type=str,
        help="""The name or ticker of the equity to retrieve. Since reverse lookup functionality is supported,\nyou can specify `BTC`, `BTC-USD`,or `Bitcoin` and receive the exact same data. EXAMPLE:\n>>> equity --name Bitcoin\n[BTC-USD result]\n>>> equity --name Salesforce\n[CRM result]\n>>> equity --name CRM\n[CRM result]\t\t\t(same as above!)\n\n"""
    )
    parser.add_argument(
        "--list",
        "-l",
        type=str,
        help="""must be a valid list that was configured with ``equity config``. If an invalid list is provided,\na ``argparse.ArgumentError`` is thrown. EXAMPLE:\n>>> equity --list 'My First List'\n[CRM result]\n[AAPL result]\n[MSFT result]\n\n>>> equity --list 'Invalid List Name'\nargparse.ArgumentError: 'Invalid List Name' does not exist. Try: My First List.\n\n"""
    )

    return parser


class ArgsHandler:
    def __init__(self, args_data: argparse.Namespace):
        self.args_data = args_data

    @staticmethod
    def _setup_dir_structure(
        dir_path: Path, list_file_path: Path, answers: PyInquirer.prompt
    ) -> bool:
        """
        make .equit_ease folder in $HOME dir.

        :params dir_path -> ``Path``: a Path object representing an operating system-agnostic path
                                  (works on POSIX and Windows)
        :params list_file_path -> ``Path``: file path for the lists ASCII text file.
        :param answers -> ``PyInquirer.prompt``: answers to the prompt.

        :returns True -> ``bool``:
        """
        dir_path.mkdir()  # create .equit_ease dir in $HOME
        list_file_path.touch()  # create config file
        with open(list_file_path, "w") as f:
            init_list_name = answers["list_name"]
            cleaner = lambda equity_names_list: [
                name.strip() for name in equity_names_list
            ]
            equity_names = answers["equities_in_list"]
            equity_names_formatted = ",".join(cleaner(equity_names.split(",")))

            contents_for_file = (
                f"""[{init_list_name}]\nequity_names = {equity_names_formatted}"""
            )
            f.write(contents_for_file)
        return True

    @staticmethod
    def _add_to_lists(lists_file_path: Path, answers: PyInquirer.prompt) -> bool:
        """
        if the .equit_ease dir already exists, then append to the
        lists ASCII text file in the directory (this file is created
        when the dir is created, so it is expected to already exist).

        :params lists_file_path -> ``Path``: the path to the `lists` ASCII text file.
        :param answers -> ``PyInquirer.prompt``: answers to the prompt.

        :returns True -> ``bool``:
        """
        with open(lists_file_path, "a") as f:
            cleaner = lambda equity_names_list: [
                name.strip() for name in equity_names_list
            ]
            list_name = answers["list_name"]
            equity_names = answers["equities_in_list"]
            equity_names_formatted = ",".join(cleaner(equity_names.split(",")))
            contents_for_file = (
                f"""\n[{list_name}]\nequity_names = {equity_names_formatted}"""
            )
            f.write(contents_for_file)
        return True

    def handle_config(self: ArgsHandler):
        """
        the `config` positional arg takes precedence over other args. If config
        exists in the args, then that is the process that is initiated and handled.

        :param self -> ``ArgsHandler``:

        :returns ``None``:
        """
        questions = [
            {"type": "input", "name": "list_name", "message": "List Name:"},
            {
                "type": "input",
                "name": "equities_in_list",
                "message": "Equities to include in list:",
            },
        ]
        answers = prompt(questions, style=None)

        user_home_dir = os.environ.get("HOME")
        equit_ease_dir_path = os.path.join(user_home_dir, ".equit_ease")
        os_agnostic_path = Path(equit_ease_dir_path)
        config_file_path = Path(os.path.join(equit_ease_dir_path, "lists"))

        if not os.path.exists(os_agnostic_path):
            self._setup_dir_structure(os_agnostic_path, config_file_path, answers)
        else:
            self._add_to_lists(config_file_path, answers)

    def handle_equity(self):
        """
        if the ``--equity`` or ``-e`` flags are specified, the equity name that
        is provided is used to perform a reverse lookup. The first result from that
        lookup is then used to retrieve data and print it to the console.

        If ``--force`` or ``-f`` is set to `False`, then you are given the flexibility
        of choosing the correct equity from the reverse lookup. This is useful is you
        do not know the exact ticker and want to ensure the correct equity is searched
        for.

        :param self -> ``Reader``:
        """

        def handle_force(use_force: bool):
            """
            used to handle the ``--force`` / ``-f`` flags. If the flag is set
            to True, the first ticker returned from the reverse lookup is used.
            Otherwise, all values from the reverse lookup are displayed and the
            user is prompted to choose which one should be searched.

            :param use_force -> ``bool``: if False, render the propmt. Otherwise, utilize first ticker.
            """
            if use_force == "False":
                long_name, ticker, choices = reader.get_equity_company_data(
                    force=use_force
                )
                questions = [
                    {
                        "type": "list",
                        "name": "Equity_Name",
                        "message": "Select The Correct Equity:",
                        "choices": choices,
                    }
                ]
                answers = prompt(questions, style=None)
                # update equity name based off selection, build new URL, and repeat process
                reader.equity = answers["Equity_Name"]
                reader.build_company_lookup_url()
                long_name, ticker = reader.get_equity_company_data(force="True")
                return long_name, ticker
            else:
                long_name, ticker = reader.get_equity_company_data(
                    force=self.args_data.force
                )
                return long_name, ticker

        reader = Reader(self.args_data.name)
        reader.build_company_lookup_url()

        long_name, ticker = handle_force(self.args_data.force)

        reader.set_ticker_and_name_props_to(ticker, long_name)
        reader.build_urls()

        equity_quote_data = reader.get_data()

        quote_parser = QuoteParser(equity=reader.equity, data=equity_quote_data)
        quote_data = quote_parser.extract_equity_meta_data()

        quote_displayer = QuoteDisplayer(reader.equity, quote_data)
        table = quote_displayer.tabularize()

        trends_displayer = TrendsDisplayer(reader)

        trends_to_retrieve = [
            "chart_one_year_url",
            "chart_six_months_url",
            "chart_three_months_url",
            "chart_one_month_url",
            "chart_five_days_url",
        ]
        (
            equity_one_year_percentage_change,
            equity_six_months_percentage_change,
            equity_three_months_percentage_change,
            equity_one_month_percentage_change,
            equity_five_days_percentage_change,
        ) = trends_displayer.get_percentage_changes(*trends_to_retrieve)

        for row in table:
            print(row)

        print(f"\n{reader.ticker} is:\n")

        trends_displayer.display(equity_one_year_percentage_change, "year")
        trends_displayer.display(equity_six_months_percentage_change, "6 months")
        trends_displayer.display(equity_three_months_percentage_change, "3 months")
        trends_displayer.display(equity_one_month_percentage_change, "1 month")
        trends_displayer.display(equity_five_days_percentage_change, "1 week")


def run():
    parser = argparse.ArgumentParser(
        description="The easiest way to access data about your favorite stocks from the command line.",
        formatter_class= argparse.RawTextHelpFormatter
    )
    parser = init_parser(parser=parser)
    args = parser.parse_args()
    args_handler = ArgsHandler(args)

    if args.config:
        if args.config == "config":
            args_handler.handle_config()
        else:
            parser.error(f"Unrecognized Argument: `{args.config}`.")

    elif args.name:
        args_handler.handle_equity()

    elif args.list:
        user_home_dir = str(Path.home())  # same as os.path.expanduser("~")
        equit_ease_dir = os.path.join(user_home_dir, ".equit_ease")
        lists_file_path = Path(os.path.join(equit_ease_dir, "lists"))

        if not os.path.exists(lists_file_path):
            raise FileNotFoundError(
                "You do not have any lists configured yet. Run ``equity config`` to setup your first list!"
            )
        else:
            with open(lists_file_path, "r") as f:
                file_contents_lines = f.read().splitlines()

            equity_list_name = args.list
            user_config = UserConfigParser(equity_list_name, file_contents_lines)
            (
                list_of_formatted_list_names,
                string_of_all_formatted_list_names,
            ) = user_config.format_equity_lists()

            if equity_list_name not in list_of_formatted_list_names:
                raise argparse.ArgumentError(
                    None, message= f"'{equity_list_name}' does not exist. Try: {string_of_all_formatted_list_names}"
                )
            else:
                equities_to_search = user_config.find_match()

                for equity in equities_to_search:
                    new_args_handler = ArgsHandler(
                        argparse.Namespace(name=equity, force="True")
                    )
                    new_args_handler.handle_equity()

if __name__ == '__main__':
    run()