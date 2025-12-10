/**
 * React hook for AG-UI event stream handling.
 *
 * This hook manages the connection to the AG-UI backend and handles:
 * - TEXT_MESSAGE_* events for streaming text content
 * - TOOL_CALL_* events for tool execution progress
 * - STATE_SNAPSHOT events for rich tool results (ICS, markdown, etc.)
 * - RUN_* events for lifecycle management
 *
 * Usage:
 *   const { isStreaming, textContent, agentState, runAgent, cancel } = useAgentStream();
 *   await runAgent("Process this meeting transcript...");
 */

import { useState, useCallback, useRef } from 'react';
import { HttpAgent } from '@ag-ui/client';
import type { AgentState, StreamingState } from '../types';

const initialState: StreamingState = {
  isStreaming: false,
  textContent: '',
  agentState: null,
  currentTool: null,
  currentToolArgs: '',
  completedTools: [],
  error: null,
};

export function useAgentStream() {
  const [state, setState] = useState<StreamingState>(initialState);
  const agentRef = useRef<HttpAgent | null>(null);

  const runAgent = useCallback(async (transcript: string) => {
    // Reset state for new run
    setState({
      ...initialState,
      isStreaming: true,
    });

    // Create HttpAgent instance
    const agent = new HttpAgent({
      url: '/api/agent',
    });
    agentRef.current = agent;

    // Set the user message
    agent.messages = [
      {
        id: `msg-${Date.now()}`,
        role: 'user',
        content: `Process this meeting transcript:\n\n${transcript}`,
      },
    ];

    try {
      // Run agent with subscriber for event handling
      await agent.runAgent(
        {
          runId: `run-${Date.now()}`,
        },
        {
          // Text message streaming
          onTextMessageStartEvent: () => {
            console.log('[AG-UI] Text message started');
          },
          onTextMessageContentEvent: ({ event }) => {
            setState((prev) => ({
              ...prev,
              textContent: prev.textContent + (event.delta || ''),
            }));
          },
          onTextMessageEndEvent: () => {
            console.log('[AG-UI] Text message ended');
          },

          // Tool call lifecycle
          onToolCallStartEvent: ({ event }) => {
            console.log(`[AG-UI] Tool call started: ${event.toolCallName}`);
            setState((prev) => ({
              ...prev,
              currentTool: event.toolCallName || null,
              currentToolArgs: '', // Reset args for new tool call
            }));
          },
          onToolCallArgsEvent: ({ event }) => {
            console.log('[AG-UI] Tool call args:', event.delta);
            setState((prev) => ({
              ...prev,
              currentToolArgs: prev.currentToolArgs + (event.delta || ''),
            }));
          },
          onToolCallEndEvent: ({ toolCallName }) => {
            console.log(`[AG-UI] Tool call ended: ${toolCallName}`);
            setState((prev) => ({
              ...prev,
              currentToolArgs: '', // Clear args when tool finishes
            }));
          },
          onToolCallResultEvent: ({ event }) => {
            console.log('[AG-UI] Tool call result:', event.content);
            // Tool completed - will be cleared when state snapshot arrives
          },

          // State synchronization (rich tool results)
          onStateSnapshotEvent: ({ event }) => {
            console.log('[AG-UI] State snapshot:', event.snapshot);
            const snapshot = event.snapshot as AgentState;
            setState((prev) => ({
              ...prev,
              agentState: snapshot,
              currentTool: snapshot.current_tool,
              // Track completed tools from results
              completedTools: snapshot.tool_results.map(
                (r) => r.type || 'unknown'
              ),
            }));
          },
          onStateDeltaEvent: ({ event }) => {
            console.log('[AG-UI] State delta:', event.delta);
            // Could apply JSON patch here for incremental updates
          },

          // Run lifecycle
          onRunStartedEvent: () => {
            console.log('[AG-UI] Run started');
          },
          onRunFinishedEvent: () => {
            console.log('[AG-UI] Run finished');
            setState((prev) => ({
              ...prev,
              isStreaming: false,
              currentTool: null,
            }));
          },
          onRunErrorEvent: ({ event }) => {
            console.error('[AG-UI] Run error:', event.message);
            setState((prev) => ({
              ...prev,
              isStreaming: false,
              error: event.message || 'Unknown error occurred',
              currentTool: null,
            }));
          },

          // Raw event handler for debugging
          onRawEvent: ({ event }) => {
            console.debug('[AG-UI] Raw event:', event.type);
          },
        }
      );
    } catch (error) {
      // Handle cancellation gracefully
      if (error instanceof Error && error.name === 'AbortError') {
        console.log('[AG-UI] Run was cancelled');
        setState((prev) => ({
          ...prev,
          isStreaming: false,
        }));
        return;
      }

      // Handle other errors
      console.error('[AG-UI] Error:', error);
      setState((prev) => ({
        ...prev,
        isStreaming: false,
        error: error instanceof Error ? error.message : 'Unknown error',
      }));
    }
  }, []);

  const cancel = useCallback(() => {
    if (agentRef.current) {
      agentRef.current.abortRun();
      agentRef.current = null;
    }
    setState((prev) => ({
      ...prev,
      isStreaming: false,
    }));
  }, []);

  const reset = useCallback(() => {
    cancel();
    setState(initialState);
  }, [cancel]);

  return {
    ...state,
    runAgent,
    cancel,
    reset,
  };
}
