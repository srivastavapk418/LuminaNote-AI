import React, { useState, useEffect } from "react";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

const GLOBAL_STYLES = `
  :root {
    --bg-gradient: radial-gradient(circle at top left, #1e293b, #020617 60%, #000000);
    --card-bg: rgba(15, 23, 42, 0.9);
    --card-border: rgba(148, 163, 184, 0.2);
    --accent: #38bdf8;
    --accent-soft: rgba(56, 189, 248, 0.2);
    --accent-strong: #0ea5e9;
    --accent-text: #e0f2fe;
    --danger: #fb7185;
    --text-main: #e5e7eb;
    --text-soft: #9ca3af;
    --radius-lg: 18px;
    --radius-md: 12px;
    --shadow-soft: 0 20px 60px rgba(15, 23, 42, 0.7);
  }

  * {
    box-sizing: border-box;
  }

  body {
    margin: 0;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Inter", sans-serif;
    background: var(--bg-gradient);
    color: var(--text-main);
  }

  .lumina-root {
    min-height: 100vh;
    padding: 24px 16px;
    display: flex;
    justify-content: center;
    align-items: flex-start;
  }

  .lumina-shell {
    width: 100%;
    max-width: 1040px;
    margin: 0 auto;
  }

  .lumina-header {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 24px;
  }

  .lumina-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 4px 12px;
    border-radius: 999px;
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(148, 163, 184, 0.3);
    color: var(--accent-text);
    font-size: 12px;
    width: fit-content;
  }

  .lumina-pill-dot {
    width: 8px;
    height: 8px;
    border-radius: 999px;
    background: #22c55e;
    box-shadow: 0 0 0 6px rgba(34, 197, 94, 0.25);
  }

  .lumina-title-row {
    display: flex;
    flex-wrap: wrap;
    align-items: flex-end;
    justify-content: space-between;
    gap: 16px;
  }

  .lumina-title-main {
    font-size: clamp(2rem, 4vw, 2.6rem);
    font-weight: 700;
    letter-spacing: 0.03em;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .lumina-title-badge {
    font-size: 11px;
    padding: 3px 8px;
    border-radius: 999px;
    background: rgba(56, 189, 248, 0.16);
    color: var(--accent-text);
    border: 1px solid rgba(56, 189, 248, 0.5);
  }

  .lumina-tagline {
    margin: 0;
    font-size: 14px;
    line-height: 1.6;
    color: var(--text-soft);
    max-width: 640px;
  }

  .lumina-layout {
    display: grid;
    grid-template-columns: minmax(0, 1.4fr) minmax(0, 1.6fr);
    gap: 20px;
  }

  .lumina-card {
    background: var(--card-bg);
    border-radius: var(--radius-lg);
    border: 1px solid var(--card-border);
    padding: 16px 18px;
    box-shadow: var(--shadow-soft);
    backdrop-filter: blur(14px);
  }

  .lumina-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 10px;
  }

  .lumina-card-title {
    font-size: 15px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .lumina-card-sub {
    margin: 0;
    font-size: 12px;
    color: var(--text-soft);
  }

  .lumina-chip {
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 999px;
    border: 1px solid rgba(148, 163, 184, 0.4);
    color: var(--text-soft);
  }

  .lumina-upload-zone {
    margin-top: 8px;
    border-radius: var(--radius-md);
    border: 1px dashed rgba(148, 163, 184, 0.6);
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    background: radial-gradient(circle at top left, rgba(56,189,248,0.08), transparent);
  }

  .lumina-upload-row {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 10px;
  }

  .lumina-file-input {
    padding: 6px 10px;
    border-radius: 999px;
    border: 1px solid rgba(148, 163, 184, 0.6);
    background: rgba(15, 23, 42, 0.9);
    color: var(--text-main);
    font-size: 13px;
  }

  .lumina-status {
    font-size: 12px;
    color: var(--text-soft);
  }

  .lumina-status-strong {
    color: var(--accent-text);
  }

  .lumina-tabs {
    display: flex;
    gap: 6px;
    margin-top: 10px;
    padding: 4px;
    border-radius: 999px;
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid rgba(51, 65, 85, 0.9);
  }

  .lumina-tab {
    flex: 1;
    font-size: 12px;
    padding: 6px 10px;
    border-radius: 999px;
    border: none;
    cursor: pointer;
    background: transparent;
    color: var(--text-soft);
    transition: all 0.18s ease-out;
  }

  .lumina-tab--active {
    background: linear-gradient(135deg, var(--accent), var(--accent-strong));
    color: #0b1220;
    font-weight: 600;
    box-shadow: 0 8px 20px rgba(56, 189, 248, 0.4);
  }

  .lumina-tab-icon {
    margin-right: 4px;
  }

  .lumina-main-panel {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 6px;
  }

  .lumina-field-label {
    font-size: 12px;
    color: var(--text-soft);
    margin-bottom: 4px;
  }

  .lumina-input {
    width: 100%;
    border-radius: var(--radius-md);
    border: 1px solid rgba(148, 163, 184, 0.6);
    background: rgba(15, 23, 42, 0.85);
    padding: 8px 10px;
    font-size: 13px;
    color: var(--text-main);
    outline: none;
    transition: border-color 0.16s ease-out, box-shadow 0.16s ease-out, background 0.16s ease-out;
  }

  .lumina-input:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 1px rgba(56, 189, 248, 0.8);
    background: rgba(15, 23, 42, 0.95);
  }

  .lumina-input-number {
    width: 80px;
    text-align: center;
  }

  .lumina-button-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
  }

  .lumina-btn {
    border-radius: 999px;
    border: none;
    font-size: 13px;
    padding: 8px 16px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: linear-gradient(135deg, var(--accent), var(--accent-strong));
    color: #020617;
    font-weight: 600;
    box-shadow: 0 10px 28px rgba(56, 189, 248, 0.5);
    transition: transform 0.12s ease-out, box-shadow 0.12s ease-out, opacity 0.12s ease-out;
  }

  .lumina-btn:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 16px 35px rgba(56, 189, 248, 0.7);
  }

  .lumina-btn:active:not(:disabled) {
    transform: translateY(0);
    box-shadow: 0 8px 18px rgba(56, 189, 248, 0.4);
  }

  .lumina-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    box-shadow: none;
  }

  .lumina-btn-secondary {
    background: rgba(15, 23, 42, 1);
    color: var(--accent-text);
    border: 1px solid rgba(148, 163, 184, 0.8);
    box-shadow: 0 10px 28px rgba(15, 23, 42, 0.8);
  }

  .lumina-badge-pill {
    font-size: 10px;
    padding: 2px 6px;
    border-radius: 999px;
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid rgba(148, 163, 184, 0.4);
    color: var(--text-soft);
  }

  .lumina-output {
    margin-top: 8px;
    border-radius: var(--radius-md);
    background: radial-gradient(circle at top left, rgba(15,23,42,0.96), rgba(15,23,42,0.98));
    padding: 12px 12px 10px;
    border: 1px solid rgba(51, 65, 85, 0.9);
    max-height: 360px;
    overflow-y: auto;
  }

  .lumina-output p,
  .lumina-output pre {
    margin: 0;
    white-space: pre-wrap;
    font-size: 13px;
  }

  .lumina-output-title {
    font-size: 12px;
    color: var(--text-soft);
    margin-bottom: 6px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .lumina-output-title span {
    font-weight: 500;
    color: var(--accent-text);
  }

  .lumina-mcq-item {
    margin-top: 10px;
    padding: 10px;
    border-radius: var(--radius-md);
    border: 1px solid rgba(51, 65, 85, 0.9);
    background: rgba(15, 23, 42, 0.96);
  }

  .lumina-mcq-question-label {
    font-size: 12px;
    color: var(--accent-text);
    margin-bottom: 4px;
  }

  .lumina-details {
    margin-top: 6px;
    font-size: 12px;
  }

  .lumina-details summary {
    cursor: pointer;
    color: var(--accent);
  }

  .lumina-footer {
    margin-top: 20px;
    font-size: 11px;
    color: var(--text-soft);
    display: flex;
    justify-content: space-between;
    gap: 8px;
    flex-wrap: wrap;
  }

  .lumina-footer span strong {
    color: var(--accent-text);
  }

  @media (max-width: 900px) {
    .lumina-layout {
      grid-template-columns: minmax(0, 1fr);
    }
  }

  @media (max-width: 640px) {
    .lumina-header {
      margin-bottom: 18px;
    }
    .lumina-card {
      padding: 14px 14px;
    }
    .lumina-title-main {
      font-size: 1.8rem;
    }
    .lumina-btn {
      width: 100%;
      justify-content: center;
    }
    .lumina-button-row {
      flex-direction: column;
      align-items: stretch;
    }
    .lumina-input-number {
      width: 100%;
      text-align: left;
    }
  }
`;

function App() {
  const [docId, setDocId] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [summary, setSummary] = useState("");
  const [topic, setTopic] = useState("");
  const [topicSummary, setTopicSummary] = useState("");
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [numQuestions, setNumQuestions] = useState(5);
  const [activeTab, setActiveTab] = useState("summary");
  const [statusMessage, setStatusMessage] = useState("");

  useEffect(() => {
    // inject global styles once
    const styleTag = document.createElement("style");
    styleTag.innerHTML = GLOBAL_STYLES;
    document.head.appendChild(styleTag);
    return () => {
      document.head.removeChild(styleTag);
    };
  }, []);

  async function handleUpload(e) {
    const file = e.target.files && e.target.files[0];
    if (!file) return;

    setUploading(true);
    setSummary("");
    setTopicSummary("");
    setQuestions([]);
    setAnswers([]);
    setStatusMessage("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${BACKEND_URL}/api/documents/upload`, {
        method: "POST",
        body: formData
      });

      let data = {};
      try {
        data = await res.json();
      } catch {
        // ignore JSON parse errors
      }

      if (res.ok) {
        setDocId(data.doc_id);
        setStatusMessage(`"${file.name}" uploaded & indexed successfully.`);
      } else {
        setDocId(null);
        setStatusMessage("");
        alert(data.error || "Upload failed on backend.");
      }
    } catch (err) {
      console.error("Upload error:", err);
      setDocId(null);
      setStatusMessage("");
      alert("Could not connect to backend. Check if backend is running on port 8000.");
    } finally {
      setUploading(false);
    }
  }

  async function fetchFullSummary() {
    if (!docId) return;
    setActiveTab("summary");
    setSummary("Loading summary…");
    try {
      const res = await fetch(`${BACKEND_URL}/api/summaries/full`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ doc_id: docId })
      });
      const data = await res.json();
      setSummary(data.summary || data.error || "Error generating summary");
    } catch (err) {
      console.error("Summary error:", err);
      setSummary("Failed to reach backend.");
    }
  }

  async function fetchTopicSummary() {
    if (!docId || !topic.trim()) return;
    setActiveTab("topic");
    setTopicSummary("Loading topic summary…");
    try {
      const res = await fetch(`${BACKEND_URL}/api/summaries/topic`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ doc_id: docId, topic })
      });
      const data = await res.json();
      setTopicSummary(
        data.summary || data.error || "Error generating topic summary"
      );
    } catch (err) {
      console.error("Topic summary error:", err);
      setTopicSummary("Failed to reach backend.");
    }
  }

  async function fetchQuestions() {
    if (!docId) return;
    setActiveTab("questions");
    setQuestions([]);
    setAnswers([]);
    try {
      const res = await fetch(`${BACKEND_URL}/api/questions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ doc_id: docId, num_questions: numQuestions })
      });
      const data = await res.json();
      if (!res.ok) {
        alert(data.error || "Failed to generate questions");
        return;
      }
      setQuestions(data.questions || []);
      setAnswers(data.answers || []);
    } catch (err) {
      console.error("Questions error:", err);
      alert("Failed to reach backend for questions.");
    }
  }

  return (
    <div className="lumina-root">
      <div className="lumina-shell">
        {/* Header */}
        <header className="lumina-header">
          <div className="lumina-pill">
            <span className="lumina-pill-dot" />
            <span>Online · Groq + Nomic Powered</span>
          </div>

          <div className="lumina-title-row">
            <div>
              <div className="lumina-title-main">
                LuminaNote AI
                <span role="img" aria-label="sparkles">
                  ✨
                </span>
                <span className="lumina-title-badge">Docs → Insights → MCQs</span>
              </div>
              <p className="lumina-tagline">
                Turn PDFs and text images into smart study companions. Upload a
                document, get focused summaries, topic explainers, and
                auto-generated MCQs — all grounded in your content.
              </p>
            </div>
          </div>
        </header>

        <main className="lumina-layout">
          {/* LEFT: Upload + Controls */}
          <section className="lumina-card">
            <div className="lumina-card-header">
              <div className="lumina-card-title">
                <span role="img" aria-label="upload">
                  📂
                </span>
                Upload & Setup
              </div>
              <span className="lumina-chip">Step 1</span>
            </div>
            <p className="lumina-card-sub">
              Start by dropping a PDF or a text-heavy image. LuminaNote will
              index it so you can query, summarize, and quiz yourself instantly.
            </p>

            <div className="lumina-upload-zone">
              <div className="lumina-upload-row">
                <input
                  type="file"
                  accept="*/*"
                  onChange={handleUpload}
                  className="lumina-file-input"
                />
                <button
                  className="lumina-btn lumina-btn-secondary"
                  type="button"
                  disabled
                >
                  <span role="img" aria-label="magic">
                    🪄
                  </span>
                  AI-ready after upload
                </button>
              </div>

              <div className="lumina-status">
                {uploading ? (
                  <span className="lumina-status-strong">
                    Uploading & processing…
                  </span>
                ) : docId ? (
                  <span className="lumina-status-strong">
                    Document processed. You can now generate summaries and MCQs.
                  </span>
                ) : (
                  "Select a PDF or image to begin."
                )}
                {statusMessage && (
                  <>
                    <br />
                    <span>{statusMessage}</span>
                  </>
                )}
              </div>
            </div>

            {docId && (
              <>
                <div className="lumina-card-header" style={{ marginTop: 16 }}>
                  <div className="lumina-card-title">
                    <span role="img" aria-label="sparkles">
                      🎯
                    </span>
                    Choose an action
                  </div>
                  <span className="lumina-badge-pill">Step 2</span>
                </div>

                <div className="lumina-tabs">
                  <button
                    className={
                      "lumina-tab" +
                      (activeTab === "summary" ? " lumina-tab--active" : "")
                    }
                    onClick={() => setActiveTab("summary")}
                    type="button"
                  >
                    <span className="lumina-tab-icon">🧾</span>
                    Full Summary
                  </button>
                  <button
                    className={
                      "lumina-tab" +
                      (activeTab === "topic" ? " lumina-tab--active" : "")
                    }
                    onClick={() => setActiveTab("topic")}
                    type="button"
                  >
                    <span className="lumina-tab-icon">📌</span>
                    Topic Explainer
                  </button>
                  <button
                    className={
                      "lumina-tab" +
                      (activeTab === "questions" ? " lumina-tab--active" : "")
                    }
                    onClick={() => setActiveTab("questions")}
                    type="button"
                  >
                    <span className="lumina-tab-icon">🧠</span>
                    Practice MCQs
                  </button>
                </div>

                <div className="lumina-main-panel">
                  {/* Full Summary controls */}
                  {activeTab === "summary" && (
                    <>
                      <p className="lumina-field-label">
                        Generate a high-level overview of the entire document.
                      </p>
                      <div className="lumina-button-row">
                        <button
                          className="lumina-btn"
                          onClick={fetchFullSummary}
                          type="button"
                        >
                          <span role="img" aria-label="doc">
                            📄
                          </span>
                          Generate full summary
                        </button>
                      </div>
                    </>
                  )}

                  {/* Topic Summary controls */}
                  {activeTab === "topic" && (
                    <>
                      <label className="lumina-field-label">
                        Topic or concept to focus on
                      </label>
                      <input
                        type="text"
                        placeholder="e.g., Multi-threading, Palindrome checking"
                        value={topic}
                        onChange={(e) => setTopic(e.target.value)}
                        className="lumina-input"
                      />
                      <div className="lumina-button-row">
                        <button
                          className="lumina-btn"
                          onClick={fetchTopicSummary}
                          type="button"
                          disabled={!topic.trim()}
                        >
                          <span role="img" aria-label="target">
                            🎯
                          </span>
                          Summarize this topic
                        </button>
                      </div>
                    </>
                  )}

                  {/* MCQs controls */}
                  {activeTab === "questions" && (
                    <>
                      <label className="lumina-field-label">
                        How many MCQs do you want?
                      </label>
                      <div className="lumina-button-row">
                        <input
                          type="number"
                          min="1"
                          value={numQuestions}
                          onChange={(e) =>
                            setNumQuestions(Number(e.target.value) || 1)
                          }
                          className={`lumina-input lumina-input-number`}
                        />
                        <button
                          className="lumina-btn"
                          onClick={fetchQuestions}
                          type="button"
                        >
                          <span role="img" aria-label="brain">
                            🧠
                          </span>
                          Generate MCQs
                        </button>
                      </div>
                      <p className="lumina-card-sub">
                        Questions are generated strictly from your uploaded
                        content, with solutions hidden under a toggle.
                      </p>
                    </>
                  )}
                </div>
              </>
            )}
          </section>

          {/* RIGHT: Outputs */}
          <section className="lumina-card">
            <div className="lumina-card-header">
              <div className="lumina-card-title">
                <span role="img" aria-label="result">
                  📊
                </span>
                AI Output
              </div>
              <span className="lumina-chip">
                {docId ? "Ready" : "Waiting for document"}
              </span>
            </div>
            <p className="lumina-card-sub">
              View summaries, topic-specific explanations, and practice
              questions — all grounded in your current document.
            </p>

            {/* Full summary output */}
            {summary && (
              <div className="lumina-output" style={{ marginTop: 10 }}>
                <div className="lumina-output-title">
                  <span>Full Summary</span>
                  <span className="lumina-badge-pill">Overview</span>
                </div>
                <p>{summary}</p>
              </div>
            )}

            {/* Topic summary output */}
            {topicSummary && (
              <div className="lumina-output" style={{ marginTop: 10 }}>
                <div className="lumina-output-title">
                  <span>Topic: {topic || "Selected concept"}</span>
                  <span className="lumina-badge-pill">Focused</span>
                </div>
                <p>{topicSummary}</p>
              </div>
            )}

            {/* MCQs output */}
            {questions.length > 0 && (
              <div className="lumina-output" style={{ marginTop: 10 }}>
                <div className="lumina-output-title">
                  <span>Practice MCQs</span>
                  <span className="lumina-badge-pill">
                    {questions.length} question(s)
                  </span>
                </div>

                {questions.map((q, idx) => (
                  <div key={idx} className="lumina-mcq-item">
                    <div className="lumina-mcq-question-label">
                      Q{idx + 1}
                    </div>
                    <pre>{q}</pre>
                    {answers[idx] && (
                      <details className="lumina-details">
                        <summary>Show solution</summary>
                        <p>{answers[idx]}</p>
                      </details>
                    )}
                  </div>
                ))}
              </div>
            )}

            {!summary && !topicSummary && questions.length === 0 && (
              <div className="lumina-output" style={{ marginTop: 10 }}>
                <p style={{ color: "var(--text-soft)", fontSize: 12 }}>
                  No AI output yet. Upload a document and choose an action on
                  the left to see summaries or questions here.
                </p>
              </div>
            )}
          </section>
        </main>

        <footer className="lumina-footer">
          <span>
            <strong>LuminaNote AI</strong> · Built for students who like their
            PDFs a little smarter.
          </span>
          <span>Backend: FastAPI · Frontend: React · Vector search: MongoDB</span>
        </footer>
      </div>
    </div>
  );
}

export default App;
