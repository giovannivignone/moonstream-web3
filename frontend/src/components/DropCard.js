import React, { useContext } from "react";
import {
  chakra,
  Flex,
  Text,
  Stack,
  Heading,
  Spinner,
  Button,
} from "@chakra-ui/react";
import useDropperClaim from "../core/hooks/useDropperClaim";
import Web3Context from "../core/providers/Web3Provider/context";
import { targetChain } from "../core/providers/Web3Provider";
import Erc20Card from "./Erc20Card";

const DropCard = ({ drop }) => {
  const web3Provider = useContext(Web3Context);

  const claimer = useDropperClaim({
    dropperAddress: process.env.NEXT_PUBLIC_DROPPER_ADDRESS ?? "",
    targetChain: targetChain,
    ctx: web3Provider,
    claimId: drop.id,
  });

  const handleClick = () => {
    console.log("handleClick");
    claimer.claim(drop.id);
  };

  let shouldDisable = false;

  if (
    claimer.claimStatus?.data &&
    (claimer.claimStatus?.data.status > 0 ||
      claimer.claimStatus?.data.claim[0] == "0")
  )
    shouldDisable = true;

  return (
    <Flex
      bgColor="blue.600"
      borderRadius="md"
      px={4}
      py={2}
      flexGrow={1}
      alignContent="baseline"
      justifyContent={"space-between"}
      alignItems="baseline"
    >
      <Text fontWeight={600} textColor="gray.100" h="min-content">
        {drop.entry.title}
      </Text>
      {claimer.claimStatus.data &&
        claimer.claimStatus.data.claim[0] == "20" && (
          <Erc20Card
            address={claimer.claimStatus.data.claim[1]}
            amount={web3Provider.web3.utils.fromWei(
              claimer.claimStatus.data.claim[3]
            )}
          />
        )}
      <Button
        isDisabled={shouldDisable}
        onClick={handleClick}
        isLoading={claimer.claimWeb3Drop.isLoading}
        colorScheme={"orange"}
      >
        Claim
      </Button>
    </Flex>
  );
};

export default DropCard;
