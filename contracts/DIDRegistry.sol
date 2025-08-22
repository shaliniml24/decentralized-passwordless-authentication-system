// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract DIDRegistry {
    event DIDRegistered(address indexed owner, string did);
    event DIDDocumentUpdated(string indexed did, string docURI);
    event StatusHashAnchored(string indexed did, bytes32 statusHash);
    event DIDRevoked(string indexed did);

    mapping(string => address) public didOwner;
    mapping(string => string) public didDocumentURI;
    mapping(string => bytes32) public latestStatusHash;

    modifier onlyOwner(string memory did) {
        require(didOwner[did] == msg.sender, "Not DID owner");
        _;
    }

    function registerDID(string calldata did, string calldata docURI) external {
        require(didOwner[did] == address(0), "DID taken");
        didOwner[did] = msg.sender;
        didDocumentURI[did] = docURI;
        emit DIDRegistered(msg.sender, did);
        emit DIDDocumentUpdated(did, docURI);
    }

    function updateDIDDocument(string calldata did, string calldata docURI)
        external
        onlyOwner(did)
    {
        didDocumentURI[did] = docURI;
        emit DIDDocumentUpdated(did, docURI);
    }

    function anchorStatusHash(string calldata did, bytes32 statusHash)
        external
        onlyOwner(did)
    {
        latestStatusHash[did] = statusHash;
        emit StatusHashAnchored(did, statusHash);
    }

    function revokeDID(string calldata did)
        external
        onlyOwner(did)
    {
        // Clear all state for this DID
        delete didOwner[did];
        delete didDocumentURI[did];
        delete latestStatusHash[did];
        emit DIDRevoked(did);
    }
}
