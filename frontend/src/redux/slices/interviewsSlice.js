import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { interviewHistory as mockInterviewHistory } from "@/lib/mock";
import { API } from "@/api/api";

// ─────────────────────────────────────────────────────────────
// Async Thunks
// ─────────────────────────────────────────────────────────────

/** POST /interview/start — kicks off a LangGraph session */
export const startInterview = createAsyncThunk(
  "interviews/startInterview",
  async (payload, { rejectWithValue }) => {
    try {
      const res = await API.post("/interview/start", payload);
      return res.data;
    } catch (err) {
      return rejectWithValue(
        err?.response?.data?.detail || "Failed to start interview"
      );
    }
  }
);

/** POST /interview/answer — submit user answer, get next question */
export const submitAnswer = createAsyncThunk(
  "interviews/submitAnswer",
  async ({ sessionId, answer, topic }, { rejectWithValue }) => {
    try {
      const res = await API.post("/interview/answer", {
        session_id: sessionId,
        answer,
        topic,
      });
      return res.data;
    } catch (err) {
      return rejectWithValue(
        err?.response?.data?.detail || "Failed to submit answer"
      );
    }
  }
);

/** GET /interview/{sessionId}/report — fetch completed report */
export const fetchReport = createAsyncThunk(
  "interviews/fetchReport",
  async (sessionId, { rejectWithValue }) => {
    try {
      const res = await API.get(`/interview/${sessionId}/report`);
      return res.data;
    } catch (err) {
      return rejectWithValue(
        err?.response?.data?.detail || "Failed to fetch report"
      );
    }
  }
);

// ─────────────────────────────────────────────────────────────
// Slice
// ─────────────────────────────────────────────────────────────

const initialState = {
  // ── Setup payload (carries from setup.jsx → live.jsx) ──────
  setupPayload: null, // { mock_test, parsed_resume }

  // ── Live session ────────────────────────────────────────────
  sessionId: null,
  currentQuestion: "",
  currentPreamble: "",
  currentAffect: "",
  answerGuidance: "",
  currentTopic: "",
  interviewPhase: "intro",
  coveredTopics: [],
  remainingTopics: [],
  transcript: [], // [{ id, from, text, timestamp, evaluation? }]
  isCompleted: false,
  completionReason: "",
  closingMessage: "",

  // ── Loading / error ─────────────────────────────────────────
  isStarting: false,
  isSubmitting: false,
  sessionError: null,

  // ── Report ──────────────────────────────────────────────────
  report: null,
  reportLoading: false,
  reportError: null,

  // ── History (list page) ─────────────────────────────────────
  history: mockInterviewHistory,
};

const interviewsSlice = createSlice({
  name: "interviews",
  initialState,
  reducers: {
    /** Call from setup.jsx before navigating to /live */
    setSetupPayload(state, action) {
      state.setupPayload = action.payload;
    },

    /** Append a message to the live transcript */
    appendTranscript(state, action) {
      state.transcript.push({
        id: Date.now(),
        timestamp: new Date().toLocaleTimeString("en-US", {
          hour: "2-digit",
          minute: "2-digit",
        }),
        ...action.payload,
      });
    },

    /** Clear session state when leaving live page */
    clearSession(state) {
      state.sessionId = null;
      state.currentQuestion = "";
      state.currentPreamble = "";
      state.currentAffect = "";
      state.answerGuidance = "";
      state.currentTopic = "";
      state.interviewPhase = "intro";
      state.coveredTopics = [];
      state.remainingTopics = [];
      state.transcript = [];
      state.isCompleted = false;
      state.completionReason = "";
      state.closingMessage = "";
      state.isStarting = false;
      state.isSubmitting = false;
      state.sessionError = null;
    },

    /** Clear report state */
    clearReport(state) {
      state.report = null;
      state.reportLoading = false;
      state.reportError = null;
    },

    addInterview(state, action) {
      state.history.unshift(action.payload);
    },

    updateInterviewHistory(state, action) {
      state.history = action.payload;
    },
  },

  extraReducers: (builder) => {
    // ── startInterview ────────────────────────────────────────
    builder
      .addCase(startInterview.pending, (state) => {
        state.isStarting = true;
        state.sessionError = null;
      })
      .addCase(startInterview.fulfilled, (state, action) => {
        const d = action.payload;
        state.isStarting = false;
        state.sessionId = d.session_id;
        state.currentQuestion = d.question || "";
        state.currentPreamble = d.preamble || "";
        state.currentAffect = d.affect || "";
        state.answerGuidance = d.answer_guidance || "";
        state.currentTopic = d.topic || "";
        state.interviewPhase = d.interview_phase || "intro";
        state.isCompleted = d.completed || false;

        // Push first AI message to transcript
        if (d.message) {
          state.transcript.push({
            id: Date.now(),
            from: "ai",
            text: d.message,
            question: d.question,
            preamble: d.preamble,
            topic: d.topic,
            timestamp: new Date().toLocaleTimeString("en-US", {
              hour: "2-digit",
              minute: "2-digit",
            }),
          });
        }
      })
      .addCase(startInterview.rejected, (state, action) => {
        state.isStarting = false;
        state.sessionError = action.payload;
      });

    // ── submitAnswer ──────────────────────────────────────────
    builder
      .addCase(submitAnswer.pending, (state) => {
        state.isSubmitting = true;
        state.sessionError = null;
      })
      .addCase(submitAnswer.fulfilled, (state, action) => {
        const d = action.payload;
        state.isSubmitting = false;
        state.isCompleted = d.completed || false;
        state.completionReason = d.completion_reason || "";
        state.closingMessage = d.closing_message || "";
        state.coveredTopics = d.covered_topics || [];
        state.remainingTopics = d.remaining_topics || [];

        if (d.completed) {
          state.currentQuestion = "";
          state.currentPreamble = "";
          // Store inline report if backend sends it
          if (d.report) {
            state.report = d.report;
          }
          // Push closing message to transcript
          if (d.closing_message) {
            state.transcript.push({
              id: Date.now(),
              from: "ai",
              text: d.closing_message,
              topic: "closing",
              timestamp: new Date().toLocaleTimeString("en-US", {
                hour: "2-digit",
                minute: "2-digit",
              }),
            });
          }
        } else {
          state.currentQuestion = d.question || "";
          state.currentPreamble = d.preamble || "";
          state.currentAffect = d.affect || "";
          state.answerGuidance = d.answer_guidance || "";
          state.currentTopic = d.topic || "";
          state.interviewPhase = d.interview_phase || "adaptive_questions";

          // Push next AI question to transcript
          if (d.message) {
            state.transcript.push({
              id: Date.now() + 1,
              from: "ai",
              text: d.message,
              question: d.question,
              preamble: d.preamble,
              topic: d.topic,
              evaluation: d.evaluation,
              timestamp: new Date().toLocaleTimeString("en-US", {
                hour: "2-digit",
                minute: "2-digit",
              }),
            });
          }
        }
      })
      .addCase(submitAnswer.rejected, (state, action) => {
        state.isSubmitting = false;
        state.sessionError = action.payload;
      });

    // ── fetchReport ───────────────────────────────────────────
    builder
      .addCase(fetchReport.pending, (state) => {
        state.reportLoading = true;
        state.reportError = null;
      })
      .addCase(fetchReport.fulfilled, (state, action) => {
        state.reportLoading = false;
        state.report = action.payload;
      })
      .addCase(fetchReport.rejected, (state, action) => {
        state.reportLoading = false;
        state.reportError = action.payload;
      });
  },
});

export const {
  setSetupPayload,
  appendTranscript,
  clearSession,
  clearReport,
  addInterview,
  updateInterviewHistory,
} = interviewsSlice.actions;

export default interviewsSlice.reducer;