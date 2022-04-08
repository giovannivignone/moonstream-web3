// SPDX-License-Identifier: Apache-2.0

/**
 * Authors: Moonstream Engineering (engineering@moonstream.to)
 * GitHub: https://github.com/bugout-dev/dao
 */

pragma solidity ^0.8.9;

import "@moonstream/contracts/terminus/TerminusFacet.sol";
import "@openzeppelin-contracts/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin-contracts/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin-contracts/contracts/token/ERC1155/IERC1155.sol";
import "@openzeppelin-contracts/contracts/access/Ownable.sol";
import "@openzeppelin-contracts/contracts/security/Pausable.sol";
import "@openzeppelin-contracts/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin-contracts/contracts/token/ERC721/IERC721Receiver.sol";
import "@openzeppelin-contracts/contracts/token/ERC1155/utils/ERC1155Holder.sol";
import "@openzeppelin-contracts/contracts/utils/cryptography/draft-EIP712.sol";
import "@openzeppelin-contracts/contracts/utils/cryptography/SignatureChecker.sol";

/**
 * @title Moonstream Dropper
 * @author Moonstream Engineering (engineering@moonstream.to)
 * @notice This contract manages drops for ERC20, ERC1155, and ERC721 tokens.
 */
contract Dropper is
    IERC721Receiver,
    ERC1155Holder,
    EIP712,
    Ownable,
    Pausable,
    ReentrancyGuard
{
    // - [x] onERC721Received
    // - [x] onERC1155Received (implemented by ERC1155Holder)
    // - [x] withdrawERC20Tokens onlyOwner
    // - [x] withdrawERC1155Tokens onlyOwner
    // - [x] withdrawERC721Tokens onlyOwner
    // - [ ] claim (transfer with signature) nonReentrant
    // - [ ] claimMessageHash public view
    // - [x] onERC1155BatchReceived nonReentrant (implemented by ERC1155Holder)
    // - [x] claimStatus view method
    // - [x] setSignerForClaim onlyOwner
    // - [x] getSignerForClaim public view
    // - [x] createClaim onlyOwner
    // - [x] numClaims public view
    // - [x] setClaimStatus onlyOwner
    // - [x] getClaim external view

    // Claim data structure:
    // (claimId, playerAddress) -> true/false

    // Signer data structure
    // token address -> signer address

    uint256 public ERC20_TYPE = 20;
    uint256 public ERC721_TYPE = 721;
    uint256 public ERC1155_TYPE = 1155;

    struct ClaimableToken {
        uint256 tokenType;
        address tokenAddress; // address of the token
        uint256 tokenId;
        uint256 amount;
    }

    uint256 private NumClaims;
    mapping(uint256 => bool) IsClaimActive;
    mapping(uint256 => address) ClaimSigner;
    mapping(uint256 => ClaimableToken) ClaimToken;
    mapping(uint256 => mapping(address => bool)) ClaimCompleted;

    event Claimed(uint256 indexed claimId, address indexed claimant);
    event ClaimCreated(
        uint256 claimId,
        uint256 indexed tokenType,
        address indexed tokenAddress,
        uint256 indexed tokenId,
        uint256 amount
    );
    event ClaimStatusChanged(uint256 indexed claimId, bool status);
    event ClaimSignerChanged(uint256 indexed claimId, address signer);
    event Withdrawal(
        address recipient,
        uint256 indexed tokenType,
        address indexed tokenAddress,
        uint256 indexed tokenId,
        uint256 amount
    );

    constructor() EIP712("Moonstream Dropper", "0.0.1") {}

    function onERC721Received(
        address operator,
        address from,
        uint256 tokenId,
        bytes calldata data
    ) external returns (bytes4) {
        return IERC721Receiver.onERC721Received.selector;
    }

    function createClaim(
        uint256 tokenType,
        address tokenAddress,
        uint256 tokenId,
        uint256 amount
    ) external onlyOwner returns (uint256) {
        require(
            tokenType == ERC20_TYPE ||
                tokenType == ERC721_TYPE ||
                tokenType == ERC1155_TYPE,
            "Dropper: createClaim -- Unknown token type"
        );
        NumClaims++;

        ClaimableToken memory tokenMetadata;
        tokenMetadata.tokenType = tokenType;
        tokenMetadata.tokenAddress = tokenAddress;
        tokenMetadata.tokenId = tokenId;
        tokenMetadata.amount = amount;
        ClaimToken[NumClaims] = tokenMetadata;
        emit ClaimCreated(NumClaims, tokenType, tokenAddress, tokenId, amount);

        IsClaimActive[NumClaims] = true;
        emit ClaimStatusChanged(NumClaims, true);

        return NumClaims;
    }

    function numClaims() external view returns (uint256) {
        return NumClaims;
    }

    function getClaim(uint256 claimId)
        external
        view
        returns (ClaimableToken memory)
    {
        return ClaimToken[claimId];
    }

    function setClaimStatus(uint256 claimId, bool status) external onlyOwner {
        IsClaimActive[claimId] = status;
        emit ClaimStatusChanged(claimId, status);
    }

    function claimStatus(uint256 claimId) external view returns (bool) {
        return IsClaimActive[claimId];
    }

    function setSignerForClaim(uint256 claimId, address signer)
        external
        onlyOwner
    {
        ClaimSigner[claimId] = signer;
        emit ClaimSignerChanged(claimId, signer);
    }

    function getSignerForClaim(uint256 claimId)
        external
        view
        returns (address)
    {
        return ClaimSigner[claimId];
    }

    function claimMessageHash(
        uint256 claimId,
        address claimant,
        uint256 blockDeadline
    ) public view returns (bytes32) {
        bytes32 structHash = keccak256(
            abi.encode(
                keccak256(
                    "ClaimPayload(uint256 claimId,address claimant,uint256 blockDeadline)"
                ),
                claimId,
                claimant,
                blockDeadline
            )
        );
        bytes32 digest = _hashTypedDataV4(structHash);
        return digest;
    }

    function claim(
        uint256 claimId,
        uint256 blockDeadline,
        bytes memory signature
    ) external whenNotPaused nonReentrant {
        require(
            block.number <= blockDeadline,
            "Dropper: claim -- Block deadline exceeded."
        );
        require(
            !ClaimCompleted[claimId][msg.sender],
            "Dropper: claim -- That claim has already been completed."
        );
        bytes32 hash = claimMessageHash(claimId, msg.sender, blockDeadline);
        require(
            SignatureChecker.isValidSignatureNow(
                ClaimSigner[claimId],
                hash,
                signature
            ),
            "Dropper: claim -- Invalid signer for claim."
        );

        ClaimableToken memory claimToken = ClaimToken[claimId];
        if (claimToken.tokenType == ERC20_TYPE) {
            IERC20 erc20Contract = IERC20(claimToken.tokenAddress);
            erc20Contract.transfer(msg.sender, claimToken.amount);
        } else if (claimToken.tokenType == ERC721_TYPE) {
            IERC721 erc721Contract = IERC721(claimToken.tokenAddress);
            erc721Contract.safeTransferFrom(
                address(this),
                msg.sender,
                claimToken.tokenId,
                ""
            );
        } else if (claimToken.tokenType == ERC1155_TYPE) {
            IERC1155 erc1155Contract = IERC1155(claimToken.tokenAddress);
            erc1155Contract.safeTransferFrom(
                address(this),
                msg.sender,
                claimToken.tokenId,
                claimToken.amount,
                ""
            );
        } else {
            revert("Dropper -- claim: Unknown token type in claim");
        }

        ClaimCompleted[claimId][msg.sender] = true;

        emit Claimed(claimId, msg.sender);
    }

    function withdrawERC20(address tokenAddress, uint256 amount)
        public
        onlyOwner
    {
        IERC20 erc20Contract = IERC20(tokenAddress);
        erc20Contract.transfer(_msgSender(), amount);
        emit Withdrawal(msg.sender, ERC20_TYPE, tokenAddress, 0, amount);
    }

    function withdrawERC721(address tokenAddress, uint256 tokenId)
        public
        onlyOwner
    {
        address _owner = owner();
        IERC721 erc721Contract = IERC721(tokenAddress);
        erc721Contract.safeTransferFrom(address(this), _owner, tokenId, "");
        emit Withdrawal(msg.sender, ERC721_TYPE, tokenAddress, tokenId, 1);
    }

    function withdrawERC1155(
        address tokenAddress,
        uint256 tokenId,
        uint256 amount
    ) public onlyOwner {
        address _owner = owner();
        IERC1155 erc1155Contract = IERC1155(tokenAddress);
        erc1155Contract.safeTransferFrom(
            address(this),
            _owner,
            tokenId,
            amount,
            ""
        );
        emit Withdrawal(
            msg.sender,
            ERC1155_TYPE,
            tokenAddress,
            tokenId,
            amount
        );
    }
}
