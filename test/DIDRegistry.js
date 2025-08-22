import { expect } from "chai";
import pkg from "hardhat";
const { ethers } = pkg;

describe("DIDRegistry", function () {
  let registry, owner, other, DIDRegistry;

  beforeEach(async function () {
    [owner, other] = await ethers.getSigners();
    DIDRegistry = await ethers.getContractFactory("DIDRegistry");
    registry = await DIDRegistry.deploy();
    await registry.waitForDeployment();
  });

  it("should register a DID and emit events", async function () {
    const did = "did:example:123";
    const doc = "ipfs://doc1";

    await expect(registry.registerDID(did, doc))
      .to.emit(registry, "DIDRegistered").withArgs(owner.address, did)
      .and.to.emit(registry, "DIDDocumentUpdated").withArgs(did, doc);

    expect(await registry.didOwner(did)).to.equal(owner.address);
    expect(await registry.didDocumentURI(did)).to.equal(doc);
  });

  it("should prevent duplicate registrations", async function () {
    const did = "did:example:dup";
    await registry.registerDID(did, "doc1");
    await expect(registry.registerDID(did, "doc2"))
      .to.be.revertedWith("DID taken");
  });

  it("should allow only the owner to update the DID document", async function () {
    const did = "did:example:update";
    await registry.registerDID(did, "doc1");

    await expect(registry.connect(other).updateDIDDocument(did, "hax"))
      .to.be.revertedWith("Not DID owner");

    await expect(registry.updateDIDDocument(did, "ipfs://updated"))
      .to.emit(registry, "DIDDocumentUpdated").withArgs(did, "ipfs://updated");

    expect(await registry.didDocumentURI(did)).to.equal("ipfs://updated");
  });

  it("should anchor a status hash (only owner)", async function () {
    const did = "did:example:status";
    await registry.registerDID(did, "doc");

    const hash = ethers.keccak256(ethers.toUtf8Bytes("revocation-list-1"));
    await expect(registry.connect(other).anchorStatusHash(did, hash))
      .to.be.revertedWith("Not DID owner");

    await expect(registry.anchorStatusHash(did, hash))
      .to.emit(registry, "StatusHashAnchored").withArgs(did, hash);

    expect(await registry.latestStatusHash(did)).to.equal(hash);
  });

  it("should revoke a DID and clear state; allows re-registration", async function () {
    const did = "did:example:revoke";
    await registry.registerDID(did, "docX");

    await expect(registry.connect(other).revokeDID(did))
      .to.be.revertedWith("Not DID owner");

    await expect(registry.revokeDID(did))
      .to.emit(registry, "DIDRevoked").withArgs(did);

    // All state cleared
    expect(await registry.didOwner(did)).to.equal(ethers.ZeroAddress);
    expect(await registry.didDocumentURI(did)).to.equal("");
    expect(await registry.latestStatusHash(did)).to.equal(ethers.ZeroHash);

    // Can register again (fresh)
    await registry.connect(other).registerDID(did, "docY");
    expect(await registry.didOwner(did)).to.equal(other.address);
    expect(await registry.didDocumentURI(did)).to.equal("docY");
  });
});
