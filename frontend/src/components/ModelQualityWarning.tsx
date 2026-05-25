import { AlertTriangle } from 'lucide-react';
import styles from './ModelQualityWarning.module.css';

export function ModelQualityWarning() {
  return (
    <div className={styles.container} role="note">
      <AlertTriangle className={styles.icon} aria-hidden="true" />
      <p className={styles.message}>
        Cleanups by a small local model aren't perfect, so the output here may
        not be what you expect.{' '}
        <a
          className={styles.link}
          href="https://www.skool.com/ai-engineer/classroom"
          target="_blank"
          rel="noopener noreferrer"
        >
          Follow the AI Engineer classroom
        </a>{' '}
        to learn how to migrate to a powerful local (GPU) or state-of-the-art
        cloud model. Improving this solution is a great first step to become an
        AI engineer.
      </p>
    </div>
  );
}
