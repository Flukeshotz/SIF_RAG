
export const FundCards = ({ funds }: { funds: any[] }) => {
  if (!funds || funds.length === 0) {
    return <div className="p-4 text-on-surface-variant font-mono-data">No funds match this criteria.</div>;
  }
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
      {funds.map((fund, idx) => (
        <div key={idx} className="bg-surface-container-low border border-[#152238] rounded-xl p-4 shadow-lg hover:border-primary/50 transition-colors flex flex-col h-full">
          <div className="flex justify-between items-start mb-3 border-b border-[#152238] pb-3">
            <div>
              {fund.status && <span className="text-[10px] font-mono-data text-primary uppercase tracking-wider bg-primary/10 px-1.5 py-0.5 rounded">{fund.status}</span>}
              <h3 className="font-headline-md text-on-surface mt-1">{fund.fund_name}</h3>
              <p className="text-xs text-on-surface-variant">{fund.amc}</p>
            </div>
            <div className="flex flex-col items-end">
              <span className="text-[10px] font-mono-data text-on-surface-variant uppercase mb-1">Risk</span>
              <span className="w-6 h-6 rounded-full bg-[#152238] flex items-center justify-center text-xs font-bold text-secondary border border-secondary/30 shadow-sm">{fund.risk_band || 'N/A'}</span>
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-3 mb-4 flex-1">
            <div className="bg-[#020617] rounded p-2 border border-[#152238]/50">
              <span className="block text-[10px] text-on-surface-variant uppercase mb-0.5">Strategy</span>
              <span className="text-xs font-semibold text-on-surface">{fund.strategy || 'Unknown'}</span>
            </div>
            <div className="bg-[#020617] rounded p-2 border border-[#152238]/50">
              <span className="block text-[10px] text-on-surface-variant uppercase mb-0.5">Min Investment</span>
              <span className="text-xs font-semibold text-on-surface">
                {fund.minimum_investment >= 10000000 ? `₹${fund.minimum_investment / 10000000} Cr` : 
                 fund.minimum_investment >= 100000 ? `₹${fund.minimum_investment / 100000} L` : 
                 `₹${fund.minimum_investment}`}
              </span>
            </div>
          </div>
          
          <div className="mt-auto">
            <button className="w-full py-2 bg-primary/10 hover:bg-primary/20 text-primary text-xs font-bold uppercase tracking-wider rounded transition-colors border border-primary/30 shadow-sm flex items-center justify-center gap-2">
              <span className="material-symbols-outlined text-[14px]">compare_arrows</span> Compare
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export const ComparisonTable = ({ funds }: { funds: any[] }) => {
  if (!funds || funds.length < 2) {
    return <div className="p-4 text-on-surface-variant font-mono-data">Need at least 2 funds to compare.</div>;
  }
  
  const properties = [
    { key: 'amc', label: 'AMC' },
    { key: 'strategy', label: 'Strategy' },
    { key: 'investment_objective', label: 'Investment Objective' },
    { key: 'portfolio_construction', label: 'Portfolio Construction' },
    { key: 'hedging_approach', label: 'Hedging Approach' },
    { key: 'target_equity_exposure', label: 'Target Equity Exposure' },
    { key: 'differentiators', label: 'Differentiators' },
    { key: 'risk_band', label: 'Risk Band' },
    { key: 'status', label: 'Status' },
    { key: 'minimum_investment', label: 'Min Investment' },
  ];
  
  return (
    <div className="overflow-x-auto mt-4 bg-surface-container border border-[#152238] rounded-xl shadow-lg">
      <table className="w-full text-left border-collapse min-w-[600px]">
        <thead>
          <tr>
            <th className="p-4 font-label-md text-on-surface-variant font-semibold tracking-wide border-r border-[#152238] bg-surface-container-low w-1/4">Metric</th>
            {funds.map((fund, idx) => (
              <th key={idx} className="p-4 font-label-md text-primary font-bold tracking-wide border-r border-[#152238] last:border-r-0 bg-surface-container-low text-center">
                {fund.fund_name}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {properties.map((prop, i) => (
            <tr key={prop.key} className={i % 2 === 0 ? 'bg-[#020617]' : 'bg-[#051424]'}>
              <td className="p-4 font-mono-data text-xs text-on-surface-variant uppercase border-r border-[#152238]/30 font-semibold">{prop.label}</td>
              {funds.map((fund, idx) => (
                <td key={idx} className="p-4 font-body-md text-on-surface border-r border-[#152238]/30 last:border-r-0 text-center align-middle">
                  {prop.key === 'risk_band' ? (
                    <span className="inline-flex w-6 h-6 rounded-full bg-[#152238] items-center justify-center text-xs font-bold text-secondary border border-secondary/30">{fund[prop.key] || 'N/A'}</span>
                  ) : prop.key === 'minimum_investment' ? (
                    <span className="font-semibold">
                      {fund[prop.key] >= 10000000 ? `₹${fund[prop.key] / 10000000} Cr` : 
                       fund[prop.key] >= 100000 ? `₹${fund[prop.key] / 100000} L` : 
                       `₹${fund[prop.key]}`}
                    </span>
                  ) : (
                    fund[prop.key] || 'Unknown'
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
