import { createSlice, nanoid } from "@reduxjs/toolkit";

const defaultNodes = [
  {
    id: "n1",
    type: "infra",
    position: { x: 80, y: 240 },
    data: { kind: "client", label: "Client", category: "Client" },
  },
  {
    id: "n2",
    type: "infra",
    position: { x: 340, y: 240 },
    data: { kind: "load-balancer", label: "Load Balancer", category: "Network" },
  },
  {
    id: "n3",
    type: "infra",
    position: { x: 600, y: 240 },
    data: { kind: "api-gateway", label: "API Gateway", category: "Network" },
  },
  {
    id: "n4",
    type: "infra",
    position: { x: 860, y: 240 },
    data: { kind: "microservice", label: "Microservice", category: "Application" },
  },
  {
    id: "n5",
    type: "infra",
    position: { x: 1120, y: 120 },
    data: { kind: "redis", label: "Redis Cache", category: "Data" },
  },
  {
    id: "n6",
    type: "infra",
    position: { x: 1120, y: 360 },
    data: { kind: "postgresql", label: "PostgreSQL", category: "Data" },
  },
];

const defaultEdges = [
  {
    id: "e1-2",
    source: "n1",
    target: "n2",
    type: "traffic",
    animated: true,
    data: { kind: "request" },
  },
  {
    id: "e2-3",
    source: "n2",
    target: "n3",
    type: "traffic",
    animated: true,
    data: { kind: "request" },
  },
  {
    id: "e3-4",
    source: "n3",
    target: "n4",
    type: "traffic",
    animated: true,
    data: { kind: "request" },
  },
  {
    id: "e4-5",
    source: "n4",
    target: "n5",
    type: "traffic",
    animated: true,
    data: { kind: "cache" },
  },
  {
    id: "e4-6",
    source: "n4",
    target: "n6",
    type: "traffic",
    animated: true,
    data: { kind: "database" },
  },
];

const blankMetrics = () => ({
  throughput: 0,
  latency: 0,
  errorRate: 0,
  costHr: 0,
  health: "Healthy",
});

const resetCanvasState = (s) => {
  s.nodes = [];
  s.edges = [];
  s.selectedNodeId = null;
  s.metrics = blankMetrics();
  s.failure = null;
  s.simulation.running = false;
};

const slice = createSlice({
  name: "simulator",
  initialState: {
    nodes: defaultNodes,
    edges: defaultEdges,
    selectedNodeId: null,
    simulation: { running: false, userLoad: 1000, pattern: "constant", duration: "5m" },
    metrics: blankMetrics(),
    failure: null,
  },
  reducers: {
    setNodes: (s, a) => {
      s.nodes = a.payload;
    },
    setEdges: (s, a) => {
      s.edges = a.payload;
    },
    addNode: (s, a) => {
      s.nodes.push(a.payload);
    },
    addEdge: (s, a) => {
      s.edges.push({
        id: nanoid(),
        animated: true,
        type: "traffic",
        data: { kind: "request" },
        ...a.payload,
      });
    },
    updateNodeData: (s, a) => {
      const n = s.nodes.find((n) => n.id === a.payload.id);
      if (n) n.data = { ...n.data, ...a.payload.data };
    },
    selectNode: (s, a) => {
      s.selectedNodeId = a.payload;
    },
    setSimulation: (s, a) => {
      s.simulation = { ...s.simulation, ...a.payload };
    },
    setMetrics: (s, a) => {
      s.metrics = { ...s.metrics, ...a.payload };
    },
    setFailure: (s, a) => {
      s.failure = a.payload;
    },
    resetAll: (s) => {
      resetCanvasState(s);
    },
    clearCanvas: (s) => {
      resetCanvasState(s);
    },
    loadTemplate: (s, a) => {
      s.nodes = a.payload.nodes;
      s.edges = a.payload.edges;
      s.failure = null;
    },
  },
});

export const {
  setNodes,
  setEdges,
  addNode,
  addEdge,
  updateNodeData,
  selectNode,
  setSimulation,
  setMetrics,
  setFailure,
  resetAll,
  clearCanvas,
  loadTemplate,
} = slice.actions;
export default slice.reducer;
