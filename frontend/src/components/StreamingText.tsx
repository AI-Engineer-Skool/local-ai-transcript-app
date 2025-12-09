/**
 * StreamingText component - displays text with animated cursor during streaming.
 *
 * Features:
 * - Shows text content as it streams in
 * - Displays blinking cursor when actively streaming
 * - Smoothly handles empty content state
 */

import type { StreamingTextProps } from '../types';
import styles from './StreamingText.module.css';

export function StreamingText({ content, isStreaming }: StreamingTextProps) {
  // Don't render anything if no content and not streaming
  if (!content && !isStreaming) {
    return null;
  }

  return (
    <div className={styles.container}>
      <span className={styles.text}>
        {content || (isStreaming ? '' : '')}
      </span>
      {isStreaming && <span className={styles.cursor}>|</span>}
    </div>
  );
}
