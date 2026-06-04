import { useState, useEffect, Suspense, lazy } from 'react';
import TopNavBar from './components/TopNavBar';
import SideNavBar from './components/SideNavBar';
import ChatArea from './components/ChatArea';
import CommandCenter from './components/CommandCenter';
import EvidenceExplorer from './components/EvidenceExplorer';
import Tour from './components/Tour';
import { submitQuery } from './api';
import type { Message } from './types';

// Lazy loaded routes
const Architecture = lazy(() => import('./pages/Architecture'));
const Insights = lazy(() => import('./pages/Insights'));
const SchedulerDashboard = lazy(() => import('./pages/SchedulerDashboard'));

function App() {
  const [activeCitationId, setActiveCitationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentView, setCurrentView] = useState<'chat' | 'architecture' | 'insights' | 'scheduler'>('chat');
  
  // App State Toggles
  const [isDemoMode, setIsDemoMode] = useState(false);

  
  // Tour State
  const [showTour, setShowTour] = useState(false);

  useEffect(() => {
    const savedTour = localStorage.getItem('sif_tour_completed');
    if (!savedTour) {
      setShowTour(true);
    }
  }, []);

  const completeTour = () => {
    localStorage.setItem('sif_tour_completed', 'true');
    setShowTour(false);
  };

  useEffect(() => {
    const saved = localStorage.getItem('sif_messages');
    if (saved) {
      try {
        setMessages(JSON.parse(saved));
      } catch (e) {
        console.error('Failed to parse saved messages');
      }
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('sif_messages', JSON.stringify(messages));
  }, [messages]);

  const handleCitationClick = (chunkId: string) => {
    setActiveCitationId(chunkId);
  };

  const handleCloseExplorer = () => {
    setActiveCitationId(null);
  };

  const executeQuery = async (query: string) => {
    if (!query.trim() || isLoading) return;

    const userMessage: Message = { id: Date.now().toString(), type: 'user', text: query };
    const loadingMessage: Message = { id: (Date.now() + 1).toString(), type: 'ai', text: '', loading: true };
    
    setMessages(prev => [...prev, userMessage, loadingMessage]);
    setIsLoading(true);

    if (isDemoMode) {
      // Fake delay and canned response
      setTimeout(() => {
        setMessages(prev => prev.map(msg => 
          msg.id === loadingMessage.id 
            ? { 
                ...msg, 
                text: "The maximum unhedged short exposure for a Specialized Investment Fund is capped at 25% of the Net Asset Value (NAV) [Source 1]. Additionally, leverage cannot exceed 2x the fund's equity [Source 2].", 
                citations: [
                  { chunk_id: "demo_1", document_title: "SEBI Circular 2023", document_type: "Regulatory", organization: "SEBI", page_number: 42, confidence: 0.99 },
                  { chunk_id: "demo_2", document_title: "SEBI Leveraged Funds Master Circular", document_type: "Regulatory", organization: "SEBI", page_number: 12, confidence: 0.95 }
                ], 
                retrieval: { chunks_retrieved: 5, search_time_ms: 12, embedding_model: "bge-small", llm: "demo-instant" },
                loading: false 
              }
            : msg
        ));
        setIsLoading(false);
      }, 1500);
      return;
    }

    try {
      const response = await submitQuery(query);
      setMessages(prev => prev.map(msg => 
        msg.id === loadingMessage.id 
          ? { ...msg, text: response.answer, citations: response.citations, retrieval: response.retrieval, loading: false }
          : msg
      ));
    } catch (error) {
      setMessages(prev => prev.map(msg => 
        msg.id === loadingMessage.id 
          ? { ...msg, text: 'Error connecting to the AI Research Engine. Please ensure the backend is running.', loading: false }
          : msg
      ));
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    const query = input;
    setInput('');
    executeQuery(query);
  };

  const clearChat = () => {
    setMessages([]);
    localStorage.removeItem('sif_messages');
  };

  return (
    <>
      {showTour && <Tour onComplete={completeTour} />}
      
      <TopNavBar 
        isDemoMode={isDemoMode} 
        setIsDemoMode={setIsDemoMode} 
      />
      <SideNavBar onViewChange={setCurrentView} currentView={currentView} />
      
      <main className="md:ml-[280px] md:pt-12 h-screen overflow-hidden flex flex-col md:flex-row bg-[#020617]">
        {currentView === 'chat' && (
          <>
            <div className="flex-1 flex flex-col h-full relative border-r border-[#152238] bg-[#071122]">
              {messages.length === 0 ? (
                <CommandCenter onSearch={executeQuery} />
              ) : (
                <>
                  <ChatArea 
                    messages={messages} 
                    onCitationClick={handleCitationClick} 
                    onClear={clearChat}
                  />
                  
                  {/* Input Area */}
                  <div className="absolute bottom-0 w-full p-4 bg-gradient-to-t from-[#020617] via-[#071122] to-transparent tour-search-box">
                    <form onSubmit={handleSubmit} className="flex gap-2 max-w-4xl mx-auto bg-[#051424] p-2 rounded-xl border border-[#152238] shadow-2xl focus-within:border-primary focus-within:ring-1 focus-within:ring-primary/50 transition-all">
                      <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask a question about SIF regulations or compare funds..."
                        className="flex-1 bg-transparent border-none focus:ring-0 text-on-surface p-3 placeholder-on-surface-variant/50 outline-none"
                        aria-label="Research Query Input"
                      />
                      <button 
                        type="submit" 
                        disabled={isLoading}
                        className="bg-primary text-on-primary px-6 rounded-lg font-semibold hover:bg-primary/90 transition-colors disabled:opacity-50 shadow-md focus:outline-none focus:ring-2 focus:ring-secondary focus:ring-offset-2 focus:ring-offset-[#020617]"
                      >
                        {isLoading ? 'Searching...' : 'Send'}
                      </button>
                    </form>
                  </div>
                </>
              )}
            </div>
            
            {activeCitationId && (
              <EvidenceExplorer 
                sourceId={activeCitationId} 
                onClose={handleCloseExplorer} 
                isDemoMode={isDemoMode}
              />
            )}
          </>
        )}
        
        <Suspense fallback={
          <div className="flex-1 flex items-center justify-center bg-[#071122]">
            <span className="material-symbols-outlined animate-spin text-primary text-4xl">sync</span>
          </div>
        }>
          {currentView === 'architecture' && (
            <div className="flex-1 flex flex-col h-full relative border-r border-[#152238] bg-[#071122] overflow-y-auto">
              <Architecture />
            </div>
          )}

          {currentView === 'insights' && (
            <div className="flex-1 flex flex-col h-full relative border-r border-[#152238] bg-[#071122] overflow-y-auto">
              <Insights />
            </div>
          )}
          
          {currentView === 'scheduler' && (
            <div className="flex-1 flex flex-col h-full relative border-r border-[#152238] bg-[#071122] overflow-y-auto">
              <SchedulerDashboard />
            </div>
          )}
        </Suspense>
      </main>
    </>
  );
}

export default App;
