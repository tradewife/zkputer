"""
Pre-built research queries for Base ecosystem intelligence
"""
from graphiti_core import Graphiti
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class ResearchQueries:
    def __init__(self, graphiti: Graphiti):
        self.graphiti = graphiti
        
    async def get_cross_platform_trending(
        self, 
        min_score: float = 0.6,
        lookback_hours: int = 24
    ) -> List[Dict]:
        """
        Query 1: Find entities trending across multiple platforms
        High alpha: tokens/agents appearing on both GMGN and Cookie
        """
        query = f"""
        Find all tokens or agents that are:
        1. Currently trending on GMGN (rank <= 30)
        2. Showing increased mindshare on Cookie.fun (delta > 1%)
        3. Have been mentioned in the last {lookback_hours} hours
        4. Include their smart money wallet connections
        
        Return entity names, platforms, trending ranks, and connection strength.
        """
        
        results = await self.graphiti.search(
            query=query,
            num_results=20
        )
        
        return self._format_results(results, "cross_platform_trending")
    
    async def get_whale_entry_positions(
        self,
        min_wallet_pnl_7d: float = 50000,
        max_hours_since_entry: int = 6
    ) -> List[Dict]:
        """
        Query 2: Identify new positions by top-performing wallets
        Immediate alpha: copy trading opportunities
        """
        query = f"""
        Find all tokens that:
        1. Were recently bought by wallets with 7-day PnL > ${min_wallet_pnl_7d:,.0f}
        2. Purchase occurred within last {max_hours_since_entry} hours
        3. Wallet has win rate > 80%
        4. Include token trending status and price momentum
        
        Return wallet address, token symbol, entry time, wallet performance metrics.
        """
        
        results = await self.graphiti.search(
            query=query,
            num_results=15
        )
        
        return self._format_results(results, "whale_entry_positions")
    
    async def get_pre_tge_momentum_shift(
        self,
        mindshare_delta_threshold: float = 1.0,
        min_rank: int = 50
    ) -> List[Dict]:
        """
        Query 3: Pre-TGE projects with accelerating mindshare
        Medium-term alpha: early positioning
        """
        query = f"""
        Find pre-TGE projects that:
        1. Have 7-day mindshare delta > {mindshare_delta_threshold}%
        2. Currently ranked in top {min_rank} on Kaito
        3. Show increasing social engagement trend
        4. Have not launched token yet (status = pre-tge)
        
        Return project name, mindshare metrics, category, social signals.
        """
        
        results = await self.graphiti.search(
            query=query,
            num_results=10
        )
        
        return self._format_results(results, "pre_tge_momentum")
    
    async def get_agent_sector_rotation(
        self,
        lookback_days: int = 7
    ) -> List[Dict]:
        """
        Query 4: Detect AI agent category rotation patterns
        Sector allocation alpha
        """
        query = f"""
        Analyze AI agent categories over the last {lookback_days} days:
        1. Which categories gained the most mindshare?
        2. Which categories lost mindshare?
        3. Which specific agents led the rotation?
        4. Are there wallet flows correlating with category changes?
        
        Return category names, mindshare changes, leading agents, wallet activity.
        """
        
        results = await self.graphiti.search(
            query=query,
            num_results=20
        )
        
        return self._format_results(results, "sector_rotation")
    
    async def get_smart_money_token_overlap(
        self,
        min_wallet_count: int = 5,
        min_wallet_pnl: float = 100000
    ) -> List[Dict]:
        """
        Query 5: Tokens held by multiple high-performer wallets
        Consensus alpha signal
        """
        query = f"""
        Find tokens that:
        1. Are held by at least {min_wallet_count} different smart money wallets
        2. Each wallet has 30-day PnL > ${min_wallet_pnl:,.0f}
        3. Multiple wallets entered position recently (< 48h)
        4. Token is currently active (volume > 0)
        
        Return token symbol, number of smart wallets, average wallet performance,
        recent entry timing distribution.
        """
        
        results = await self.graphiti.search(
            query=query,
            num_results=10
        )
        
        return self._format_results(results, "smart_money_overlap")
    
    async def get_social_to_price_correlation(
        self,
        entity_type: str = "agent"  # or "token"
    ) -> List[Dict]:
        """
        Query 6: Entities where social metrics precede price action
        Predictive alpha
        """
        query = f"""
        Find {entity_type}s where:
        1. Social engagement (impressions/engagement) increased significantly
        2. Price action followed within 6-24 hours
        3. Pattern has repeated at least once historically
        4. Currently showing similar social surge
        
        Return entity name, social metrics, price correlation lag time,
        current social status.
        """
        
        results = await self.graphiti.search(
            query=query,
            num_results=15
        )
        
        return self._format_results(results, "social_price_correlation")
    
    async def get_fresh_wallet_discovery(
        self,
        max_tracked_by: int = 10,
        min_win_rate: float = 90.0
    ) -> List[Dict]:
        """
        Query 7: Undiscovered high-performance wallets
        Early follower advantage
        """
        query = f"""
        Find wallets that:
        1. Have win rate >= {min_win_rate}%
        2. Are tracked by fewer than {max_tracked_by} users (underappreciated)
        3. Have recent profitable trades (last 7 days)
        4. Are currently active (trades in last 24h)
        
        Return wallet address, performance metrics, recent trades,
        tracking status, activity recency.
        """
        
        results = await self.graphiti.search(
            query=query,
            num_results=20
        )
        
        return self._format_results(results, "fresh_wallet_discovery")
    
    async def get_temporal_pattern_query(
        self,
        pattern_type: str = "pump_before_listing",
        reference_date: Optional[str] = None
    ) -> List[Dict]:
        """
        Query 8: Historical pattern matching
        Example: "Show me tokens that pumped 2-3 days before major CEX listing"
        """
        if reference_date is None:
            ref_time = datetime.utcnow()
        else:
            ref_time = datetime.fromisoformat(reference_date)
            
        query = f"""
        Using temporal graph analysis:
        1. Find historical instances of {pattern_type} pattern
        2. Extract common leading indicators (wallet activity, social signals)
        3. Identify entities currently showing similar early indicators
        4. Calculate similarity score to historical patterns
        
        Return matching entities, pattern similarity score, leading indicators present,
        estimated time to event.
        """
        
        results = await self.graphiti.search(
            query=query,
            num_results=10,
            reference_time=ref_time
        )
        
        return self._format_results(results, f"pattern_{pattern_type}")
    
    def _format_results(self, results, query_type: str) -> List[Dict]:
        """Format Graphiti search results for consumption"""
        formatted = []
        
        for result in results:
            formatted.append({
                'query_type': query_type,
                'entity': result.get('entity'),
                'content': result.get('content'),
                'score': result.get('score'),
                'metadata': result.get('metadata'),
                'timestamp': datetime.utcnow().isoformat()
            })
            
        return formatted