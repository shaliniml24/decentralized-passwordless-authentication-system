<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Decentralized Passwordless Authentication System — README</title>
  <style>
    :root{
      --bg:#0b1020;
      --card:#121833;
      --muted:#9fb0ff;
      --text:#e9ecff;
      --accent:#6ea8fe;
      --ok:#33d1a0;
      --warn:#f0b429;
      --err:#ff6b6b;
      --border:rgba(255,255,255,.08);
    }
    *{box-sizing:border-box}
    body{
      margin:0;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", "Apple Color Emoji", "Segoe UI Emoji";
      background:linear-gradient(180deg, #0b1020, #0a0e1b);
      color:var(--text);
      line-height:1.6;
    }
    .wrap{max-width:1000px;margin:40px auto;padding:0 20px;}
    .title{
      display:flex;align-items:center;gap:12px;margin-bottom:16px;
    }
    .logo{
      width:40px;height:40px;border-radius:12px;background:linear-gradient(135deg,#6ea8fe,#33d1a0);
      box-shadow:0 10px 30px rgba(102,153,255,.35), inset 0 0 10px rgba(255,255,255,.2);
    }
    h1{font-size:38px;margin:0}
    .badge-row{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 22px}
    .badge{
      display:inline-flex;align-items:center;gap:8px;
      border:1px solid var(--border);
      background:rgba(255,255,255,.03);
      padding:6px 10px;border-radius:999px;font-size:12px;color:var(--muted)
    }
    .grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
    .card{
      background:linear-gradient(180deg, rgba(255,255,255,.02), rgba(255,255,255,.01));
      border:1px solid var(--border);
      border-radius:16px;padding:18px 18px 14px;
      box-shadow:0 10px 30px rgba(0,0,0,.25);
    }
    h2{margin:24px 0 10px;font-size:24px}
    h3{margin:18px 0 8px;font-size:18px;color:var(--muted)}
    ul{margin:8px 0 16px 20px}
    code, pre{
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
      background:#0b122a;
      border:1px solid var(--border);
      color:#cfe3ff;
      border-radius:10px;
    }
    code{padding:2px 6px}
    pre{padding:14px 16px;overflow:auto}
    .kbd{border:1px solid var(--border);padding:2px 6px;border-radius:6px;background:rgba(255,255,255,.05)}
    a{color:var(--accent);text-decoration:none}
    a:hover{text-decoration:underline}
    table{width:100%;border-collapse:collapse;margin:10px 0 18px}
    th, td{border:1px solid var(--border);padding:10px;text-align:left}
    th{background:rgba(255,255,255,.04)}
    .pill{
      display:inline-block;padding:3px 10px;border-radius:999px;
      border:1px solid var(--border);font-size:12px;color:var(--muted)
    }
    .callout{border-left:4px solid var(--accent);padding:10px 12px;background:rgba(110,168,254,.08);border-radius:8px;margin:12px 0}
    .ok{color:var(--ok)} .warn{color:var(--warn)} .err{color:var(--err)}
    footer{opacity:.75;margin-top:24px;font-size:13px}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="title">
      <div class="logo" aria-hidden="true"></div>
      <h1>Decentralized Passwordless Authentication System</h1>
    </div>

    <div class="badge-row">
      <span class="badge">Solidity</span>
      <span class="badge">Hardhat</span>
      <span class="badge">Node/Express</span>
      <span class="badge">React</span>
      <span class="badge">MongoDB</span>
      <span class="badge">Ethers/Web3</span>
      <span class="badge">Zero-Knowledge (ZK) Ready</span>
    </div>

    <div class="card">
      <h2>Overview</h2>
      <p>This project implements a <strong>passwordless login</strong> flow powered by <strong>Decentralized Identifiers (DIDs)</strong> and on-chain <strong>DID Registry</strong> smart contracts. Users authenticate via signed challenges; the backend verifies signatures and (optionally) anchors state on-chain. A companion database (MongoDB) stores off-chain metadata (profiles, sessions, audit logs) without ever storing passwords.</p>
      <div class="callout">
        <strong>Goal:</strong> Secure, user-centric identity with cryptographic proofs instead of passwords, designed to integrate with modern dApps and web backends.
      </div>
    </div>

    <div class="grid">
      <div class="card">
        <h3>Key Features</h3>
        <ul>
          <li>Passwordless login using wallet signatures (<code>eth_personalSign</code> / <code>siwe</code>-style).</li>
          <li>DID registration, update, revoke via smart contract (e.g., <code>DIDRegistry</code>).</li>
          <li>Anchor document hash / status on-chain for verifiability.</li>
          <li>MongoDB persistence for user profile &amp; session management.</li>
          <li>Clean separation: Contracts • Backend API • Frontend UI.</li>
          <li>Docker-ready for local development.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Tech Stack</h3>
        <ul>
          <li><strong>Smart Contracts:</strong> Solidity, Hardhat, Ethers</li>
          <li><strong>Backend:</strong> Node.js / Express (or Python FastAPI variant), Ethers, MongoDB Driver/Mongoose</li>
          <li><strong>Frontend:</strong> React / Vite (or CRA), Web3Modal / Wagmi (optional)</li>
          <li><strong>Infra:</strong> Alchemy/Infura RPC, Docker, dotenv</li>
        </ul>
      </div>
    </div>

    <div class="card">
      <h2>Architecture</h2>
      <ul>
        <li><span class="pill">Client</span>: Connect wallet → request nonce → sign message → send to API.</li>
        <li><span class="pill">API</span>: Verify signature → issue session/JWT → (optional) write DID anchor on-chain.</li>
        <li><span class="pill">Contract</span>: <code>DIDRegistry</code> stores owner, document URI, status hash, and events.</li>
        <li><span class="pill">DB</span>: MongoDB stores users, DIDs, nonces, sessions, audit events.</li>
      </ul>
      <pre><code>
[ Wallet ] --sign--> [ API ] --verify--> [ Session ]
    |                                 |
    |                                     (optional)
    v                                 v
 [ UI ] &lt;--profile--  [ MongoDB ]   [ Ethereum / Testnet ]
      </code></pre>
    </div>

    <div class="grid">
      <div class="card">
        <h3>Prerequisites</h3>
        <ul>
          <li>Node.js 18+</li>
          <li>Git &amp; Docker (optional)</li>
          <li>MongoDB (local or Atlas)</li>
          <li>Alchemy/Infura RPC URL for your network (e.g., Sepolia)</li>
        </ul>
      </div>
      <div class="card">
        <h3>Environment Variables</h3>
        <table>
          <thead><tr><th>Variable</th><th>Description</th></tr></thead>
          <tbody>
            <tr><td><code>RPC_URL</code></td><td>Ethereum RPC endpoint (Alchemy/Infura)</td></tr>
            <tr><td><code>PRIVATE_KEY</code></td><td>Deployer account private key (for Hardhat/Backend signer)</td></tr>
            <tr><td><code>MONGO_URI</code></td><td>MongoDB connection string</td></tr>
            <tr><td><code>JWT_SECRET</code></td><td>Secret for signing API sessions/JWTs</td></tr>
            <tr><td><code>DID_REGISTRY_ADDRESS</code></td><td>Deployed contract address</td></tr>
            <tr><td><code>CHAIN_ID</code></td><td>Target chain id (e.g., 11155111 for Sepolia)</td></tr>
          </tbody>
        </table>
        <pre><code># .env (example)
RPC_URL=https://eth-sepolia.g.alchemy.com/v2/your-key
PRIVATE_KEY=0xabc...def
MONGO_URI=mongodb://localhost:27017/did_auth
JWT_SECRET=supersecret
DID_REGISTRY_ADDRESS=0xYourDeployedContract
CHAIN_ID=11155111
</code></pre>
      </div>
    </div>

    <div class="card">
      <h2>Getting Started</h2>
      <h3>1) Install &amp; Build</h3>
      <pre><code># clone your repo
git clone https://github.com/shaliniml24/decentralized-passwordless-authentication-system.git
cd decentralized-passwordless-authentication-system

# install
npm install  # (or pnpm i / yarn)
</code></pre>

      <h3>2) Contracts (Hardhat)</h3>
      <pre><code># compile
npx hardhat compile

# test
npx hardhat test

# deploy (network in hardhat.config)
npx hardhat run scripts/deploy.js --network sepolia
</code></pre>

      <h3>3) Backend</h3>
      <pre><code># from /backend
cp .env.example .env
npm install
npm run dev

# endpoints (typical)
POST /api/auth/nonce        # issue nonce for address
POST /api/auth/verify       # verify signature, mint session
POST /api/did/register      # writes DID &amp; optional on-chain anchor
GET  /api/did/:did          # resolve
</code></pre>

      <h3>4) Frontend</h3>
      <pre><code># from /frontend
cp .env.example .env
npm install
npm run dev
</code></pre>

      <h3>5) Docker (Optional)</h3>
      <pre><code># run db + api + web
docker compose up -d

# view logs
docker compose logs -f
</code></pre>
    </div>

    <div class="grid">
      <div class="card">
        <h3>MongoDB Models (Example)</h3>
        <pre><code>users: { _id, address, did, createdAt, updatedAt }
nonces: { address, nonce, expiresAt }
sessions: { userId, jwtId, issuedAt, expiresAt }
audits: { actor, action, meta, at }
</code></pre>
      </div>
      <div class="card">
        <h3>Contract Interface (Example)</h3>
        <pre><code>function register(bytes32 did, string uri, bytes32 statusHash) external;
function update(bytes32 did, string uri, bytes32 statusHash) external;
function revoke(bytes32 did) external;
function ownerOf(bytes32 did) view returns (address);
event DIDRegistered(bytes32 indexed did, address owner);
</code></pre>
      </div>
    </div>

    <div class="card">
      <h2>Troubleshooting</h2>
      <ul>
        <li><strong>Rejected push (non-fast-forward)</strong> — Run <code>git pull --rebase origin main</code> first, or use <code>git push --force</code> if you intend to overwrite.</li>
        <li><strong>“cannot pull with rebase: index contains uncommitted changes”</strong> — <code>git add . &amp;&amp; git commit -m "wip"</code> or <code>git stash</code> before pulling.</li>
        <li><strong>Hardhat: "require is not defined in ES module"</strong> — remove <code>"type":"module"</code> or switch to <code>import</code> syntax consistently.</li>
        <li><strong>FileNotFoundError for <code>DIDRegistry.json</code></strong> — make sure the path matches your compiled artifacts (e.g., <code>artifacts/contracts/DIDRegistry.json</code>) or copy ABI to <code>backend/contracts/</code>.</li>
        <li><strong>MongoDB connection errors</strong> — verify <code>MONGO_URI</code>, network access (Atlas IP allowlist), and service is running.</li>
      </ul>
    </div>

    <div class="grid">
      <div class="card">
        <h3>Common Git Commands</h3>
        <pre><code># initial push
git branch -M main
git remote add origin &lt;repo-url&gt;
git push -u origin main

# sync
git add .
git commit -m "feat: ..."
git pull --rebase origin main
git push origin main
</code></pre>
      </div>
      <div class="card">
        <h3>Security Notes</h3>
        <ul>
          <li>Never commit private keys. Use <code>.env</code> + <code>.gitignore</code>.</li>
          <li>Use per-session nonces and short-lived tokens.</li>
          <li>Validate chainId and domain in the signed message.</li>
          <li>Emit/consume contract events for auditability.</li>
        </ul>
      </div>
    </div>

    <div class="grid">
      <div class="card">
        <h3>Roadmap Ideas</h3>
        <ul>
          <li>SIWE (Sign-In with Ethereum) compliant flow.</li>
          <li>Verifiable Credentials issuance &amp; selective disclosure (ZK).</li>
          <li>Social recovery / multisig for DID control.</li>
          <li>ENS reverse resolution for nicer UX.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Contributing</h3>
        <p>PRs welcome! Please open an issue for major changes. Run tests and linters before submitting.</p>
        <h3>License</h3>
        <p>MIT © 2025 Shalini M L</p>
      </div>
    </div>

    <footer>
      <p>Made with ♥ for decentralized identity. Have questions? Open an issue in the repo.</p>
    </footer>
  </div>
</body>
</html>
