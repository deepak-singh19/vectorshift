from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",  
    "http://localhost:3001",  # adjust this according to your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Node(BaseModel):
    id: str
    type: str
    data: Dict

class Edge(BaseModel):
    id: str
    source: str
    target: str

class Pipeline(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

@app.post('/pipelines/parse')
async def parse_pipeline(pipeline: Pipeline):
    num_nodes = len(pipeline.nodes)
    num_edges = len(pipeline.edges)

    graph = {node.id: [] for node in pipeline.nodes}
    for edge in pipeline.edges:
        graph[edge.source].append(edge.target)

    def is_dag(graph):
        visited = set()
        stack = set()

        def visit(node):
            if node in stack:
                return False
            if node in visited:
                return True

            stack.add(node)
            visited.add(node)
            for neighbor in graph[node]:
                if not visit(neighbor):
                    return False
            stack.remove(node)
            return True

        return all(visit(node) for node in graph)

    is_dag_result = is_dag(graph)

    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "is_dag": is_dag_result
    }
