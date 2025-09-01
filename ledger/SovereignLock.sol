// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// SovereignLock — minimal anchoring stub (alpha).
// Do NOT deploy as-is in production.

contract SovereignLock {
    event ActionCommitted(address indexed actor, bytes32 indexed actionHash, string kind, string metadataURI, uint256 blockTs);

    mapping(bytes32 => bool) public committed;

    function commit(bytes32 actionHash, string calldata kind, string calldata metadataURI) external {
        require(!committed[actionHash], "Already committed");
        committed[actionHash] = true;
        emit ActionCommitted(msg.sender, actionHash, kind, metadataURI, block.timestamp);
    }

    function isCommitted(bytes32 actionHash) external view returns (bool) {
        return committed[actionHash];
    }
}
