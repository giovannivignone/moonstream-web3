// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.9;

// Interface generated by solface: https://github.com/moonstream-to/solface
// solface version: 0.1.0
// Interface ID: f472ee2f
interface ICrafting {
    // structs
    struct Compound0 {
        uint256 tokenType;
        address tokenAddress;
        uint256 tokenId;
        uint256 amount;
        uint256 tokenAction;
    }
    struct Compound1 {
        uint256 tokenType;
        address tokenAddress;
        uint256 tokenId;
        uint256 amount;
        uint256 tokenAction;
    }
    struct Compound2 {
        Compound0[] inputs;
        Compound1[] outputs;
        bool isActive;
    }
    struct Compound3 {
        uint256 tokenType;
        address tokenAddress;
        uint256 tokenId;
        uint256 amount;
        uint256 tokenAction;
    }
    struct Compound4 {
        uint256 tokenType;
        address tokenAddress;
        uint256 tokenId;
        uint256 amount;
        uint256 tokenAction;
    }
    struct Compound5 {
        Compound3[] inputs;
        Compound4[] outputs;
        bool isActive;
    }
    struct Compound6 {
        uint256 tokenType;
        address tokenAddress;
        uint256 tokenId;
        uint256 amount;
        uint256 tokenAction;
    }
    struct Compound7 {
        uint256 tokenType;
        address tokenAddress;
        uint256 tokenId;
        uint256 amount;
        uint256 tokenAction;
    }
    struct Compound8 {
        Compound6[] inputs;
        Compound7[] outputs;
        bool isActive;
    }
    struct Compound9 {
        uint256 tokenType;
        address tokenAddress;
        uint256 tokenId;
        uint256 amount;
        uint256 tokenAction;
    }
    struct Compound10 {
        uint256 tokenType;
        address tokenAddress;
        uint256 tokenId;
        uint256 amount;
        uint256 tokenAction;
    }
    struct Compound11 {
        Compound9[] inputs;
        Compound10[] outputs;
        bool isActive;
    }
    struct Compound12 {
        uint256 tokenType;
        address tokenAddress;
        uint256 tokenId;
        uint256 amount;
        uint256 tokenAction;
    }
    struct Compound13 {
        uint256 tokenType;
        address tokenAddress;
        uint256 tokenId;
        uint256 amount;
        uint256 tokenAction;
    }
    struct Compound14 {
        Compound12[] inputs;
        Compound13[] outputs;
        bool isActive;
    }

    // events
    event Craft(uint256 recipeId, address player);
    event RecipeCreated(uint256 recipeId, Compound2 recipe, address operator);
    event RecipeUpdated(uint256 recipeId, Compound5 recipe, address operator);

    // functions
    // Selector: a1141e04
    function addRecipe(Compound8 memory recipe) external;

    // Selector: f3917bd2
    function craft(uint256 recipeId) external;

    // Selector: f8d12a41
    function getRecipe(
        uint256 recipeId
    ) external view returns (Compound11 memory);

    // Selector: 953633b9
    function numRecipes() external view returns (uint256);

    // Selector: bc197c81
    function onERC1155BatchReceived(
        address,
        address,
        uint256[] memory,
        uint256[] memory,
        bytes memory
    ) external returns (bytes4);

    // Selector: f23a6e61
    function onERC1155Received(
        address,
        address,
        uint256,
        uint256,
        bytes memory
    ) external returns (bytes4);

    // Selector: 150b7a02
    function onERC721Received(
        address,
        address,
        uint256,
        bytes memory
    ) external returns (bytes4);

    // Selector: e74738d9
    function setTerminusAuth(address terminusAddress, uint256 tokenId) external;

    // Selector: 01ffc9a7
    function supportsInterface(bytes4 interfaceId) external view returns (bool);

    // Selector: 76800b9d
    function updateRecipe(uint256 recipeId, Compound14 memory recipe) external;

    // errors
}
