/**
 * StreamingText component - displays text with animated cursor during streaming.
 *
 * Features:
 * - Shows text content as it streams in with markdown rendering
 * - Displays blinking cursor when actively streaming
 * - Smoothly handles empty content state
 */

import ReactMarkdown from 'react-markdown';
import type { StreamingTextProps } from '../types';
import styles from './StreamingText.module.css';

export function StreamingText({ content, isStreaming }: StreamingTextProps) {
  // Don't render anything if no content and not streaming
  if (!content && !isStreaming) {
    return null;
  }

  return (
    <div className={styles.container}>
      <div className={styles.text}>
        <ReactMarkdown>{content || ''}</ReactMarkdown>
      </div>
      {isStreaming && <span className={styles.cursor}>|</span>}
    </div>
  );
}
