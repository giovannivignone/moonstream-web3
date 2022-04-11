# Code generated by moonworm : https://github.com/bugout-dev/moonworm
# Moonworm version : 0.1.18

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from brownie import Contract, network, project
from brownie.network.contract import ContractContainer
from eth_typing.evm import ChecksumAddress


PROJECT_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BUILD_DIRECTORY = os.path.join(PROJECT_DIRECTORY, "build", "contracts")


def boolean_argument_type(raw_value: str) -> bool:
    TRUE_VALUES = ["1", "t", "y", "true", "yes"]
    FALSE_VALUES = ["0", "f", "n", "false", "no"]

    if raw_value.lower() in TRUE_VALUES:
        return True
    elif raw_value.lower() in FALSE_VALUES:
        return False

    raise ValueError(
        f"Invalid boolean argument: {raw_value}. Value must be one of: {','.join(TRUE_VALUES + FALSE_VALUES)}"
    )


def bytes_argument_type(raw_value: str) -> str:
    return raw_value


def get_abi_json(abi_name: str) -> List[Dict[str, Any]]:
    abi_full_path = os.path.join(BUILD_DIRECTORY, f"{abi_name}.json")
    if not os.path.isfile(abi_full_path):
        raise IOError(
            f"File does not exist: {abi_full_path}. Maybe you have to compile the smart contracts?"
        )

    with open(abi_full_path, "r") as ifp:
        build = json.load(ifp)

    abi_json = build.get("abi")
    if abi_json is None:
        raise ValueError(f"Could not find ABI definition in: {abi_full_path}")

    return abi_json


def contract_from_build(abi_name: str) -> ContractContainer:
    # This is workaround because brownie currently doesn't support loading the same project multiple
    # times. This causes problems when using multiple contracts from the same project in the same
    # python project.
    PROJECT = project.main.Project("moonworm", Path(PROJECT_DIRECTORY))

    abi_full_path = os.path.join(BUILD_DIRECTORY, f"{abi_name}.json")
    if not os.path.isfile(abi_full_path):
        raise IOError(
            f"File does not exist: {abi_full_path}. Maybe you have to compile the smart contracts?"
        )

    with open(abi_full_path, "r") as ifp:
        build = json.load(ifp)

    return ContractContainer(PROJECT, build)


class MockERC721:
    def __init__(self, contract_address: Optional[ChecksumAddress]):
        self.contract_name = "MockERC721"
        self.address = contract_address
        self.contract = None
        self.abi = get_abi_json("MockERC721")
        if self.address is not None:
            self.contract: Optional[Contract] = Contract.from_abi(
                self.contract_name, self.address, self.abi
            )

    def deploy(self, transaction_config):
        contract_class = contract_from_build(self.contract_name)
        deployed_contract = contract_class.deploy(transaction_config)
        self.address = deployed_contract.address
        self.contract = deployed_contract

    def assert_contract_is_instantiated(self) -> None:
        if self.contract is None:
            raise Exception("contract has not been instantiated")

    def verify_contract(self):
        self.assert_contract_is_instantiated()
        contract_class = contract_from_build(self.contract_name)
        contract_class.publish_source(self.contract)

    def approve(self, to: ChecksumAddress, token_id: int, transaction_config) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.approve(to, token_id, transaction_config)

    def balance_of(self, owner: ChecksumAddress) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.balanceOf.call(owner)

    def get_approved(self, token_id: int) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.getApproved.call(token_id)

    def is_approved_for_all(
        self, owner: ChecksumAddress, operator: ChecksumAddress
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.isApprovedForAll.call(owner, operator)

    def mint(self, to: ChecksumAddress, token_id: int, transaction_config) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.mint(to, token_id, transaction_config)

    def name(self) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.name.call()

    def owner_of(self, token_id: int) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.ownerOf.call(token_id)

    def safe_transfer_from(
        self,
        from_: ChecksumAddress,
        to: ChecksumAddress,
        token_id: int,
        transaction_config,
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.safeTransferFrom(from_, to, token_id, transaction_config)

    def safe_transfer_from(
        self,
        from_: ChecksumAddress,
        to: ChecksumAddress,
        token_id: int,
        _data: bytes,
        transaction_config,
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.safeTransferFrom(
            from_, to, token_id, _data, transaction_config
        )

    def set_approval_for_all(
        self, operator: ChecksumAddress, approved: bool, transaction_config
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.setApprovalForAll(operator, approved, transaction_config)

    def supports_interface(self, interface_id: bytes) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.supportsInterface.call(interface_id)

    def symbol(self) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.symbol.call()

    def token_by_index(self, index: int) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.tokenByIndex.call(index)

    def token_of_owner_by_index(self, owner: ChecksumAddress, index: int) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.tokenOfOwnerByIndex.call(owner, index)

    def token_uri(self, token_id: int) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.tokenURI.call(token_id)

    def total_supply(self) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.totalSupply.call()

    def transfer_from(
        self,
        from_: ChecksumAddress,
        to: ChecksumAddress,
        token_id: int,
        transaction_config,
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.transferFrom(from_, to, token_id, transaction_config)


def get_transaction_config(args: argparse.Namespace) -> Dict[str, Any]:
    signer = network.accounts.load(args.sender, args.password)
    transaction_config: Dict[str, Any] = {"from": signer}
    if args.gas_price is not None:
        transaction_config["gas_price"] = args.gas_price
    if args.max_fee_per_gas is not None:
        transaction_config["max_fee"] = args.max_fee_per_gas
    if args.max_priority_fee_per_gas is not None:
        transaction_config["priority_fee"] = args.max_priority_fee_per_gas
    if args.confirmations is not None:
        transaction_config["required_confs"] = args.confirmations
    if args.nonce is not None:
        transaction_config["nonce"] = args.nonce
    return transaction_config


def add_default_arguments(parser: argparse.ArgumentParser, transact: bool) -> None:
    parser.add_argument(
        "--network", required=True, help="Name of brownie network to connect to"
    )
    parser.add_argument(
        "--address", required=False, help="Address of deployed contract to connect to"
    )
    if not transact:
        return
    parser.add_argument(
        "--sender", required=True, help="Path to keystore file for transaction sender"
    )
    parser.add_argument(
        "--password",
        required=False,
        help="Password to keystore file (if you do not provide it, you will be prompted for it)",
    )
    parser.add_argument(
        "--gas-price", default=None, help="Gas price at which to submit transaction"
    )
    parser.add_argument(
        "--max-fee-per-gas",
        default=None,
        help="Max fee per gas for EIP1559 transactions",
    )
    parser.add_argument(
        "--max-priority-fee-per-gas",
        default=None,
        help="Max priority fee per gas for EIP1559 transactions",
    )
    parser.add_argument(
        "--confirmations",
        type=int,
        default=None,
        help="Number of confirmations to await before considering a transaction completed",
    )
    parser.add_argument(
        "--nonce", type=int, default=None, help="Nonce for the transaction (optional)"
    )
    parser.add_argument(
        "--value", default=None, help="Value of the transaction in wei(optional)"
    )


def handle_deploy(args: argparse.Namespace) -> None:
    network.connect(args.network)
    transaction_config = get_transaction_config(args)
    contract = MockERC721(None)
    result = contract.deploy(transaction_config=transaction_config)
    print(result)


def handle_verify_contract(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MockERC721(args.address)
    result = contract.verify_contract()
    print(result)


def handle_approve(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MockERC721(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.approve(
        to=args.to, token_id=args.token_id, transaction_config=transaction_config
    )
    print(result)


def handle_balance_of(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MockERC721(args.address)
    result = contract.balance_of(owner=args.owner)
    print(result)


def handle_get_approved(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MockERC721(args.address)
    result = contract.get_approved(token_id=args.token_id)
    print(result)


def handle_is_approved_for_all(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MockERC721(args.address)
    result = contract.is_approved_for_all(owner=args.owner, operator=args.operator)
    print(result)


def handle_mint(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MockERC721(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.mint(
        to=args.to, token_id=args.token_id, transaction_config=transaction_config
    )
    print(result)


def handle_name(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MockERC721(args.address)
    result = contract.name()
    print(result)


def handle_owner_of(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MockERC721(args.address)
    result = contract.owner_of(token_id=args.token_id)
    print(result)


def handle_safe_transfer_from(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MockERC721(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.safe_transfer_from(
        from_=args.from_arg,
        to=args.to,
        token_id=args.token_id,
        transaction_config=transaction_config,
    )
    print(result)


def handle_safe_transfer_from(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MockERC721(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.safe_transfer_from(
        from_=args.from_arg,
        to=args.to,
        token_id=args.token_id,
        _data=args.data_arg,
        transaction_config=transaction_config,
    )
    print(result)


def handle_set_approval_for_all(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MockERC721(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.set_approval_for_all(
        operator=args.operator,
        approved=args.approved,
        transaction_config=transaction_config,
    )
    print(result)


def handle_supports_interface(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MockERC721(args.address)
    result = contract.supports_interface(interface_id=args.interface_id)
    print(result)


def handle_symbol(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MockERC721(args.address)
    result = contract.symbol()
    print(result)


def handle_token_by_index(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MockERC721(args.address)
    result = contract.token_by_index(index=args.index)
    print(result)


def handle_token_of_owner_by_index(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MockERC721(args.address)
    result = contract.token_of_owner_by_index(owner=args.owner, index=args.index)
    print(result)


def handle_token_uri(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MockERC721(args.address)
    result = contract.token_uri(token_id=args.token_id)
    print(result)


def handle_total_supply(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MockERC721(args.address)
    result = contract.total_supply()
    print(result)


def handle_transfer_from(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MockERC721(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.transfer_from(
        from_=args.from_arg,
        to=args.to,
        token_id=args.token_id,
        transaction_config=transaction_config,
    )
    print(result)


def generate_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CLI for MockERC721")
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers()

    deploy_parser = subcommands.add_parser("deploy")
    add_default_arguments(deploy_parser, True)
    deploy_parser.set_defaults(func=handle_deploy)

    verify_contract_parser = subcommands.add_parser("verify-contract")
    add_default_arguments(verify_contract_parser, False)
    verify_contract_parser.set_defaults(func=handle_verify_contract)

    approve_parser = subcommands.add_parser("approve")
    add_default_arguments(approve_parser, True)
    approve_parser.add_argument("--to", required=True, help="Type: address")
    approve_parser.add_argument(
        "--token-id", required=True, help="Type: uint256", type=int
    )
    approve_parser.set_defaults(func=handle_approve)

    balance_of_parser = subcommands.add_parser("balance-of")
    add_default_arguments(balance_of_parser, False)
    balance_of_parser.add_argument("--owner", required=True, help="Type: address")
    balance_of_parser.set_defaults(func=handle_balance_of)

    get_approved_parser = subcommands.add_parser("get-approved")
    add_default_arguments(get_approved_parser, False)
    get_approved_parser.add_argument(
        "--token-id", required=True, help="Type: uint256", type=int
    )
    get_approved_parser.set_defaults(func=handle_get_approved)

    is_approved_for_all_parser = subcommands.add_parser("is-approved-for-all")
    add_default_arguments(is_approved_for_all_parser, False)
    is_approved_for_all_parser.add_argument(
        "--owner", required=True, help="Type: address"
    )
    is_approved_for_all_parser.add_argument(
        "--operator", required=True, help="Type: address"
    )
    is_approved_for_all_parser.set_defaults(func=handle_is_approved_for_all)

    mint_parser = subcommands.add_parser("mint")
    add_default_arguments(mint_parser, True)
    mint_parser.add_argument("--to", required=True, help="Type: address")
    mint_parser.add_argument(
        "--token-id", required=True, help="Type: uint256", type=int
    )
    mint_parser.set_defaults(func=handle_mint)

    name_parser = subcommands.add_parser("name")
    add_default_arguments(name_parser, False)
    name_parser.set_defaults(func=handle_name)

    owner_of_parser = subcommands.add_parser("owner-of")
    add_default_arguments(owner_of_parser, False)
    owner_of_parser.add_argument(
        "--token-id", required=True, help="Type: uint256", type=int
    )
    owner_of_parser.set_defaults(func=handle_owner_of)

    safe_transfer_from_parser = subcommands.add_parser("safe-transfer-from")
    add_default_arguments(safe_transfer_from_parser, True)
    safe_transfer_from_parser.add_argument(
        "--from-arg", required=True, help="Type: address"
    )
    safe_transfer_from_parser.add_argument("--to", required=True, help="Type: address")
    safe_transfer_from_parser.add_argument(
        "--token-id", required=True, help="Type: uint256", type=int
    )
    safe_transfer_from_parser.set_defaults(func=handle_safe_transfer_from)

    safe_transfer_from_parser = subcommands.add_parser("safe-transfer-from")
    add_default_arguments(safe_transfer_from_parser, True)
    safe_transfer_from_parser.add_argument(
        "--from-arg", required=True, help="Type: address"
    )
    safe_transfer_from_parser.add_argument("--to", required=True, help="Type: address")
    safe_transfer_from_parser.add_argument(
        "--token-id", required=True, help="Type: uint256", type=int
    )
    safe_transfer_from_parser.add_argument(
        "--data-arg", required=True, help="Type: bytes", type=bytes_argument_type
    )
    safe_transfer_from_parser.set_defaults(func=handle_safe_transfer_from)

    set_approval_for_all_parser = subcommands.add_parser("set-approval-for-all")
    add_default_arguments(set_approval_for_all_parser, True)
    set_approval_for_all_parser.add_argument(
        "--operator", required=True, help="Type: address"
    )
    set_approval_for_all_parser.add_argument(
        "--approved", required=True, help="Type: bool", type=boolean_argument_type
    )
    set_approval_for_all_parser.set_defaults(func=handle_set_approval_for_all)

    supports_interface_parser = subcommands.add_parser("supports-interface")
    add_default_arguments(supports_interface_parser, False)
    supports_interface_parser.add_argument(
        "--interface-id", required=True, help="Type: bytes4", type=bytes_argument_type
    )
    supports_interface_parser.set_defaults(func=handle_supports_interface)

    symbol_parser = subcommands.add_parser("symbol")
    add_default_arguments(symbol_parser, False)
    symbol_parser.set_defaults(func=handle_symbol)

    token_by_index_parser = subcommands.add_parser("token-by-index")
    add_default_arguments(token_by_index_parser, False)
    token_by_index_parser.add_argument(
        "--index", required=True, help="Type: uint256", type=int
    )
    token_by_index_parser.set_defaults(func=handle_token_by_index)

    token_of_owner_by_index_parser = subcommands.add_parser("token-of-owner-by-index")
    add_default_arguments(token_of_owner_by_index_parser, False)
    token_of_owner_by_index_parser.add_argument(
        "--owner", required=True, help="Type: address"
    )
    token_of_owner_by_index_parser.add_argument(
        "--index", required=True, help="Type: uint256", type=int
    )
    token_of_owner_by_index_parser.set_defaults(func=handle_token_of_owner_by_index)

    token_uri_parser = subcommands.add_parser("token-uri")
    add_default_arguments(token_uri_parser, False)
    token_uri_parser.add_argument(
        "--token-id", required=True, help="Type: uint256", type=int
    )
    token_uri_parser.set_defaults(func=handle_token_uri)

    total_supply_parser = subcommands.add_parser("total-supply")
    add_default_arguments(total_supply_parser, False)
    total_supply_parser.set_defaults(func=handle_total_supply)

    transfer_from_parser = subcommands.add_parser("transfer-from")
    add_default_arguments(transfer_from_parser, True)
    transfer_from_parser.add_argument("--from-arg", required=True, help="Type: address")
    transfer_from_parser.add_argument("--to", required=True, help="Type: address")
    transfer_from_parser.add_argument(
        "--token-id", required=True, help="Type: uint256", type=int
    )
    transfer_from_parser.set_defaults(func=handle_transfer_from)

    return parser


def main() -> None:
    parser = generate_cli()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
