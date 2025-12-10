import { useState, useRef, useEffect, useCallback } from 'react';
import styles from './App.module.css';
import { Header } from './components/Header';
import { RecordButton } from './components/RecordButton';
import { UploadZone } from './components/UploadZone';
import { TextInputZone } from './components/TextInputZone';
import { SettingsPanel } from './components/SettingsPanel';
import { TranscriptionResults } from './components/TranscriptionResults';
import { AgentResults } from './components/AgentResults';
import { ErrorMessage } from './components/ErrorMessage';
import { Footer } from './components/Footer';
import { useAgentStream } from './hooks/useAgentStream';

interface TranscriptionResponse {
  success: boolean;
  text?: string;
  error?: string;
}

interface SystemPromptResponse {
  default_prompt: string;
}

interface CleanResponse {
  success: boolean;
  text?: string;
  error?: string;
}

function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [rawText, setRawText] = useState<string | null>(null);
  const [cleanedText, setCleanedText] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [useLLM, setUseLLM] = useState(false); // Default false - agent is separate now
  const [useAgent, setUseAgent] = useState(true); // Toggle for agent processing
  const [isCopied, setIsCopied] = useState(false);
  const [systemPrompt, setSystemPrompt] = useState('');
  const [isLoadingPrompt, setIsLoadingPrompt] = useState(true);
  const [isDragging, setIsDragging] = useState(false);
  const [isCleaningWithLLM, setIsCleaningWithLLM] = useState(false);
  const [isOriginalExpanded, setIsOriginalExpanded] = useState(true);

  // AG-UI streaming hook for real-time agent updates
  const {
    isStreaming,
    textContent: streamingText,
    agentState,
    currentTool,
    currentToolArgs,
    completedTools,
    error: streamingError,
    runAgent,
    reset: resetStreaming,
  } = useAgentStream();

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const isKeyDownRef = useRef(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const loadSystemPrompt = async () => {
      try {
        const response = await fetch('/api/system-prompt');
        const data = (await response.json()) as SystemPromptResponse;
        setSystemPrompt(data.default_prompt);
      } catch (err) {
        console.error('Failed to load system prompt:', err);
        setError('Failed to load system prompt');
      } finally {
        setIsLoadingPrompt(false);
      }
    };

    void loadSystemPrompt();
  }, []);

  // Process with AG-UI streaming agent
  const processWithAgent = useCallback(
    async (text: string) => {
      resetStreaming();
      await runAgent(text);
    },
    [runAgent, resetStreaming]
  );

  const uploadAudio = useCallback(
    async (audioBlob: Blob) => {
      const formData = new FormData();
      formData.append('audio', audioBlob, 'recording.webm');

      try {
        const transcribeResponse = await fetch('/api/transcribe', {
          method: 'POST',
          body: formData,
        });

        if (!transcribeResponse.ok) {
          throw new Error(
            `Transcription failed: ${transcribeResponse.statusText}`
          );
        }

        const transcribeData =
          (await transcribeResponse.json()) as TranscriptionResponse;

        if (!transcribeData.success) {
          throw new Error(transcribeData.error || 'Transcription failed');
        }

        setRawText(transcribeData.text || '');
        setIsProcessing(false);
        setError(null);

        // Auto-process with agent if enabled
        if (useAgent && transcribeData.text) {
          void processWithAgent(transcribeData.text);
        }

        // Optional: Clean with simple LLM if enabled
        if (useLLM && transcribeData.text) {
          setIsCleaningWithLLM(true);

          const cleanResponse = await fetch('/api/clean', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              text: transcribeData.text,
              ...(systemPrompt && { system_prompt: systemPrompt }),
            }),
          });

          if (!cleanResponse.ok) {
            setIsCleaningWithLLM(false);
            throw new Error(`Cleaning failed: ${cleanResponse.statusText}`);
          }

          const cleanData = (await cleanResponse.json()) as CleanResponse;

          if (cleanData.success && cleanData.text) {
            setCleanedText(cleanData.text);
          }

          setIsCleaningWithLLM(false);
        }
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : 'Unknown error';
        setError('Processing failed: ' + errorMessage);
        setIsProcessing(false);
      }
    },
    [useLLM, useAgent, systemPrompt, processWithAgent]
  );

  const startRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      mediaRecorderRef.current = new MediaRecorder(stream);
      chunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (e: BlobEvent) => {
        chunksRef.current.push(e.data);
      };

      mediaRecorderRef.current.onstop = async () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        await uploadAudio(blob);

        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
      setError(null);
      setRawText(null);
      setCleanedText(null);
      resetStreaming();
      setIsCleaningWithLLM(false);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      setError('Microphone access denied: ' + errorMessage);
    }
  }, [uploadAudio, resetStreaming]);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setIsProcessing(true);
    }
  }, [isRecording]);

  const processAudioFile = (file: File) => {
    if (!file) return;

    if (!file.type.startsWith('audio/')) {
      setError('Please select an audio file');
      return;
    }

    setError(null);
    setRawText(null);
    setCleanedText(null);
    resetStreaming();
    setIsProcessing(true);
    setIsCleaningWithLLM(false);

    const blob = new Blob([file], { type: file.type });
    void uploadAudio(blob);
  };

  const handleDragEnter = () => {
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (file: File) => {
    if (isProcessing || isRecording) return;
    processAudioFile(file);
  };

  const handleFileSelect = (file: File) => {
    processAudioFile(file);

    // Reset file input so the same file can be selected again
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleTextSubmit = useCallback(
    async (text: string) => {
      if (!text.trim()) return;

      try {
        setError(null);
        setRawText(null);
        setCleanedText(null);
        resetStreaming();
        setIsProcessing(true);
        setIsCleaningWithLLM(false);

        setRawText(text);
        setIsProcessing(false);

        // Auto-process with agent if enabled
        if (useAgent) {
          void processWithAgent(text);
        }

        // Optional: Clean with simple LLM if enabled
        if (useLLM) {
          setIsCleaningWithLLM(true);

          const cleanResponse = await fetch('/api/clean', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              text: text,
              ...(systemPrompt && { system_prompt: systemPrompt }),
            }),
          });

          if (!cleanResponse.ok) {
            setIsCleaningWithLLM(false);
            throw new Error(`Cleaning failed: ${cleanResponse.statusText}`);
          }

          const cleanData = (await cleanResponse.json()) as CleanResponse;

          if (cleanData.success && cleanData.text) {
            setCleanedText(cleanData.text);
          }

          setIsCleaningWithLLM(false);
        }
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : 'Unknown error';
        setError('Processing failed: ' + errorMessage);
        setIsProcessing(false);
        setIsCleaningWithLLM(false);
      }
    },
    [useLLM, useAgent, systemPrompt, processWithAgent, resetStreaming]
  );

  const copyToClipboard = (text: string) => {
    navigator.clipboard
      .writeText(text)
      .then(() => {
        setIsCopied(true);
        setTimeout(() => setIsCopied(false), 2000);
      })
      .catch((err: Error) => setError('Copy failed: ' + err.message));
  };

  // Keyboard shortcut: Hold V to record
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (isProcessing || e.repeat || isKeyDownRef.current) return;

      const target = e.target as HTMLElement;
      if (
        e.key.toLowerCase() === 'v' &&
        !['INPUT', 'TEXTAREA'].includes(target.tagName)
      ) {
        e.preventDefault();
        isKeyDownRef.current = true;

        if (!isRecording) {
          void startRecording();
        }
      }
    };

    const handleKeyUp = (e: KeyboardEvent) => {
      if (e.key.toLowerCase() === 'v') {
        isKeyDownRef.current = false;

        if (isRecording) {
          stopRecording();
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
    // startRecording and stopRecording are stable callbacks, safe to omit
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isRecording, isProcessing]);

  return (
    <div className={styles.app}>
      <div className={styles.container}>
        <Header />

        <RecordButton
          isRecording={isRecording}
          isProcessing={isProcessing}
          onStartRecording={startRecording}
          onStopRecording={stopRecording}
        />

        <UploadZone
          isProcessing={isProcessing}
          isDragging={isDragging}
          onFileSelect={handleFileSelect}
          onDragEnter={handleDragEnter}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          fileInputRef={fileInputRef}
        />

        <TextInputZone
          isProcessing={isProcessing}
          onTextSubmit={handleTextSubmit}
        />

        <SettingsPanel
          useLLM={useLLM}
          useAgent={useAgent}
          systemPrompt={systemPrompt}
          isLoadingPrompt={isLoadingPrompt}
          onToggleLLM={setUseLLM}
          onToggleAgent={setUseAgent}
          onPromptChange={setSystemPrompt}
        />

        {error && (
          <ErrorMessage message={error} onDismiss={() => setError(null)} />
        )}

        <TranscriptionResults
          rawText={rawText}
          cleanedText={cleanedText}
          useLLM={useLLM}
          isCopied={isCopied}
          isCleaningWithLLM={isCleaningWithLLM}
          isProcessing={isProcessing}
          isOriginalExpanded={isOriginalExpanded}
          onCopy={copyToClipboard}
          onToggleOriginalExpanded={() =>
            setIsOriginalExpanded(!isOriginalExpanded)
          }
        />

        <AgentResults
          // Streaming props (AG-UI)
          isStreaming={isStreaming}
          streamingText={streamingText}
          agentState={agentState}
          currentTool={currentTool}
          currentToolArgs={currentToolArgs}
          completedTools={completedTools}
          error={streamingError || undefined}
        />

        <Footer />
      </div>
    </div>
  );
}

export default App;
