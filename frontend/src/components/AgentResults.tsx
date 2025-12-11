import { Brain } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { Box } from './Box';
import { IncidentReport } from './IncidentReport';
import { DecisionRecord } from './DecisionRecord';
import type { AgentResultsProps, IncidentReportData, DecisionRecordData } from '../types';
import styles from './AgentResults.module.css';

export function AgentResults({ toolCalls, results, summary, error, isProcessing }: AgentResultsProps) {
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
          ❌ {error}
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
            <ReactMarkdown>{summary}</ReactMarkdown>
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
