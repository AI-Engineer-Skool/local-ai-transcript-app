export type RecordingState = 'idle' | 'recording' | 'processing';

export interface AppState {
  isRecording: boolean;
  isProcessing: boolean;
  rawText: string | null;
  cleanedText: string | null;
  isCleaningWithLLM: boolean;
  error: string | null;
  useLLM: boolean;
  isCopied: boolean;
  systemPrompt: string;
  isLoadingPrompt: boolean;
  isDragging: boolean;
}

export interface TranscriptionResponse {
  text: string;
}

export interface CleanTextResponse {
  cleaned_text: string;
}

export interface SystemPromptResponse {
  default_prompt: string;
}

// eslint-disable-next-line @typescript-eslint/no-empty-object-type
export interface HeaderProps {}

export interface RecordButtonProps {
  isRecording: boolean;
  isProcessing: boolean;
  onStartRecording: () => Promise<void>;
  onStopRecording: () => void;
}

export interface UploadZoneProps {
  isProcessing: boolean;
  isDragging: boolean;
  onFileSelect: (file: File) => void;
  onDragEnter: () => void;
  onDragLeave: () => void;
  onDrop: (file: File) => void;
  fileInputRef: React.RefObject<HTMLInputElement | null>;
}

export interface TextInputZoneProps {
  isProcessing: boolean;
  onTextSubmit: (text: string) => Promise<void>;
}

export interface SettingsPanelProps {
  useLLM: boolean;
  systemPrompt: string;
  isLoadingPrompt: boolean;
  onToggleLLM: (value: boolean) => void;
  onPromptChange: (value: string) => void;
}

export interface TranscriptionResultsProps {
  rawText: string | null;
  cleanedText: string | null;
  useLLM: boolean;
  isCopied: boolean;
  isCleaningWithLLM: boolean;
  isProcessing: boolean;
  isOriginalExpanded: boolean;
  onCopy: (text: string) => void;
  onToggleOriginalExpanded: () => void;
}

export interface ErrorMessageProps {
  message: string;
  onDismiss: () => void;
}

export interface TextBoxProps {
  value: string;
  onChange?: (value: string) => void;
  placeholder?: string;
  mode: 'input' | 'display';
  variant?: 'default' | 'enhanced';
  isLoading?: boolean;
  isDisabled?: boolean;
  showCopyButton?: boolean;
  isCopied?: boolean;
  onCopy?: () => void;
  rows?: number;
  maxHeight?: string;
  ariaLabel?: string;
  id?: string;
}

export interface BoxProps {
  children: React.ReactNode;
  header?: string;
  icon?: React.ComponentType<{ className?: string }>;
  collapsible?: boolean;
  isExpanded?: boolean;
  onToggleExpanded?: () => void;
  className?: string;
}

export type AudioFileType =
  | 'audio/mpeg'
  | 'audio/wav'
  | 'audio/webm'
  | 'audio/ogg'
  | 'audio/x-m4a';

export const ACCEPTED_AUDIO_TYPES: AudioFileType[] = [
  'audio/mpeg',
  'audio/wav',
  'audio/webm',
  'audio/ogg',
  'audio/x-m4a',
];

// Agent & Tool Types
export interface ToolCall {
  name: string;
  input: Record<string, unknown>;
}

export interface ToolResult {
  status: string;
  type?: string;
  content?: string;
  filename?: string;
  markdown_content?: string;
  data?: IncidentReportData | CalendarData | DecisionRecordData | Record<string, unknown>;
  message?: string;
}

export interface AgentResponse {
  tool_calls?: ToolCall[];
  results?: ToolResult[];
  summary?: string;
  success: boolean;
  error?: string;
}

export interface AgentResultsProps {
  toolCalls?: ToolCall[];
  results?: ToolResult[];
  summary?: string;
  error?: string;
  isProcessing?: boolean;
}

// Calendar Tool Types
export interface ActionItem {
  task: string;
  owner: string;
  priority?: 'high' | 'medium' | 'low';
  due_date?: string;
}

export interface Blocker {
  blocker: string;
  affected_person: string;
}

export interface UrgentIssue {
  issue: string;
  severity: 'critical' | 'high' | 'medium';
}

export interface CalendarData {
  meeting_title: string;
  meeting_type: string;
  meeting_summary: string;
  key_points: string[];
  action_items: ActionItem[];
  blockers?: Blocker[];
  urgent_issues?: UrgentIssue[];
  reminder_date: string;
}

// Incident Report Types
export interface TimelineEvent {
  time: string;
  event: string;
  actor?: string;
}

export interface BusinessImpact {
  description?: string;
  downtime_duration?: string;
  affected_users?: string;
  failed_transactions?: string;
  revenue_impact?: string;
}

export interface FollowUpAction {
  action: string;
  owner: string;
  priority?: 'high' | 'medium' | 'low';
  due_date?: string;
}

export interface IncidentReportData {
  incident_title: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  start_time: string;
  detection_time?: string;
  resolution_time?: string;
  root_cause: string;
  business_impact?: BusinessImpact;
  timeline: TimelineEvent[];
  resolution_steps: string[];
  stakeholders_notified?: string[];
  follow_up_actions?: FollowUpAction[];
  additional_notes?: string;
}

export interface IncidentReportProps {
  markdownContent: string;
  data: IncidentReportData;
}

// Decision Record Types
export interface DecisionOption {
  option: string;
  pros?: string[];
  cons?: string[];
}

export interface DecisionConsequences {
  positive?: string[];
  negative?: string[];
  risks?: string[];
}

export interface DecisionRecordData {
  decision_title: string;
  decision_date: string;
  status: 'proposed' | 'accepted' | 'rejected' | 'deprecated' | 'superseded';
  context: string;
  options_considered: DecisionOption[];
  decision: string;
  rationale: string;
  consequences?: DecisionConsequences;
  decision_makers?: string[];
  additional_notes?: string;
}

export interface DecisionRecordProps {
  markdownContent: string;
  data: DecisionRecordData;
}

// =============================================================================
// AG-UI Streaming Types
// =============================================================================

/**
 * State synchronized from backend via AG-UI STATE_SNAPSHOT events.
 * Mirrors the AgentState model in backend/models.py.
 */
export interface AgentState {
  tool_results: ToolResult[];
  current_tool: string | null;
  processing_status: 'idle' | 'analyzing' | 'executing' | 'complete';
  current_date: string;
  one_week_from_now: string;
}

/**
 * State managed by the useAgentStream hook.
 * Combines streaming text, agent state, and UI state.
 */
export interface StreamingState {
  isStreaming: boolean;
  textContent: string;
  agentState: AgentState | null;
  currentTool: string | null;
  completedTools: string[];
  error: string | null;
}

/**
 * Props for the StreamingText component.
 */
export interface StreamingTextProps {
  content: string;
  isStreaming: boolean;
}

/**
 * Props for the ToolCallProgress component.
 */
export interface ToolCallProgressProps {
  currentTool: string | null;
  completedTools: string[];
}

/**
 * Extended AgentResultsProps for streaming support.
 * Supports both legacy (non-streaming) and new (streaming) modes.
 */
export interface StreamingAgentResultsProps extends AgentResultsProps {
  isStreaming?: boolean;
  streamingText?: string;
  agentState?: AgentState | null;
  currentTool?: string | null;
  completedTools?: string[];
}
