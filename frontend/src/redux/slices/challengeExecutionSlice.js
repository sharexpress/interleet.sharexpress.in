import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { API } from '@/api/api';

// Map frontend editor lang codes → backend Language enum values
const LANG_MAP = {
  js: 'javascript',
  ts: 'typescript',
  py: 'python',
  go: 'go',
  cpp: 'cpp',
  rs: 'rust',
  java: 'java',
};

// ─── Thunk: Run (against visible sample test cases) ─────────────────────────
export const runCode = createAsyncThunk(
  'challengeExecution/run',
  async ({ code, language, testCases = [] }, { rejectWithValue }) => {
    const backendLang = LANG_MAP[language] || language;
    try {
      const response = await API.post('/api/v1/run', {
        language: backendLang,
        code,
        test_cases: testCases.map((tc) => ({
          id: tc.id || String(Math.random()),
          stdin: tc.stdin || '',
          expected_output: tc.expected_output || '',
          name: tc.name || null,
          hidden: tc.hidden || false,
        })),
        time_limit: 10,
        memory_limit: 256,
      });
      return response.data;
    } catch (err) {
      const detail = err.response?.data?.detail || err.response?.data?.message || 'Execution failed';
      return rejectWithValue({ message: detail });
    }
  }
);

// ─── Thunk: Submit (against all test cases including hidden) ─────────────────
export const submitCode = createAsyncThunk(
  'challengeExecution/submit',
  async ({ code, language, slug, userId, contestId }, { rejectWithValue }) => {
    const backendLang = LANG_MAP[language] || language;
    try {
      // Step 1: Enqueue submission
      const queueRes = await API.post('/api/v1/submissions', {
        language: backendLang,
        code,
        problem_slug: slug,
        user_id: userId || null,
        contest_id: contestId || null,
        mode: 'submit',
        time_limit: 10,
        memory_limit: 256,
      });

      const { submission_id } = queueRes.data;
      if (!submission_id) throw new Error('No submission_id returned');

      // Step 2: Poll with exponential backoff until result is ready (max 60s)
      // 404 = "not yet done" → keep polling. Only error on 5xx or other issues.
      const INTERVALS = [1000, 1500, 2000, 2000, 2000, 3000, 3000, 3000, 3000, 3000]; // first 10
      const DEFAULT_INTERVAL = 3000;
      const MAX_WAIT_MS = 60_000;
      const start = Date.now();
      let attempt = 0;

      while (Date.now() - start < MAX_WAIT_MS) {
        const waitMs = attempt < INTERVALS.length ? INTERVALS[attempt] : DEFAULT_INTERVAL;
        await new Promise((r) => setTimeout(r, waitMs));
        attempt++;

        try {
          const resRes = await API.get(`/api/v1/results/${submission_id}`);
          if (resRes.data && (resRes.data.verdict || resRes.data.status === 'COMPLETED')) {
            return { ...resRes.data, submission_id };
          }
          // Result returned but no verdict yet — worker still judging
          continue;
        } catch (pollErr) {
          if (pollErr.response?.status === 404) {
            // Worker hasn't finished yet — keep polling
            continue;
          }
          // Real error (500, network, etc.)
          throw pollErr;
        }
      }

      return rejectWithValue({ message: 'Submission timed out — the sandbox may be under load. Check back shortly.' });
    } catch (err) {
      const detail = err.response?.data?.detail || err.response?.data?.message || 'Submission failed';
      return rejectWithValue({ message: detail });
    }
  }
);

// ─── Slice ───────────────────────────────────────────────────────────────────
const initialState = {
  // Run (sample test cases)
  runStatus: 'idle',   // 'idle' | 'loading' | 'succeeded' | 'failed'
  runResult: null,     // Full ExecutionResult from /run
  runError: null,

  // Submit (all test cases)
  submitStatus: 'idle',
  submitResult: null,
  submitError: null,
  submissionId: null,
};

const challengeExecutionSlice = createSlice({
  name: 'challengeExecution',
  initialState,
  reducers: {
    resetExecution(state) {
      state.runStatus = 'idle';
      state.runResult = null;
      state.runError = null;
      state.submitStatus = 'idle';
      state.submitResult = null;
      state.submitError = null;
      state.submissionId = null;
    },
  },
  extraReducers: (builder) => {
    // ── runCode ──
    builder
      .addCase(runCode.pending, (state) => {
        state.runStatus = 'loading';
        state.runResult = null;
        state.runError = null;
      })
      .addCase(runCode.fulfilled, (state, action) => {
        state.runStatus = 'succeeded';
        state.runResult = action.payload;
      })
      .addCase(runCode.rejected, (state, action) => {
        state.runStatus = 'failed';
        state.runError = action.payload?.message || 'Run failed';
      });

    // ── submitCode ──
    builder
      .addCase(submitCode.pending, (state) => {
        state.submitStatus = 'loading';
        state.submitResult = null;
        state.submitError = null;
        state.submissionId = null;
      })
      .addCase(submitCode.fulfilled, (state, action) => {
        state.submitStatus = 'succeeded';
        state.submitResult = action.payload;
        state.submissionId = action.payload.submission_id || null;
      })
      .addCase(submitCode.rejected, (state, action) => {
        state.submitStatus = 'failed';
        state.submitError = action.payload?.message || 'Submission failed';
      });
  },
});

export const { resetExecution } = challengeExecutionSlice.actions;
export default challengeExecutionSlice.reducer;

// ─── Selectors ───────────────────────────────────────────────────────────────
export const selectChallengeExecution = (state) => state.challengeExecution;
export const selectRunResult = (state) => state.challengeExecution.runResult;
export const selectSubmitResult = (state) => state.challengeExecution.submitResult;
