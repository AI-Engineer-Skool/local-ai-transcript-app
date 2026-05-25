import { FileText, Sparkles } from 'lucide-react';
import styles from './TranscriptionResults.module.css';
import type { TranscriptionResultsProps } from '../types';
import { TextBox } from './TextBox';
import { Box } from './Box';
import { ModelQualityWarning } from './ModelQualityWarning';

export function TranscriptionResults({
  rawText,
  cleanedText,
  useLLM,
  isCopied,
  isCleaningWithLLM,
  isProcessing,
  isOriginalExpanded,
  onCopy,
  onToggleOriginalExpanded,
}: TranscriptionResultsProps) {
  // Show component if either processing or rawText exists
  if (!isProcessing && !rawText) {
    return null;
  }

  const displayText = useLLM && cleanedText ? cleanedText : rawText;

  return (
    <div className={styles.container}>
      <Box
        header="Original Transcription"
        icon={FileText}
        collapsible={true}
        isExpanded={isOriginalExpanded}
        onToggleExpanded={onToggleOriginalExpanded}
      >
        <TextBox
          mode="display"
          variant="default"
          value={rawText || ''}
          isLoading={isProcessing && !rawText}
          maxHeight="300px"
        />
      </Box>

      {/* Cleaned transcription (if LLM is enabled and cleaned text exists or is processing) */}
      {useLLM && (cleanedText || isCleaningWithLLM) && (
        <Box header="Cleaned Transcription" icon={Sparkles}>
          {cleanedText && <ModelQualityWarning />}
          <TextBox
            mode="display"
            variant="default"
            value={cleanedText || ''}
            isLoading={isCleaningWithLLM}
            showCopyButton={!!cleanedText}
            isCopied={isCopied}
            onCopy={() => cleanedText && onCopy(cleanedText)}
            maxHeight="300px"
          />
        </Box>
      )}

      {/* Copy button for non-LLM case */}
      {!useLLM && displayText && (
        <TextBox
          mode="display"
          variant="default"
          value={displayText}
          showCopyButton={true}
          isCopied={isCopied}
          onCopy={() => onCopy(displayText)}
          maxHeight="300px"
        />
      )}
    </div>
  );
}
