"""Helius API Fetcher - Real on-chain signal data from Solana"""

import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import os

# Load API key from environment or .env file
HELIUS_API_KEY = os.environ.get("HELIUS_API_KEY", "")


class HeliusFetcher:
    """Fetches real on-chain data from Helius API for narrative signals"""
    
    BASE_URL = "https://api.helius.xyz/v0"
    RPC_URL = "https://mainnet.helius-rpc.com"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or HELIUS_API_KEY
        if not self.api_key:
            # Try loading from .env file
            env_path = os.path.join(os.path.dirname(__file__), ".env")
            if os.path.exists(env_path):
                with open(env_path) as f:
                    for line in f:
                        if line.startswith("HELIUS_API_KEY="):
                            self.api_key = line.strip().split("=", 1)[1].strip('"\'')
                            break
        
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "SolanaNarrativeRadar/2.0"
        }
    
    def _make_request(self, endpoint: str, method: str = "GET", data: dict = None) -> Optional[dict]:
        """Make a request to Helius API"""
        url = f"{self.BASE_URL}{endpoint}?api-key={self.api_key}"
        
        try:
            if method == "POST" and data:
                req = urllib.request.Request(
                    url, 
                    data=json.dumps(data).encode(),
                    headers=self.headers,
                    method="POST"
                )
            else:
                req = urllib.request.Request(url, headers=self.headers)
            
            with urllib.request.urlopen(req, timeout=15) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"    ⚠️ Helius API error: {e}")
            return None
    
    def _make_rpc_request(self, method: str, params: list = None) -> Optional[dict]:
        """Make an RPC request to Helius RPC endpoint"""
        url = f"{self.RPC_URL}/?api-key={self.api_key}"
        
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or []
        }
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode(),
                headers=self.headers,
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                result = json.loads(response.read().decode())
                return result.get("result")
        except Exception as e:
            print(f"    ⚠️ Helius RPC error: {e}")
            return None
    
    def get_network_stats(self) -> Dict[str, Any]:
        """Get current network performance stats"""
        stats = {
            "tps": 0,
            "slot": 0,
            "epoch": 0,
            "block_height": 0,
            "active_validators": 0
        }
        
        # Get recent performance samples
        perf = self._make_rpc_request("getRecentPerformanceSamples", [1])
        if perf and len(perf) > 0:
            sample = perf[0]
            stats["tps"] = round(sample.get("numTransactions", 0) / sample.get("samplePeriodSecs", 1))
        
        # Get epoch info
        epoch_info = self._make_rpc_request("getEpochInfo")
        if epoch_info:
            stats["epoch"] = epoch_info.get("epoch", 0)
            stats["slot"] = epoch_info.get("absoluteSlot", 0)
            stats["block_height"] = epoch_info.get("blockHeight", 0)
        
        # Get validator count
        vote_accounts = self._make_rpc_request("getVoteAccounts")
        if vote_accounts:
            stats["active_validators"] = len(vote_accounts.get("current", []))
        
        return stats
    
    def get_trending_tokens(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get tokens with recent high activity using DAS API"""
        tokens = []
        
        # Use the token metadata endpoint to get popular SPL tokens
        # We'll query known high-activity mints
        popular_mints = [
            "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",  # JUP
            "85VBFQZC9TZkfaptBWjvUw7YbZjy52A6mjtPGjstQAmQ",  # W (Wormhole)
            "EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm",  # WIF
            "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",  # BONK
            "7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr",  # POPCAT
            "MEW1gQWJ3nEXg2qgERiKu7FAFj79PHvQVREQUzScPP5",   # MEW
        ]
        
        for mint in popular_mints[:limit]:
            metadata = self._get_token_metadata(mint)
            if metadata:
                tokens.append(metadata)
        
        return tokens
    
    def _get_token_metadata(self, mint: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a specific token mint"""
        result = self._make_rpc_request("getAsset", [mint])
        if result:
            content = result.get("content", {})
            metadata = content.get("metadata", {})
            return {
                "mint": mint,
                "name": metadata.get("name", "Unknown"),
                "symbol": metadata.get("symbol", "???"),
                "supply": result.get("supply", {}).get("print_current_supply", 0),
                "interface": result.get("interface", "unknown")
            }
        return None
    
    def get_recent_program_activity(self) -> List[Dict[str, Any]]:
        """Analyze recent program activity to detect trending protocols"""
        activities = []
        
        # Key Solana programs to track for narrative signals
        programs = {
            # DeFi
            "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4": {"name": "Jupiter", "category": "defi_evolution"},
            "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8": {"name": "Raydium", "category": "defi_evolution"},
            "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc": {"name": "Orca Whirlpools", "category": "defi_evolution"},
            "MFv2hWf31Z9kbCa1snEPYctwafyhdvnV7FZnsebVacA": {"name": "Marginfi", "category": "defi_evolution"},
            "KLend2g3cP87ber7j6xNxhQNGFpxmuQJ9HqaJwk9iCKc": {"name": "Kamino", "category": "defi_evolution"},
            
            # Memecoins
            "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P": {"name": "Pump.fun", "category": "memecoins"},
            
            # Staking
            "mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So": {"name": "Marinade", "category": "infrastructure"},
            "Jito4APyf642JPZPx3hGc6WWJ8zPKtRbRs4P815Awbb": {"name": "Jito", "category": "infrastructure"},
            
            # NFT/Compression
            "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s": {"name": "Metaplex", "category": "zk_compression"},
            "cmtDvXumGCrqC1Age74AVPhSRVXJMd8PJS91L8KbNCK": {"name": "Bubblegum (cNFT)", "category": "zk_compression"},
        }
        
        for program_id, info in programs.items():
            # Get signatures for program
            sigs = self._make_rpc_request("getSignaturesForAddress", [
                program_id,
                {"limit": 100}
            ])
            
            if sigs:
                tx_count = len(sigs)
                # Calculate approximate time span
                if tx_count > 0:
                    activities.append({
                        "program_id": program_id,
                        "name": info["name"],
                        "category": info["category"],
                        "recent_tx_count": tx_count,
                        "activity_level": "high" if tx_count > 80 else "medium" if tx_count > 40 else "low"
                    })
        
        # Sort by activity
        activities.sort(key=lambda x: x["recent_tx_count"], reverse=True)
        return activities
    
    def get_stablecoin_metrics(self) -> Dict[str, Any]:
        """Get stablecoin supply and activity metrics"""
        stablecoins = {
            "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": "USDC",
            "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": "USDT",
            "USDSwr9ApdHk5bvJKMjzff41FfuX8bSxdKcR81vTwcA": "USDS",
        }
        
        metrics = {
            "total_supply_usd": 0,
            "tokens": []
        }
        
        for mint, name in stablecoins.items():
            supply_data = self._make_rpc_request("getTokenSupply", [mint])
            if supply_data:
                ui_amount = float(supply_data.get("value", {}).get("uiAmountString", "0"))
                metrics["tokens"].append({
                    "name": name,
                    "mint": mint,
                    "supply": ui_amount
                })
                metrics["total_supply_usd"] += ui_amount
        
        return metrics
    
    def get_nft_activity(self) -> Dict[str, Any]:
        """Get recent NFT trading activity signals"""
        # Track major NFT marketplaces
        marketplaces = {
            "M2mx93ekt1fmXSVkTrUL9xVFHkmME8HTUi5Cyc5aF7K": "Magic Eden",
            "TSWAPaqyCSx2KABk68Shruf4rp7CxcNi8hAsbdwmHbN": "Tensor",
        }
        
        activity = {
            "total_recent_trades": 0,
            "marketplaces": []
        }
        
        for program_id, name in marketplaces.items():
            sigs = self._make_rpc_request("getSignaturesForAddress", [
                program_id,
                {"limit": 50}
            ])
            
            if sigs:
                tx_count = len(sigs)
                activity["marketplaces"].append({
                    "name": name,
                    "recent_trades": tx_count
                })
                activity["total_recent_trades"] += tx_count
        
        return activity
    
    def get_narrative_signals(self) -> List[Dict[str, Any]]:
        """Generate narrative signals from on-chain data"""
        signals = []
        
        print("    ├── Fetching network stats...")
        network = self.get_network_stats()
        if network["tps"] > 0:
            signals.append({
                "source": "helius_onchain",
                "title": f"Solana Network: {network['tps']:,} TPS, {network['active_validators']:,} Validators",
                "description": f"Real-time network performance: {network['tps']:,} transactions per second across {network['active_validators']:,} active validators. Epoch {network['epoch']}, block height {network['block_height']:,}.",
                "category": "infrastructure",
                "metrics": network,
                "signal_strength": "high" if network["tps"] > 3000 else "medium"
            })
        
        print("    ├── Analyzing program activity...")
        programs = self.get_recent_program_activity()
        for prog in programs[:5]:
            if prog["activity_level"] in ["high", "medium"]:
                signals.append({
                    "source": "helius_onchain",
                    "title": f"{prog['name']}: {prog['recent_tx_count']} recent transactions",
                    "description": f"{prog['name']} showing {prog['activity_level']} activity with {prog['recent_tx_count']} transactions in recent blocks. This indicates strong {prog['category'].replace('_', ' ')} narrative momentum.",
                    "category": prog["category"],
                    "metrics": prog,
                    "signal_strength": prog["activity_level"]
                })
        
        print("    ├── Checking stablecoin metrics...")
        stables = self.get_stablecoin_metrics()
        if stables["total_supply_usd"] > 0:
            signals.append({
                "source": "helius_onchain",
                "title": f"${stables['total_supply_usd']/1e9:.2f}B Stablecoins on Solana",
                "description": f"Total stablecoin supply on Solana: ${stables['total_supply_usd']/1e9:.2f}B. USDC leads with ${stables['tokens'][0]['supply']/1e9:.2f}B. Strong PayFi infrastructure signal.",
                "category": "stablecoins_payfi",
                "metrics": stables,
                "signal_strength": "high" if stables["total_supply_usd"] > 5e9 else "medium"
            })
        
        print("    └── Analyzing NFT marketplace activity...")
        nft = self.get_nft_activity()
        if nft["total_recent_trades"] > 0:
            top_marketplace = max(nft["marketplaces"], key=lambda x: x["recent_trades"]) if nft["marketplaces"] else {"name": "Unknown", "recent_trades": 0}
            signals.append({
                "source": "helius_onchain",
                "title": f"NFT Trading: {nft['total_recent_trades']} recent trades",
                "description": f"{top_marketplace['name']} leading with {top_marketplace['recent_trades']} recent trades. NFT and compressed NFT activity remains active, signaling ongoing zk_compression adoption.",
                "category": "zk_compression",
                "metrics": nft,
                "signal_strength": "medium" if nft["total_recent_trades"] > 50 else "low"
            })
        
        return signals


def fetch_helius_signals(api_key: str = None) -> List[Dict[str, Any]]:
    """Main function to fetch all Helius on-chain signals"""
    fetcher = HeliusFetcher(api_key)
    
    if not fetcher.api_key:
        print("    ⚠️ No Helius API key found, skipping on-chain data")
        return []
    
    return fetcher.get_narrative_signals()


if __name__ == "__main__":
    # Test the fetcher
    signals = fetch_helius_signals()
    print(f"\n=== HELIUS SIGNALS ({len(signals)}) ===")
    for s in signals:
        print(f"\n[{s['category']}] {s['title']}")
        print(f"  {s['description'][:100]}...")
