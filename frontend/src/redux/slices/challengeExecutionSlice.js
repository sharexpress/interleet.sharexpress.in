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
  html: 'html',
  multi: 'multi',
};

// ─── Thunk: Run (against visible sample test cases) ─────────────────────────
export const runCode = createAsyncThunk(
  'challengeExecution/run',
  async ({ code, language, testCases = [], executionMode = 'cli', runtime = null }, { rejectWithValue }) => {
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
          ...(tc.verification_script ? { verification_script: tc.verification_script } : {}),
          ...(tc.files ? { files: tc.files } : {}),
        })),
        time_limit: 10,
        memory_limit: 256,
        execution_mode: executionMode,
        runtime,
      });
      return response.data;
    } catch (err) {
      let detail = err.response?.data?.detail || err.response?.data?.message || 'Execution failed';
      if (typeof detail !== 'string') detail = JSON.stringify(detail, null, 2);
      return rejectWithValue({ message: detail });
    }
  }
);

// ─── Thunk: Submit (against all test cases including hidden) ─────────────────
export const submitCode = createAsyncThunk(
  'challengeExecution/submit',
  async ({ code, language, slug, userId, contestId, executionMode = 'cli', runtime = null }, { dispatch, rejectWithValue }) => {
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
        execution_mode: executionMode,
        runtime,
      });

      const { submission_id } = queueRes.data;
      if (!submission_id) throw new Error('No submission_id returned');

      // Step 2: Poll with active backoff until result is ready (max 60s)
      const INTERVALS = [200, 400, 600, 800, 1200, 1500, 2000, 2000, 2000];
      const DEFAULT_INTERVAL = 2000;
      const MAX_WAIT_MS = 60_000;
      const start = Date.now();
      let attempt = 0;

      while (Date.now() - start < MAX_WAIT_MS) {
        const waitMs = attempt < INTERVALS.length ? INTERVALS[attempt] : DEFAULT_INTERVAL;
        await new Promise((r) => setTimeout(r, waitMs));
        attempt++;

        try {
          const resRes = await API.get(`/api/v1/submissions/${submission_id}`);
          if (resRes.data) {
            if (resRes.data.verdict || resRes.data.status === 'COMPLETED') {
              dispatch(updateActiveStatus('COMPLETED'));
              return { ...resRes.data, submission_id };
            }
            if (resRes.data.status) {
              dispatch(updateActiveStatus(resRes.data.status));
            }
          }
          continue;
        } catch (pollErr) {
          if (pollErr.response?.status === 404) {
            continue;
          }
          throw pollErr;
        }
      }

      return rejectWithValue({ message: 'Submission timed out — the sandbox may be under load. Check back shortly.' });
    } catch (err) {
      let detail = err.response?.data?.detail || err.response?.data?.message || 'Submission failed';
      if (typeof detail !== 'string') detail = JSON.stringify(detail, null, 2);
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
  activeStatus: null,  // 'QUEUED' | 'COMPILING' | 'RUNNING' | 'JUDGING' | 'COMPLETED'
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
      state.activeStatus = null;
    },
    updateActiveStatus(state, action) {
      state.activeStatus = action.payload;
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

export const { resetExecution, updateActiveStatus } = challengeExecutionSlice.actions;
export default challengeExecutionSlice.reducer;

// ─── Selectors ───────────────────────────────────────────────────────────────
export const selectChallengeExecution = (state) => state.challengeExecution;
export const selectRunResult = (state) => state.challengeExecution.runResult;
export const selectSubmitResult = (state) => state.challengeExecution.submitResult;
