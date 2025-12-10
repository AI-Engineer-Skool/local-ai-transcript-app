import { Brain } from 'lucide-react';
import { Box } from './Box';
import { IncidentReport } from './IncidentReport';
import { DecisionRecord } from './DecisionRecord';
import { StreamingText } from './StreamingText';
import { ToolCallProgress } from './ToolCallProgress';
import type {
  StreamingAgentResultsProps,
  IncidentReportData,
  DecisionRecordData,
  ToolResult,
} from '../types';
import styles from './AgentResults.module.css';

/**
 * Helper component for calendar download button.
 * Used in both streaming and non-streaming modes.
 */
function CalendarDownload({ result }: { result: ToolResult }) {
  const handleDownload = () => {
    if (!result.content || !result.filename) return;

    const blob = new Blob([result.content], { type: 'text/calendar' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = result.filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className={styles.calendarSection}>
      <div className={styles.calendarInfo}>
        Calendar reminder created with meeting summary, action items, blockers,
        and urgent issues
      </div>
      <button onClick={handleDownload} className={styles.downloadButton}>
        Download .ics File
      </button>
    </div>
  );
}

export function AgentResults({
  toolCalls,
  results,
  summary,
  error,
  isProcessing,
  // New streaming props
  isStreaming = false,
  streamingText = '',
  agentState = null,
  currentTool = null,
  currentToolArgs = '',
  completedTools = [],
}: StreamingAgentResultsProps) {
  // Streaming mode - show real-time updates
  if (isStreaming || streamingText) {
    // Use results from agentState if available, otherwise use prop
    const streamingResults = agentState?.tool_results || results || [];
    const effectiveCompletedTools =
      completedTools.length > 0
        ? completedTools
        : streamingResults.map((r: ToolResult) => r.type || 'unknown');

    return (
      <Box header="Agent Response" icon={Brain}>
        <div className={styles.container}>
          {/* Streaming text with cursor */}
          <StreamingText content={streamingText} isStreaming={isStreaming} />

          {/* Tool execution progress */}
          <ToolCallProgress
            currentTool={currentTool || agentState?.current_tool || null}
            currentToolArgs={currentToolArgs}
            completedTools={effectiveCompletedTools}
          />

          {/* Render completed tool results from streaming state */}
          {streamingResults.map((result: ToolResult, idx: number) => (
            <div key={idx}>
              {result.type === 'incident_report' &&
                result.markdown_content &&
                result.data && (
                  <IncidentReport
                    markdownContent={result.markdown_content}
                    data={result.data as IncidentReportData}
                  />
                )}
              {result.type === 'decision_record' &&
                result.markdown_content &&
                result.data && (
                  <DecisionRecord
                    markdownContent={result.markdown_content}
                    data={result.data as DecisionRecordData}
                  />
                )}
              {result.type === 'calendar' && result.filename && (
                <CalendarDownload result={result} />
              )}
            </div>
          ))}
        </div>
      </Box>
    );
  }

  // Legacy non-streaming mode
  if (isProcessing) {
    return (
      <Box header="Agent Processing" icon={Brain}>
        <div className={styles.processing}>
          <div className={styles.spinner}></div>
          <p>Analyzing transcript and executing tools...</p>
        </div>
      </Box>
    );
  }

  if (error) {
    return (
      <Box header="Agent Processing" icon={Brain}>
        <div className={styles.error}>
          {error}
        </div>
      </Box>
    );
  }

  if (!toolCalls || toolCalls.length === 0) {
    return null;
  }

  // Find calendar result
  const calendarResult = results?.find(r => r.type === 'calendar');

  // Find incident report result
  const incidentResult = results?.find(r => r.type === 'incident_report');

  // Find decision record result
  const decisionResult = results?.find(r => r.type === 'decision_record');

  // Create blob URL for calendar download
  const handleCalendarDownload = () => {
    if (!calendarResult?.content || !calendarResult.filename) return;

    const blob = new Blob([calendarResult.content], { type: 'text/calendar' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = calendarResult.filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <Box header="Agent Results" icon={Brain}>
      <div className={styles.container}>

        {/* Summary from agent */}
        {summary && (
          <div className={styles.summary}>
            {summary}
          </div>
        )}

        {/* Incident Report */}
        {incidentResult && incidentResult.markdown_content && incidentResult.data && (
          <IncidentReport
            markdownContent={incidentResult.markdown_content}
            data={incidentResult.data as IncidentReportData}
          />
        )}

        {/* Decision Record */}
        {decisionResult && decisionResult.markdown_content && decisionResult.data && (
          <DecisionRecord
            markdownContent={decisionResult.markdown_content}
            data={decisionResult.data as DecisionRecordData}
          />
        )}

        {/* Calendar download */}
        {calendarResult && calendarResult.filename && (
          <div className={styles.calendarSection}>
            <div className={styles.calendarInfo}>
              📅 Calendar reminder created with meeting summary, action items, blockers, and urgent issues
            </div>
            <button
              onClick={handleCalendarDownload}
              className={styles.downloadButton}
            >
              Download .ics File
            </button>
          </div>
        )}

        {/* Tool execution details */}
        <details className={styles.details}>
          <summary className={styles.detailsSummary}>
            Tool Execution Details ({toolCalls.length} executed)
          </summary>
          <div className={styles.toolList}>
            {toolCalls.map((call, idx) => (
              <div key={idx} className={styles.toolItem}>
                <code className={styles.toolName}>{call.name}</code>
                {results && results[idx] && (
                  <span className={styles.toolStatus}>
                    {results[idx].status === 'success' ? '✓' : '✗'} {results[idx].status}
                  </span>
                )}
              </div>
            ))}
          </div>
        </details>
      </div>
    </Box>
  );
}
