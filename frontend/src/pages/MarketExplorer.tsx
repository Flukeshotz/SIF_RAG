import { useEffect, useState } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function MarketExplorer() {
    const [stats, setStats] = useState({
        total_funds: 0,
        total_amcs: 0,
        strategies: {} as Record<string, number>,
        categories: {} as Record<string, number>,
        funds: [] as any[]
    });
    const [loading, setLoading] = useState(true);
    
    // Hash-based routing state
    const [currentPath, setCurrentPath] = useState(window.location.hash.replace('#', '') || '/market');
    const [searchQuery, setSearchQuery] = useState("");
    const [selectedAMC, setSelectedAMC] = useState("All");
    const [selectedStrategy, setSelectedStrategy] = useState("All");

    useEffect(() => {
        const handleHashChange = () => {
            setCurrentPath(window.location.hash.replace('#', '') || '/market');
        };
        window.addEventListener('hashchange', handleHashChange);
        return () => window.removeEventListener('hashchange', handleHashChange);
    }, []);

    useEffect(() => {
        async function fetchRegistryData() {
            try {
                // Fetch basic endpoints concurrently
                const [fundsRes, strategiesRes, categoriesRes] = await Promise.all([
                    fetch(`${API_BASE_URL}/funds`).then(res => res.json()),
                    fetch(`${API_BASE_URL}/funds/strategies`).then(res => res.json()),
                    fetch(`${API_BASE_URL}/funds/categories`).then(res => res.json())
                ]);

                // Compute total AMCs uniquely
                const amcs = new Set(fundsRes.map((f: any) => f.amc));

                setStats({
                    total_funds: fundsRes.length,
                    total_amcs: amcs.size,
                    strategies: strategiesRes,
                    categories: categoriesRes,
                    funds: fundsRes
                });
            } catch (e) {
                console.error("Failed to fetch registry data", e);
            } finally {
                setLoading(false);
            }
        }
        fetchRegistryData();
    }, []);

    const trackFundView = async (fund: any) => {
        try {
            await fetch(`${API_BASE_URL}/analytics/view_fund`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    fund_id: fund.fund_id,
                    amc: fund.amc,
                    strategy: fund.strategy
                })
            });
            // Also open official URL
            if (fund.official_url || fund.groww_url) {
                window.open(fund.official_url || fund.groww_url, '_blank');
            }
        } catch (e) {
            console.error("Tracking error", e);
        }
    };

    if (loading) {
        return (
            <div className="w-full h-full flex flex-col items-center justify-center">
                <span className="material-symbols-outlined animate-spin text-primary text-4xl mb-4">sync</span>
                <p className="text-on-surface font-mono-data uppercase tracking-widest text-xs">Loading Market Intelligence...</p>
            </div>
        );
    }
    
    // Parse route parameters
    let viewMode = "market";
    let filterParam = "";
    if (currentPath.startsWith('/amc/')) {
        viewMode = "amc";
        filterParam = currentPath.replace('/amc/', '').replace(/-/g, ' ');
    } else if (currentPath.startsWith('/strategy/')) {
        viewMode = "strategy";
        filterParam = currentPath.replace('/strategy/', '').replace(/-/g, ' ');
    }

    // Filter funds for main display
    let filteredFunds = stats.funds;
    if (viewMode === "amc") {
        filteredFunds = filteredFunds.filter(f => f.amc.toLowerCase().replace(/[- ]/g, '') === filterParam.toLowerCase().replace(/[- ]/g, ''));
    } else if (viewMode === "strategy") {
        filteredFunds = filteredFunds.filter(f => f.strategy.toLowerCase().replace(/[- ]/g, '') === filterParam.toLowerCase().replace(/[- ]/g, ''));
    } else {
        // Market view general filters
        if (selectedAMC !== "All") {
            filteredFunds = filteredFunds.filter(f => f.amc === selectedAMC);
        }
        if (selectedStrategy !== "All") {
            filteredFunds = filteredFunds.filter(f => f.strategy === selectedStrategy);
        }
    }
    
    // Search filter applies universally
    if (searchQuery) {
        filteredFunds = filteredFunds.filter(f => 
            f.fund_name.toLowerCase().includes(searchQuery.toLowerCase()) || 
            f.amc.toLowerCase().includes(searchQuery.toLowerCase())
        );
    }

    const uniqueAMCs = Array.from(new Set(stats.funds.map(f => f.amc))).sort();
    const uniqueStrategies = Array.from(new Set(stats.funds.map(f => f.strategy))).sort();

    const FundCard = ({ fund }: { fund: any }) => (
        <div 
            onClick={() => trackFundView(fund)}
            className="bg-surface-container border border-[#152238] rounded-xl p-5 hover:border-primary/50 transition-colors cursor-pointer group"
        >
            <div className="flex justify-between items-start mb-3">
                <h3 className="font-semibold text-on-surface group-hover:text-primary transition-colors">{fund.fund_name}</h3>
                <span className={`text-[10px] uppercase font-bold px-2 py-1 rounded ${fund.status === 'Live' ? 'bg-[#10b981]/10 text-[#10b981]' : 'bg-[#0ea5e9]/10 text-[#0ea5e9]'}`}>
                    {fund.status}
                </span>
            </div>
            <div className="flex flex-col gap-1 mt-4 border-t border-[#152238] pt-3">
                <div className="flex justify-between text-xs">
                    <span className="text-on-surface-variant">AMC</span>
                    <a href={`#/amc/${fund.amc.toLowerCase().replace(/ /g, '-')}`} className="text-secondary hover:underline" onClick={e => e.stopPropagation()}>{fund.amc}</a>
                </div>
                <div className="flex justify-between text-xs mt-1">
                    <span className="text-on-surface-variant">Strategy</span>
                    <a href={`#/strategy/${fund.strategy.toLowerCase().replace(/ /g, '-')}`} className="text-secondary hover:underline" onClick={e => e.stopPropagation()}>{fund.strategy}</a>
                </div>
            </div>
        </div>
    );

    return (
        <div className="w-full h-full p-8 overflow-y-auto">
            {/* Header Navigation Area */}
            <header className="mb-8 border-b border-[#152238] pb-6">
                <div className="flex gap-4 items-center mb-4 text-sm text-on-surface-variant">
                    <a href="#/market" className="hover:text-primary transition-colors flex items-center gap-1">
                        <span className="material-symbols-outlined text-[16px]">home</span>
                        Market
                    </a>
                    {viewMode === "amc" && (
                        <>
                            <span className="material-symbols-outlined text-[16px]">chevron_right</span>
                            <span className="text-primary capitalize">{filterParam}</span>
                        </>
                    )}
                    {viewMode === "strategy" && (
                        <>
                            <span className="material-symbols-outlined text-[16px]">chevron_right</span>
                            <span className="text-primary capitalize">{filterParam}</span>
                        </>
                    )}
                </div>
                
                <div className="flex justify-between items-end">
                    <div>
                        <h1 className="text-3xl font-black text-on-surface tracking-tight capitalize">
                            {viewMode === "market" ? "Market Explorer" : filterParam}
                        </h1>
                        <p className="text-on-surface-variant text-sm mt-1">
                            {viewMode === "market" ? "Live Institutional Discovery Engine for Specialized Investment Funds." : `Viewing all ${filterParam} funds.`}
                        </p>
                    </div>
                </div>
            </header>

            {/* Filter and Search Controls (Only in Market View) */}
            {viewMode === "market" && (
                <div className="flex flex-col md:flex-row gap-4 mb-8">
                    <div className="flex-1 relative">
                        <span className="material-symbols-outlined absolute left-3 top-2.5 text-on-surface-variant">search</span>
                        <input 
                            type="text" 
                            placeholder="Search funds or AMCs..." 
                            value={searchQuery}
                            onChange={e => setSearchQuery(e.target.value)}
                            className="w-full bg-[#051424] border border-[#152238] rounded-lg py-2 pl-10 pr-4 text-sm text-on-surface focus:border-primary focus:outline-none transition-colors"
                        />
                    </div>
                    <select 
                        value={selectedAMC}
                        onChange={e => setSelectedAMC(e.target.value)}
                        className="bg-[#051424] border border-[#152238] rounded-lg py-2 px-4 text-sm text-on-surface focus:border-primary focus:outline-none"
                    >
                        <option value="All">All AMCs</option>
                        {uniqueAMCs.map(amc => <option key={amc as string} value={amc as string}>{amc as string}</option>)}
                    </select>
                    <select 
                        value={selectedStrategy}
                        onChange={e => setSelectedStrategy(e.target.value)}
                        className="bg-[#051424] border border-[#152238] rounded-lg py-2 px-4 text-sm text-on-surface focus:border-primary focus:outline-none"
                    >
                        <option value="All">All Strategies</option>
                        {uniqueStrategies.map(strat => <option key={strat as string} value={strat as string}>{strat as string}</option>)}
                    </select>
                </div>
            )}

            {/* Strategy Intelligence Metrics */}
            {viewMode === "strategy" && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                    <div className="bg-surface-container-low border border-[#152238] rounded-xl p-4 text-center">
                        <span className="text-2xl font-black text-on-surface">{filteredFunds.length}</span>
                        <span className="block text-[10px] uppercase text-on-surface-variant mt-1">Total Funds</span>
                    </div>
                    <div className="bg-surface-container-low border border-[#152238] rounded-xl p-4 text-center">
                        <span className="text-2xl font-black text-on-surface">{new Set(filteredFunds.map(f => f.amc)).size}</span>
                        <span className="block text-[10px] uppercase text-on-surface-variant mt-1">Active AMCs</span>
                    </div>
                    <div className="bg-surface-container-low border border-[#152238] rounded-xl p-4 text-center">
                        <span className="text-2xl font-black text-on-surface">{filteredFunds.filter(f => f.status === 'Live').length}</span>
                        <span className="block text-[10px] uppercase text-on-surface-variant mt-1">Live SIFs</span>
                    </div>
                    <div className="bg-surface-container-low border border-[#152238] rounded-xl p-4 text-center">
                        <span className="text-2xl font-black text-secondary">
                            {filteredFunds.length > 0 
                                ? (() => {
                                    const avg = filteredFunds.reduce((sum, f) => sum + (f.minimum_investment || 1000000), 0) / filteredFunds.length;
                                    return avg >= 10000000 
                                        ? `₹${(avg / 10000000).toFixed(1)} Cr` 
                                        : `₹${(avg / 100000).toFixed(0)} Lakhs`;
                                })()
                                : '₹0'}
                        </span>
                        <span className="block text-[10px] uppercase text-on-surface-variant mt-1">Avg Min Investment</span>
                    </div>
                </div>
            )}

            {/* Fund Grid */}
            <div>
                <h2 className="text-lg font-bold text-on-surface border-l-4 border-primary pl-3 mb-6">
                    {filteredFunds.length} Funds Discovered
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                    {filteredFunds.map((fund, idx) => <FundCard key={idx} fund={fund} />)}
                </div>
                {filteredFunds.length === 0 && (
                    <div className="text-center py-12 text-on-surface-variant">
                        No funds match your current filters.
                    </div>
                )}
            </div>
        </div>
    );
}
