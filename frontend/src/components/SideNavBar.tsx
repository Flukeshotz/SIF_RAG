import React from 'react';

interface SideNavBarProps {
    onViewChange: (view: 'chat' | 'architecture' | 'insights' | 'scheduler' | 'coming_soon') => void;
    currentView: string;
}

const SideNavBar: React.FC<SideNavBarProps> = ({ onViewChange, currentView }) => {
    return (
        <aside className="hidden md:flex fixed left-0 top-0 h-full z-40 pt-12 flex-col w-[280px] bg-surface-container-low border-r border-outline-variant">
            <div className="p-margin flex flex-col gap-xs border-b border-outline-variant">
                <h1 className="font-headline-md text-headline-md font-black text-primary">SIF Terminal</h1>
                <p className="font-label-md text-label-md text-on-surface-variant">Institutional Grade</p>
            </div>
            
            <div className="px-md py-md">
                <button 
                    onClick={() => window.location.reload()}
                    className="w-full flex items-center justify-center gap-sm bg-primary text-on-primary font-label-md text-label-md py-sm rounded-lg hover:bg-primary-fixed transition-colors"
                >
                    <span className="material-symbols-outlined text-[18px]">add</span>
                    + New Research
                </button>
            </div>

            <div className="flex-1 overflow-y-auto px-sm py-sm flex flex-col gap-base">
                <button onClick={() => onViewChange('chat')} className={`flex items-center gap-md px-md py-sm rounded-lg font-semibold transition-all w-full ${currentView === 'chat' ? 'bg-secondary-container text-on-secondary-container scale-95 duration-100' : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-variant'}`}>
                    <span className="material-symbols-outlined text-[20px]" style={currentView === 'chat' ? {fontVariationSettings: "'FILL' 1"} : {}}>search_insights</span>
                    <span className="font-label-md text-label-md">Research</span>
                </button>
                
                <button onClick={() => onViewChange('funds')} className={`flex items-center gap-md px-md py-sm rounded-lg transition-all w-full text-left ${currentView === 'funds' ? 'bg-secondary-container text-on-secondary-container' : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-variant'}`}>
                    <span className="material-symbols-outlined text-[20px]">account_balance</span>
                    <span className="font-label-md text-label-md">Funds</span>
                </button>
                <button onClick={() => onViewChange('regulations')} className={`flex items-center gap-md px-md py-sm rounded-lg transition-all w-full text-left ${currentView === 'regulations' ? 'bg-secondary-container text-on-secondary-container' : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-variant'}`}>
                    <span className="material-symbols-outlined text-[20px]">gavel</span>
                    <span className="font-label-md text-label-md">Regulations</span>
                </button>
                <button onClick={() => onViewChange('insights')} className={`flex items-center gap-md px-md py-sm rounded-lg transition-all w-full text-left ${currentView === 'insights' ? 'bg-secondary-container text-on-secondary-container' : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-variant'}`}>
                    <span className="material-symbols-outlined text-[20px]">psychology</span>
                    <span className="font-label-md text-label-md">Corpus Intelligence</span>
                </button>
                <button onClick={() => onViewChange('knowledge_graph')} className={`flex items-center gap-md px-md py-sm rounded-lg transition-all w-full text-left ${currentView === 'knowledge_graph' ? 'bg-secondary-container text-on-secondary-container' : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-variant'}`}>
                    <span className="material-symbols-outlined text-[20px]">hub</span>
                    <span className="font-label-md text-label-md">Knowledge Graph</span>
                </button>
                <button onClick={() => onViewChange('architecture')} className={`flex items-center gap-md px-md py-sm rounded-lg transition-all w-full text-left ${currentView === 'architecture' ? 'bg-secondary-container text-on-secondary-container' : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-variant'}`}>
                    <span className="material-symbols-outlined text-[20px]">schema</span>
                    <span className="font-label-md text-label-md">Architecture</span>
                </button>
                <button onClick={() => onViewChange('scheduler')} className={`flex items-center gap-md px-md py-sm rounded-lg transition-all w-full text-left ${currentView === 'scheduler' ? 'bg-secondary-container text-on-secondary-container' : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-variant'}`}>
                    <span className="material-symbols-outlined text-[20px]">monitor_heart</span>
                    <span className="font-label-md text-label-md">System Health</span>
                </button>
            </div>

            <div className="p-sm flex flex-col gap-base border-t border-outline-variant">
                <a href="#" className="flex items-center gap-md px-md py-sm text-on-surface-variant hover:text-on-surface hover:bg-surface-variant rounded-lg transition-all">
                    <span className="material-symbols-outlined text-[20px]">settings</span>
                    <span className="font-label-md text-label-md">Settings</span>
                </a>
                <a href="#" className="flex items-center gap-md px-md py-sm text-on-surface-variant hover:text-on-surface hover:bg-surface-variant rounded-lg transition-all">
                    <span className="material-symbols-outlined text-[20px]">help</span>
                    <span className="font-label-md text-label-md">Help</span>
                </a>
            </div>
        </aside>
    );
};

export default SideNavBar;
