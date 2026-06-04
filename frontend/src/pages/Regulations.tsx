import React from 'react';

export default function Regulations() {
  const regulations = [
    { id: "SEBI/HO/IMD/DF2/CIR/P/2023/128", title: "Master Circular for Specialized Investment Funds", date: "Oct 12, 2023", status: "Active", tag: "Master Circular" },
    { id: "SEBI/HO/IMD/IMD-I/DOF5/P/CIR/2022/29", title: "Standardization of Exit Load Methodologies", date: "Mar 15, 2022", status: "Active", tag: "Compliance" },
    { id: "SEBI/HO/MRD/MRD-PoD-1/P/CIR/2024/14", title: "Framework for Corporate Debt Market Development Fund", date: "Feb 04, 2024", status: "Recent", tag: "Framework" },
    { id: "SEBI/HO/IMD/DF3/CIR/P/2020/197", title: "Product Labeling in Mutual Funds - Risk-o-meter", date: "Oct 05, 2020", status: "Active", tag: "Disclosure" },
  ];

  return (
    <div className="p-lg lg:p-xl max-w-5xl mx-auto w-full pb-32 animate-fade-up">
      <div className="mb-lg border-b border-[#152238] pb-md">
        <h1 className="font-headline-lg text-headline-lg text-on-surface mb-2 flex items-center gap-2">
          <span className="material-symbols-outlined text-primary text-3xl">gavel</span>
          Regulatory Repository
        </h1>
        <p className="text-on-surface-variant text-lg max-w-3xl">
          Directly linked to SEBI's master database. All regulations here are currently indexed in the Vector Database.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {regulations.map((reg, idx) => (
          <div key={idx} className="bg-[#020617] border border-[#152238] rounded-xl p-6 hover:border-primary/40 transition-colors flex gap-6 items-start group">
            <div className="w-12 h-12 rounded-full bg-surface-variant flex items-center justify-center shrink-0 border border-outline-variant/30 group-hover:bg-primary/20 group-hover:text-primary transition-colors">
              <span className="material-symbols-outlined">description</span>
            </div>
            
            <div className="flex-1">
              <div className="flex justify-between items-start mb-2">
                <span className="font-mono-data text-xs text-primary bg-primary/10 px-2 py-1 rounded">
                  {reg.id}
                </span>
                <span className="font-mono-data text-xs text-on-surface-variant">{reg.date}</span>
              </div>
              <h3 className="font-headline-md text-lg text-on-surface mb-2 group-hover:text-primary transition-colors">
                {reg.title}
              </h3>
              <div className="flex items-center gap-3 mt-4">
                <span className="flex items-center gap-1 text-xs font-semibold text-secondary bg-secondary/10 px-2 py-1 rounded">
                  <span className="material-symbols-outlined text-[14px]">check_circle</span>
                  {reg.status}
                </span>
                <span className="text-xs font-mono-data text-on-surface-variant border border-[#152238] px-2 py-1 rounded">
                  {reg.tag}
                </span>
              </div>
            </div>

            <button className="p-3 bg-surface-container rounded-lg text-on-surface-variant hover:text-on-surface hover:bg-surface-variant transition-colors border border-[#152238]">
              <span className="material-symbols-outlined block">download</span>
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
