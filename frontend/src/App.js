import React, { useState } from "react";
import { ethers } from "ethers";
import "./App.css";
import { contractAddress, contractABI } from "./contractConfig";

async function getContract() {
  if (!window.ethereum) {
    alert("Please install MetaMask!");
    return null;
  }

  const provider = new ethers.BrowserProvider(window.ethereum);
  const signer = await provider.getSigner();
  return new ethers.Contract(contractAddress, contractABI, signer);
}

function App() {
  const [did, setDid] = useState("");
  const [docURI, setDocURI] = useState("");
  const [statusHash, setStatusHash] = useState("");

  // ✅ Register DID
  async function registerDID() {
    const contract = await getContract();
    if (!contract) return;
    try {
      const tx = await contract.registerDID(did, docURI);
      await tx.wait();
      alert(`✅ DID Registered: ${did}`);
    } catch (error) {
      console.error(error);
      alert("❌ Error registering DID");
    }
  }

  // ✅ Update DID Document
  async function updateDID() {
    const contract = await getContract();
    if (!contract) return;
    try {
      const tx = await contract.updateDIDDocument(did, docURI);
      await tx.wait();
      alert(`✅ DID Updated: ${did}`);
    } catch (error) {
      console.error(error);
      alert("❌ Error updating DID");
    }
  }

  // ✅ Anchor Status Hash
  async function anchorStatus() {
    const contract = await getContract();
    if (!contract) return;
    try {
      const hash = ethers.keccak256(ethers.toUtf8Bytes(statusHash));
      const tx = await contract.anchorStatusHash(did, hash);
      await tx.wait();
      alert(`✅ Status Anchored for DID: ${did}`);
    } catch (error) {
      console.error(error);
      alert("❌ Error anchoring status hash");
    }
  }

  // ✅ Revoke DID
  async function revokeDID() {
    const contract = await getContract();
    if (!contract) return;
    try {
      const tx = await contract.revokeDID(did);
      await tx.wait();
      alert(`❌ DID Revoked: ${did}`);
    } catch (error) {
      console.error(error);
      alert("❌ Error revoking DID");
    }
  }

  return (
    <div style={{ padding: "20px" }}>
      <h2>🆔 DID Registry</h2>

      <input
        type="text"
        placeholder="Enter DID (e.g., did:example:123)"
        value={did}
        onChange={(e) => setDid(e.target.value)}
      />
      <br /><br />

      <input
        type="text"
        placeholder="Enter Document URI"
        value={docURI}
        onChange={(e) => setDocURI(e.target.value)}
      />
      <br /><br />

      <input
        type="text"
        placeholder="Enter Status Data"
        value={statusHash}
        onChange={(e) => setStatusHash(e.target.value)}
      />
      <br /><br />

      <button onClick={registerDID}>Register DID</button>
      <button onClick={updateDID}>Update DID</button>
      <button onClick={anchorStatus}>Anchor Status Hash</button>
      <button onClick={revokeDID}>Revoke DID</button>
    </div>
  );
}

export default App;
