const { ethers } = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contract with account:", deployer.address);

  // ⬇️ Replace "DIDRegistry" with your actual contract name if different
  const ContractFactory = await ethers.getContractFactory("DIDRegistry");
  const contract = await ContractFactory.deploy();

  // Wait for deployment (ethers v6 style)
  await contract.waitForDeployment();

  console.log("✅ Contract deployed to:", await contract.getAddress());
}

main().catch((error) => {
  console.error("❌ Deployment failed:", error);
  process.exitCode = 1;
});
