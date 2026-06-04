import React, { useEffect, useState } from 'react';

export default function KnowledgeGraph() {
  const [nodes, setNodes] = useState<{id: number, x: number, y: number, label: string, type: string}[]>([]);
  const [edges, setEdges] = useState<{from: number, to: number}[]>([]);

  useEffect(() => {
    // Generate some deterministic random nodes for a cool graph effect
    const newNodes = [
      { id: 0, x: 50, y: 50, label: "SEBI Master Circular", type: "core" },
      { id: 1, x: 25, y: 30, label: "Exit Load Policy", type: "concept" },
      { id: 2, x: 75, y: 30, label: "AUM Threshold", type: "concept" },
      { id: 3, x: 20, y: 70, label: "Quant SIF", type: "fund" },
      { id: 4, x: 80, y: 70, label: "Tata SIF", type: "fund" },
      { id: 5, x: 50, y: 85, label: "Derivative Exposure", type: "concept" },
      { id: 6, x: 10, y: 50, label: "Tier 2 Disclosure", type: "concept" },
      { id: 7, x: 90, y: 50, label: "Liquidity Norms", type: "concept" }
    ];

    const newEdges = [
      { from: 0, to: 1 }, { from: 0, to: 2 }, { from: 0, to: 5 },
      { from: 1, to: 3 }, { from: 2, to: 4 }, { from: 5, to: 3 },
      { from: 5, to: 4 }, { from: 0, to: 6 }, { from: 0, to: 7 }
    ];

    setNodes(newNodes);
    setEdges(newEdges);
  }, []);

  return (
    <div className="p-lg lg:p-xl max-w-6xl mx-auto w-full pb-32 animate-fade-up h-full flex flex-col">
      <div className="mb-lg border-b border-[#152238] pb-md">
        <h1 className="font-headline-lg text-headline-lg text-on-surface mb-2 flex items-center gap-2">
          <span className="material-symbols-outlined text-primary text-3xl">hub</span>
          Ontology Knowledge Graph
        </h1>
        <p className="text-on-surface-variant text-lg max-w-3xl">
          Visualizing the semantic relationships between SEBI directives and specific fund entities extracted by the RAG pipeline.
        </p>
      </div>

      <div className="flex-1 bg-[#020617] border border-[#152238] rounded-2xl relative overflow-hidden min-h-[500px]">
        {/* Background grid */}
        <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'radial-gradient(#4d8eff 1px, transparent 1px)', backgroundSize: '30px 30px' }}></div>
        
        <svg className="absolute inset-0 w-full h-full">
          {/* Render edges */}
          {edges.map((edge, i) => {
            const source = nodes.find(n => n.id === edge.from);
            const target = nodes.find(n => n.id === edge.to);
            if (!source || !target) return null;
            return (
              <line 
                key={i}
                x1={`${source.x}%`} y1={`${source.y}%`}
                x2={`${target.x}%`} y2={`${target.y}%`}
                stroke="rgba(140, 144, 159, 0.2)"
                strokeWidth="2"
                className="animate-pulse"
              />
            );
          })}
        </svg>

        {/* Render nodes */}
        {nodes.map((node) => (
          <div 
            key={node.id} 
            className="absolute transform -translate-x-1/2 -translate-y-1/2 flex flex-col items-center gap-2 group cursor-pointer"
            style={{ left: `${node.x}%`, top: `${node.y}%` }}
          >
            <div className={`w-12 h-12 rounded-full flex items-center justify-center border-2 transition-all duration-300 shadow-[0_0_15px_rgba(0,0,0,0.5)] ${
              node.type === 'core' ? 'bg-primary/20 border-primary text-primary glow-active' :
              node.type === 'fund' ? 'bg-secondary/20 border-secondary text-secondary glow-secondary' :
              'bg-surface-variant border-outline-variant text-on-surface-variant group-hover:border-primary group-hover:text-primary'
            }`}>
              <span className="material-symbols-outlined">
                {node.type === 'core' ? 'account_balance' : node.type === 'fund' ? 'show_chart' : 'scatter_plot'}
              </span>
            </div>
            <span className="font-label-md text-xs bg-[#051424] px-2 py-1 rounded border border-[#152238] text-on-surface whitespace-nowrap">
              {node.label}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
