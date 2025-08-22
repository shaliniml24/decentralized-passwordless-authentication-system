const { ethers } = require("hardhat");

async function main() {
  const contractAddress = "0x5F4ED6390505A36410C8390516e3B533edD7BEF8"; // replace with Sepolia address
  const DIDRegistry = await ethers.getContractFactory("DIDRegistry");
  const contract = DIDRegistry.attach(contractAddress);

  // Call registerDID
  const tx = await contract.registerDID("did:example:123", "https://example.com/did.json");
  await tx.wait();
  console.log("✅ DID Registered");

  // Call updateDIDDocument
  const tx2 = await contract.updateDIDDocument("did:example:123", "https://new-doc.com");
  await tx2.wait();
  console.log("✅ DID Updated");

  // Call anchorStatusHash
  const hash = ethers.keccak256(ethers.toUtf8Bytes("status-data"));
  const tx3 = await contract.anchorStatusHash("did:example:123", hash);
  await tx3.wait();
  console.log("✅ Status Hash Anchored");

  // Call revokeDID
await contract.revokeDID("did:example:123"); 
console.log("✅ DID Revoked");

}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
