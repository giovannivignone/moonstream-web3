import argparse


from . import Lootbox, core, MockErc20


def main():
    parser = argparse.ArgumentParser(
        description="dao: The command line interface to Moonstream DAO"
    )
    parser.set_defaults(func=lambda _: parser.print_help())
    subparsers = parser.add_subparsers()

    lootbox_parser = Lootbox.generate_cli()
    subparsers.add_parser("lootbox", parents=[lootbox_parser], add_help=False)

    core_parser = core.generate_cli()
    subparsers.add_parser("core", parents=[core_parser], add_help=False)

    erc20_parser = MockErc20.generate_cli()
    subparsers.add_parser("mock-erc20", parents=[erc20_parser], add_help=False)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
