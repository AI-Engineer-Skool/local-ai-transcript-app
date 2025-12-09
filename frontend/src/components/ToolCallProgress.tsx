/**
 * ToolCallProgress component - displays tool execution progress.
 *
 * Features:
 * - Shows completed tools with checkmark
 * - Shows currently executing tool with spinner
 * - Formats tool names for human readability
 */

import { Loader2, CheckCircle } from 'lucide-react';
import type { ToolCallProgressProps } from '../types';
import styles from './ToolCallProgress.module.css';

/**
 * Formats a snake_case tool name to Title Case.
 * e.g., "create_calendar_reminder" -> "Create Calendar Reminder"
 */
function formatToolName(name: string): string {
  return name
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

/**
 * Gets a friendly label for tool types.
 */
function getToolLabel(toolType: string): string {
  const labels: Record<string, string> = {
    calendar: 'Calendar Reminder',
    incident_report: 'Incident Report',
    decision_record: 'Decision Record',
    unknown: 'Tool',
  };
  return labels[toolType] || formatToolName(toolType);
}

export function ToolCallProgress({
  currentTool,
  completedTools,
}: ToolCallProgressProps) {
  // Don't render if nothing to show
  if (!currentTool && completedTools.length === 0) {
    return null;
  }

  return (
    <div className={styles.container}>
      {/* Completed tools */}
      {completedTools.map((toolType, idx) => (
        <div key={`completed-${idx}`} className={styles.completed}>
          <CheckCircle size={16} className={styles.checkIcon} />
          <span>{getToolLabel(toolType)}</span>
        </div>
      ))}

      {/* Currently executing tool */}
      {currentTool && (
        <div className={styles.running}>
          <Loader2 size={16} className={styles.spinner} />
          <span>Running {formatToolName(currentTool)}...</span>
        </div>
      )}
    </div>
  );
}
