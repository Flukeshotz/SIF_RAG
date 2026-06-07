
export default function Funds() {
  const funds = [
    { name: "Quant SIF Alpha", type: "Equity", nav: "₹10.52", aum: "₹1,250 Cr", return1y: "+24.5%", risk: "High" },
    { name: "Tata Social Impact Fund", type: "Debt", nav: "₹10.40", aum: "₹4,100 Cr", return1y: "+8.2%", risk: "Low" },
    { name: "Zerodha Nifty LargeMidcap", type: "Index", nav: "₹10.10", aum: "₹850 Cr", return1y: "+18.4%", risk: "Moderate" },
    { name: "SBI Magnum SIF", type: "Hybrid", nav: "₹10.80", aum: "₹8,900 Cr", return1y: "+14.1%", risk: "Moderate" },
    { name: "Nippon India Special", type: "Equity", nav: "₹10.20", aum: "₹5,400 Cr", return1y: "+21.0%", risk: "High" },
  ];

  return (
    <div className="p-lg lg:p-xl max-w-6xl mx-auto w-full pb-32 animate-fade-up">
      <div className="mb-lg border-b border-[#152238] pb-md flex justify-between items-end">
        <div>
          <h1 className="font-headline-lg text-headline-lg text-on-surface mb-2 flex items-center gap-2">
            <span className="material-symbols-outlined text-primary text-3xl">account_balance</span>
            Active SIF Funds
          </h1>
          <p className="text-on-surface-variant text-lg max-w-3xl">
            Live monitoring of Specialized Investment Funds across the domestic market.
          </p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-surface-container border border-outline-variant rounded-lg text-on-surface hover:border-primary transition-colors">
          <span className="material-symbols-outlined text-[18px]">filter_list</span>
          Filter
        </button>
      </div>

      <div className="bg-[#020617] border border-[#152238] rounded-2xl overflow-hidden shadow-2xl">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-surface-container-low border-b border-[#152238]">
              <th className="p-4 font-label-md text-on-surface-variant font-semibold">Fund Name</th>
              <th className="p-4 font-label-md text-on-surface-variant font-semibold">Category</th>
              <th className="p-4 font-label-md text-on-surface-variant font-semibold">Current NAV</th>
              <th className="p-4 font-label-md text-on-surface-variant font-semibold">AUM</th>
              <th className="p-4 font-label-md text-on-surface-variant font-semibold">1Y Return</th>
              <th className="p-4 font-label-md text-on-surface-variant font-semibold">Risk Profile</th>
            </tr>
          </thead>
          <tbody>
            {funds.map((fund, idx) => (
              <tr key={idx} className="border-b border-[#152238]/50 hover:bg-surface-container-lowest transition-colors group cursor-pointer">
                <td className="p-4 font-body-md text-on-surface font-medium group-hover:text-primary transition-colors">{fund.name}</td>
                <td className="p-4">
                  <span className="px-2 py-1 rounded text-xs font-mono-data bg-surface-variant text-on-surface-variant border border-outline-variant/30">
                    {fund.type}
                  </span>
                </td>
                <td className="p-4 font-mono-data text-on-surface">{fund.nav}</td>
                <td className="p-4 font-mono-data text-on-surface-variant">{fund.aum}</td>
                <td className="p-4 font-mono-data text-secondary">{fund.return1y}</td>
                <td className="p-4">
                  <span className={`flex items-center gap-1 text-xs font-semibold ${fund.risk === 'High' ? 'text-error' : fund.risk === 'Moderate' ? 'text-[#eab308]' : 'text-secondary'}`}>
                    <span className="material-symbols-outlined text-[14px]">
                      {fund.risk === 'High' ? 'warning' : fund.risk === 'Moderate' ? 'trending_flat' : 'verified_user'}
                    </span>
                    {fund.risk}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
