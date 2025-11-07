import { useState, useRef, useEffect } from 'react';
import { apiService, type ChatMessage, type ChatbotResponse } from '../services/api';
import '../css/ChatbotWidget.css';

export default function ChatbotWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Load session history when opening chat
    if (isOpen && sessionId) {
      loadHistory();
    } else if (isOpen && !sessionId) {
      // Create new session when opening for the first time
      createSession();
    }
  }, [isOpen]);

  const createSession = async () => {
    try {
      const response = await apiService.createChatbotSession();
      if (response.success) {
        setSessionId(response.session_id);
      }
    } catch (err) {
      console.error('Failed to create session:', err);
    }
  };

  const loadHistory = async () => {
    if (!sessionId) return;
    try {
      const response = await apiService.getChatbotHistory(sessionId);
      if (response.success && response.messages) {
        setMessages(response.messages);
      }
    } catch (err) {
      console.error('Failed to load history:', err);
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      role: 'user',
      message: inputMessage,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setError(null);

    try {
      const response: ChatbotResponse = await apiService.sendChatbotMessage(
        inputMessage,
        sessionId || undefined,
        'smotra'
      );

      if (response.success) {
        if (response.session_id && !sessionId) {
          setSessionId(response.session_id);
        }

        const botMessage: ChatMessage = {
          role: 'assistant',
          message: response.message || 'Nisam uspio dobiti odgovor.',
          timestamp: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, botMessage]);
      } else {
        setError(response.error || 'Greška pri slanju poruke');
        const errorMessage: ChatMessage = {
          role: 'assistant',
          message: 'Žao mi je, došlo je do greške. Molimo pokušajte ponovno.',
          timestamp: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, errorMessage]);
      }
    } catch (err: any) {
      setError(err.message || 'Greška pri slanju poruke');
      const errorMessage: ChatMessage = {
        role: 'assistant',
        message: 'Žao mi je, došlo je do greške. Molimo pokušajte ponovno.',
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      {/* Floating Chat Button */}
      <button
        className="chatbot-toggle-button"
        onClick={handleToggle}
        aria-label="Otvori chatbot"
        title="Virtualni asistent - Kako vam mogu pomoći?"
      >
        <svg
          width="28"
          height="28"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M20 2H4C2.9 2 2 2.9 2 4V22L6 18H20C21.1 18 22 17.1 22 16V4C22 2.9 21.1 2 20 2ZM20 16H6L4 18V4H20V16Z"
            fill="currentColor"
          />
          <circle cx="9" cy="9" r="1" fill="currentColor" opacity="0.6" />
          <circle cx="15" cy="9" r="1" fill="currentColor" opacity="0.6" />
        </svg>
        {!isOpen && (
          <span className="chatbot-pulse"></span>
        )}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <div className="chatbot-header-content">
              <h3>Virtualni asistent</h3>
              <p>Kako vam mogu pomoći?</p>
            </div>
            <button
              className="chatbot-close-button"
              onClick={() => setIsOpen(false)}
              aria-label="Zatvori chatbot"
            >
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path
                  d="M15 5L5 15M5 5L15 15"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                />
              </svg>
            </button>
          </div>

          <div className="chatbot-messages">
            {messages.length === 0 ? (
              <div className="chatbot-welcome">
                <p>👋 Dobrodošli!</p>
                <p>Ja sam vaš virtualni asistent. Mogu vam pomoći s:</p>
                <ul>
                  <li>Informacijama o fakultetima</li>
                  <li>Studentskim udrugama</li>
                  <li>Prakama i poslovima</li>
                  <li>Erasmus projektima</li>
                  <li>Karijernim savjetovanjem</li>
                </ul>
                <p>Što vas zanima?</p>
              </div>
            ) : (
              messages.map((msg, index) => (
                <div
                  key={index}
                  className={`chatbot-message chatbot-message-${msg.role}`}
                >
                  <div className="chatbot-message-content">{msg.message}</div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="chatbot-message chatbot-message-assistant">
                <div className="chatbot-message-content">
                  <span className="chatbot-typing">Pisanje...</span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chatbot-input-container">
            {error && <div className="chatbot-error">{error}</div>}
            <div className="chatbot-input-wrapper">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Upišite poruku..."
                disabled={isLoading}
                className="chatbot-input"
              />
              <button
                onClick={handleSendMessage}
                disabled={isLoading || !inputMessage.trim()}
                className="chatbot-send-button"
                aria-label="Pošalji poruku"
              >
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path
                    d="M18 2L9 11M18 2L12 18L9 11M18 2L2 8L9 11"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

