interface TopNavBarProps {
  isDemoMode: boolean;
  setIsDemoMode: (val: boolean) => void;
  isPresentationMode: boolean;
  setIsPresentationMode: (val: boolean) => void;
}

export default function TopNavBar({ isDemoMode, setIsDemoMode, isPresentationMode, setIsPresentationMode }: TopNavBarProps) {
  return (
    <header className="fixed top-0 left-0 right-0 h-12 bg-surface-container-low border-b border-outline-variant z-50 flex items-center justify-between px-md md:pl-[280px]">
      <div className="flex items-center gap-sm md:hidden">
        <span className="material-symbols-outlined text-primary text-xl">smart_toy</span>
        <h2 className="font-headline-md font-bold text-primary">SIF Terminal</h2>
      </div>
      
      <div className="hidden md:flex flex-1"></div>
      
      {/* Search / Status / Toggles */}
      <div className="flex items-center gap-4">
        
        {/* Demo Mode Toggle */}
        <div className="flex items-center gap-2">
          <label className="text-xs font-mono-data text-on-surface-variant cursor-pointer" htmlFor="demo-toggle">
            Demo Mode
          </label>
          <div 
            className={`w-8 h-4 rounded-full flex items-center p-0.5 cursor-pointer transition-colors ${isDemoMode ? 'bg-primary' : 'bg-[#152238]'}`}
            onClick={() => setIsDemoMode(!isDemoMode)}
            id="demo-toggle"
          >
            <div className={`w-3 h-3 bg-white rounded-full shadow-sm transform transition-transform ${isDemoMode ? 'translate-x-4' : 'translate-x-0'}`}></div>
          </div>
        </div>

        {/* Presentation Mode Toggle */}
        <div className="flex items-center gap-2 border-l border-[#152238] pl-4">
          <label className="text-xs font-mono-data text-on-surface-variant cursor-pointer" htmlFor="presentation-toggle">
            Presentation Mode
          </label>
          <div 
            className={`w-8 h-4 rounded-full flex items-center p-0.5 cursor-pointer transition-colors ${isPresentationMode ? 'bg-secondary' : 'bg-[#152238]'}`}
            onClick={() => setIsPresentationMode(!isPresentationMode)}
            id="presentation-toggle"
          >
            <div className={`w-3 h-3 bg-white rounded-full shadow-sm transform transition-transform ${isPresentationMode ? 'translate-x-4' : 'translate-x-0'}`}></div>
          </div>
        </div>

        <div className="hidden md:flex items-center gap-sm ml-4 border-l border-[#152238] pl-4">
          <span className="material-symbols-outlined text-sm text-on-surface-variant">search</span>
          <input 
            type="text" 
            placeholder="Search corpus (⌘K)" 
            className="bg-transparent border-none text-sm text-on-surface focus:ring-0 placeholder-on-surface-variant w-48 outline-none font-body-md"
          />
        </div>
      </div>
    </header>
  );
}
