# Decentralized Identity (DID) DApp

A decentralized application for **managing DIDs (Decentralized Identifiers)** with features such as registration, update, and revocation.  
The project integrates **smart contracts, backend APIs, and a React-based frontend dashboard**.

---

## 🚀 Project Structure
app/
├── backend/ # Python backend (Flask/FastAPI)
│ ├── server.py
│ ├── requirements.txt
│ └── contracts/
├── contracts/ # Solidity smart contracts
│ ├── DIDRegistry.sol
│ └── SemaphoreVerifier.sol
├── dashboard/ # React-based dashboard
│ ├── src/App.jsx
│ └── package.json
├── frontend/ # Frontend app
│ ├── contractConfig.js
│ └── package.json
├── docker-compose.yml # Containerized setup
├── hardhat.config.cjs # Hardhat config for Ethereum contracts
└── package.json

---

## ⚙️ Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>/app

Install Dependencies:
Backend (Python)
cd backend
pip install -r requirements.txt


Smart Contracts (Hardhat):
cd ..
npm install
npx hardhat compile

Frontend:
cd frontend
npm install
npm start

Dashboard:
cd dashboard
npm install
npm run dev

Running the Project

Backend:
cd backend
python server.py

Contracts:
npx hardhat node
npx hardhat run scripts/deploy.js --network localhost

Frontend:
cd frontend
npm start

Dashboard:
cd dashboard
npm run dev

Features

DID registration, update, and revocation

Smart contract interaction using Hardhat

Python backend for API and storage

React-based dashboard for visualization

Containerized setup with Docker





