"""Configuration for Solana Narrative Radar"""

# Solana KOLs to track
SOLANA_KOLS = [
    {"handle": "0xMert_", "name": "Mert Mumtaz", "org": "Helius"},
    {"handle": "aeyakovenko", "name": "Anatoly Yakovenko", "org": "Solana Labs"},
    {"handle": "akshaybd", "name": "Akshay BD", "org": "Superteam"},
    {"handle": "rajgokal", "name": "Raj Gokal", "org": "Solana Labs"},
    {"handle": "armaboreh", "name": "Armani Boreh", "org": "Solana Foundation"},
]

# GitHub topics to track
GITHUB_TOPICS = [
    "solana",
    "anchor-lang",
    "solana-program",
    "solana-sdk",
    "spl-token",
]

# Narrative categories with keywords
NARRATIVE_KEYWORDS = {
    "ai_agents": [
        "ai agent", "autonomous", "ai16z", "eliza", "solana agent kit",
        "sendai", "trading bot", "llm", "gpt", "claude", "autonomous trading",
        "swarm", "marc aindreessen", "agent", "agentic"
    ],
    "infrastructure": [
        "firedancer", "alpenglow", "tps", "latency", "finality",
        "validator", "jump crypto", "consensus", "throughput", "1m tps",
        "150ms", "upgrade", "block space", "compute unit"
    ],
    "stablecoins_payfi": [
        "usdc", "usdt", "stablecoin", "payment", "payfi", "micropayment",
        "western union", "visa", "mastercard", "remittance", "cross-border",
        "settlement", "usdpt", "circle"
    ],
    "rwa_tokenization": [
        "rwa", "real world asset", "tokenized", "tokenization", "ondo",
        "wisdomtree", "stocks", "bonds", "etf", "securities", "equities",
        "treasury", "commodity", "multiliquid"
    ],
    "mobile_consumer": [
        "seeker", "saga", "mobile", "skr", "dapp store", "seed vault",
        "consumer", "wallet", "phone", "android", "hardware"
    ],
    "depin": [
        "depin", "helium", "render", "hivemapper", "io.net", "nosana",
        "physical infrastructure", "gpu", "wireless", "bandwidth",
        "dawn network", "compute"
    ],
    "memecoins": [
        "pump.fun", "memecoin", "meme coin", "bonk", "wif", "dogwifhat",
        "launchpad", "bonding curve", "pengu", "pump", "degen"
    ],
    "defi_evolution": [
        "jupiter", "raydium", "marinade", "jito", "kamino", "drift",
        "perp", "perpetual", "amm", "lending", "borrowing", "yield",
        "liquid staking", "restaking"
    ],
    "zk_compression": [
        "zk compression", "state compression", "light protocol",
        "compressed nft", "cnft", "merkle tree", "storage"
    ]
}

# Data sources
DATA_SOURCES = {
    "github": "https://api.github.com",
    "helius_blog": "https://www.helius.dev/blog",
    "messari": "https://messari.io/research",
}

# Output settings
OUTPUT_DIR = "/home/clawdbot/clawd/builds/solana-narrative-radar/output"
REPORT_FILE = "narrative_report"
