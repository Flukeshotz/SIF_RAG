import React from 'react';

interface TopNavBarProps {
    isDemoMode: boolean;
    setIsDemoMode: (val: boolean) => void;
}

const TopNavBar: React.FC<TopNavBarProps> = ({ isDemoMode, setIsDemoMode }) => {
    return (
        <nav className="fixed top-0 left-0 w-full z-50 h-12 flex justify-between items-center px-gutter bg-surface/60 backdrop-blur-md border-b border-outline-variant shadow-sm">
            <div className="flex items-center gap-md flex-1 overflow-hidden">
                <div className="font-display-lg text-headline-md font-bold tracking-tight text-primary ml-4">SIF Copilot V2</div>
                
                {/* Market Ticker */}
                <div className="hidden md:flex overflow-hidden w-full max-w-2xl items-center border-l border-r border-outline-variant px-md h-full ml-4">
                    <div className="motion-safe:animate-ticker flex gap-xl whitespace-nowrap font-mono-data text-mono-data text-on-surface-variant w-full">
                        <span><span className="text-secondary">NIFTY</span> 22,450.50 ▲ +0.4%</span>
                        <span><span className="text-error">SENSEX</span> 73,810.15 ▼ -0.1%</span>
                        <span><span className="text-secondary">USDINR</span> 83.20 ▲ +0.05%</span>
                        <span><span className="text-secondary">NIFTY</span> 22,450.50 ▲ +0.4%</span>
                    </div>
                </div>
            </div>

            <div className="flex items-center gap-md pl-md">
                {/* Toggles */}
                <div className="hidden lg:flex items-center gap-xs mr-4 border-r border-outline-variant pr-md">
                    <label className="flex items-center cursor-pointer gap-2 mr-2">
                        <div className="relative">
                            <input type="checkbox" className="sr-only" checked={isDemoMode} onChange={(e) => setIsDemoMode(e.target.checked)} />
                            <div className={`block w-8 h-5 rounded-full ${isDemoMode ? 'bg-secondary' : 'bg-surface-variant'}`}></div>
                            <div className={`dot absolute left-1 top-1 bg-on-surface w-3 h-3 rounded-full transition ${isDemoMode ? 'transform translate-x-3' : ''}`}></div>
                        </div>
                        <span className="text-xs text-on-surface-variant font-label-md">Demo Mode</span>
                    </label>
                </div>
                {/* System Status & Live Corpus */}
                <div className="hidden lg:flex items-center gap-md border-r border-outline-variant pr-md">
                    <div className="flex items-center gap-xs">
                        <div className="w-2 h-2 rounded-full bg-secondary shadow-[0_0_8px_rgba(78,222,163,0.6)] animate-pulse"></div>
                        <span className="font-label-md text-label-md text-on-surface-variant">System Status</span>
                    </div>
                    <div className="flex items-center gap-xs">
                        <div className="w-2 h-2 rounded-full bg-primary shadow-[0_0_8px_rgba(173,198,255,0.6)] animate-pulse delay-500"></div>
                        <span className="font-label-md text-label-md text-on-surface-variant">Live Corpus</span>
                    </div>
                </div>
                <div className="flex items-center gap-sm mr-4">
                    <button className="p-xs text-on-surface-variant hover:bg-surface-variant/50 transition-colors rounded-full flex items-center justify-center opacity-80">
                        <span className="material-symbols-outlined" style={{fontVariationSettings: "'FILL' 0"}}>notifications</span>
                    </button>
                    <button className="p-xs text-on-surface-variant hover:bg-surface-variant/50 transition-colors rounded-full flex items-center justify-center opacity-80">
                        <span className="material-symbols-outlined" style={{fontVariationSettings: "'FILL' 0"}}>account_circle</span>
                    </button>
                </div>
            </div>
        </nav>
    );
};

export default TopNavBar;
