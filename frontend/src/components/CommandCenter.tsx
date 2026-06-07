import React, { useState, useEffect } from 'react';
import { fetchIntelligence, type IntelligenceItem } from '../api';

interface CommandCenterProps {
    onSearch: (query: string) => void;
}

const CommandCenter: React.FC<CommandCenterProps> = ({ onSearch }) => {
    const [inputValue, setInputValue] = useState("");
    const [feed, setFeed] = useState<IntelligenceItem[]>([]);

    useEffect(() => {
        const loadFeed = async () => {
            try {
                const data = await fetchIntelligence();
                if (data && data.length > 0) {
                    setFeed(data);
                }
            } catch (err) {
                console.error("Failed to load intelligence feed", err);
            }
        };
        loadFeed();
        const interval = setInterval(loadFeed, 60000 * 5); // Poll frontend every 5m
        return () => clearInterval(interval);
    }, []);

    const displayFeed = feed.length > 0 ? feed : [
        {
            category: "Regulatory Update",
            title: "SEBI mandates strict AUM thresholds for New SIF Launches",
            description: "The latest master circular requires Specialized Investment Funds to maintain a minimum corpus before admitting retail investors.",
            time_ago: "2h ago",
            type: "primary" as const
        },
        {
            category: "Market Insight",
            title: "Quant SIF Active Allocator sees record inflows",
            description: "Following the recent market correction, Quant's flagship SIF strategy attracted heavy HNI allocations bypassing traditional MFs.",
            time_ago: "4h ago",
            type: "secondary" as const
        }
    ];

    const handleSubmit = (e?: React.FormEvent) => {
        if (e) e.preventDefault();
        if (inputValue.trim()) {
            onSearch(inputValue);
        }
    };

    const handleSuggestionClick = (query: string) => {
        setInputValue(query);
        onSearch(query);
    };

    return (
        <div className="flex-1 flex flex-col items-center pt-[102px] px-margin overflow-y-auto">
            <div className="w-full max-w-[900px] flex flex-col items-center text-center mb-xl animate-fade-up">
                <h2 className="font-display-lg text-display-lg font-bold text-on-surface mb-sm tracking-tight">
                    What would you like to research?
                </h2>
                <p className="font-body-lg text-body-lg text-on-surface-variant max-w-2xl">
                    Search across SEBI circulars, SIF documentation, fund disclosures, and verified regulatory sources.
                </p>
            </div>

            {/* Input */}
            <div className="w-full max-w-[900px] relative group mb-md animate-fade-up" style={{ animationDelay: '200ms' }}>
                <form onSubmit={handleSubmit}>
                    <div className="absolute inset-y-0 left-0 pl-md flex items-center pointer-events-none">
                        <span className="material-symbols-outlined text-outline">search</span>
                    </div>
                    <input 
                        className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl py-lg pl-[52px] pr-lg text-body-lg text-on-surface placeholder:text-outline-variant focus:border-primary focus:ring-0 outline-none transition-all duration-300 shadow-[0_0_0_rgba(77,142,255,0)] focus:shadow-[0_0_15px_rgba(77,142,255,0.15)]" 
                        placeholder="Ask anything..." 
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                    />
                    <div className="absolute inset-y-0 right-0 pr-sm flex items-center">
                        <button 
                            type="submit"
                            className="bg-primary/10 text-primary hover:bg-primary hover:text-on-primary p-sm rounded-lg transition-colors border border-primary/20"
                        >
                            <span className="material-symbols-outlined text-[20px]">arrow_forward</span>
                        </button>
                    </div>
                </form>
            </div>

            {/* Suggestions */}
            <div className="w-full max-w-[900px] flex flex-wrap justify-center gap-sm mb-xl animate-fade-up" style={{ animationDelay: '300ms' }}>
                <button 
                    onClick={() => handleSuggestionClick("Compare Quant vs Tata")}
                    className="flex items-center gap-xs px-sm py-xs rounded-lg border border-outline-variant bg-surface-container-low text-on-surface-variant hover:text-primary hover:border-primary/50 transition-colors font-label-md text-label-md"
                >
                    <span className="material-symbols-outlined text-[16px]">compare_arrows</span>
                    Compare Quant vs Tata
                </button>
                <button 
                    onClick={() => handleSuggestionClick("What are the specific exit load regulations for Social Impact Funds (SIF) under SEBI guidelines?")}
                    className="flex items-center gap-xs px-sm py-xs rounded-lg border border-outline-variant bg-surface-container-low text-on-surface-variant hover:text-primary hover:border-primary/50 transition-colors font-label-md text-label-md"
                >
                    <span className="material-symbols-outlined text-[16px]">update</span>
                    Latest SEBI changes
                </button>
                <button 
                    onClick={() => handleSuggestionClick("Exit load methodologies")}
                    className="flex items-center gap-xs px-sm py-xs rounded-lg border border-outline-variant bg-surface-container-low text-on-surface-variant hover:text-primary hover:border-primary/50 transition-colors font-label-md text-label-md"
                >
                    <span className="material-symbols-outlined text-[16px]">article</span>
                    Exit load methodologies
                </button>
            </div>

            {/* Daily Intelligence Feed */}
            <div className="w-full max-w-[900px] flex flex-col gap-md mt-lg pb-margin animate-fade-up" style={{ animationDelay: '400ms' }}>
                <div className="flex items-center gap-sm mb-sm border-b border-outline-variant pb-xs">
                    <span className="material-symbols-outlined text-primary text-[20px]">auto_awesome</span>
                    <h3 className="font-headline-md text-headline-md text-on-surface">Daily Intelligence Feed</h3>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-md">
                    {displayFeed.map((item, idx) => {
                        const borderHover = item.type === 'primary' ? 'hover:border-primary/40' : item.type === 'error' ? 'hover:border-error/40' : 'hover:border-secondary/40';
                        const bgIndicator = item.type === 'primary' ? 'bg-primary' : item.type === 'error' ? 'bg-error' : 'bg-secondary';
                        const badgeColors = item.type === 'primary' ? 'text-primary bg-primary/10' : item.type === 'error' ? 'text-error bg-error/10' : 'text-secondary bg-secondary/10';
                        
                        return (
                        <div key={idx} className={`bg-surface rounded-xl border border-outline-variant p-md ${borderHover} transition-colors flex flex-col gap-sm relative overflow-hidden`}>
                            <div className={`absolute top-0 left-0 w-1 h-full ${bgIndicator}`}></div>
                            <div className="flex justify-between items-start">
                                <span className={`font-label-md text-label-md px-xs py-[2px] rounded uppercase tracking-wider ${badgeColors}`}>{item.category}</span>
                                <span className="font-mono-data text-mono-data text-on-surface-variant">{item.time_ago}</span>
                            </div>
                            <h4 className="font-headline-md text-[16px] leading-tight text-on-surface mt-xs">{item.title}</h4>
                            <p className="font-body-md text-body-md text-on-surface-variant line-clamp-2">{item.description}</p>
                        </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
};

export default CommandCenter;
