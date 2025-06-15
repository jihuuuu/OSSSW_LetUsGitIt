import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import * as d3 from "d3";

type Node = {
  id: number;
  name: string;
  count: number;
  x?: number;
  y?: number;
  vx?: number;
  vy?: number;
  fx?: number | null;
  fy?: number | null;
};

type Edge = {
  source: number | Node;
  target: number | Node;
  weight?: number;
};

type Props = {
  nodes: Node[];
  edges: Edge[];
};

export function KeywordGraph({ nodes, edges }: Props) {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!svgRef.current) return;

    const width = 900;
    const height = 400;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove(); // 초기화

    const colorScale = d3
      .scaleLinear<string>()
      .domain([0, 0.5, 1])
      .range(["#d0d0ff", "#8888ff", "#0000ff"]);

    const simulation = d3
      .forceSimulation<Node>(nodes)
      .force(
        "link",
        d3
          .forceLink<Node, Edge>(edges)
          .id((d) => d.id)
          .distance(180)
      )
      .force("charge", d3.forceManyBody().strength(-50))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("x", d3.forceX<Node>(width / 2).strength(0.01))
      .force("y", d3.forceY<Node>(height / 2).strength(0.03))
      .force(
        "collision",
        d3
          .forceCollide<Node>()
          .radius((d) => {
            const fontSize = 10 + Math.min(d.count, 20);
            return fontSize + d.name.length * 3;
          })
      );

    const link = svg
      .append("g")
      .attr("stroke-opacity", 0.6)
      .selectAll("line")
      .data(edges)
      .join("line")
      .attr("stroke", (d) =>
        colorScale(d.weight !== undefined ? d.weight : 0)
      )
      .attr("stroke-width", (d) =>
        d3.scaleLinear().domain([0, 1]).range([1, 4])(d.weight || 0)
      );

    const labels = svg
      .append("g")
      .selectAll("text")
      .data(nodes)
      .join("text")
      .text((d) => d.name)
      .attr("font-size", (d) => `${10 + Math.min(d.count, 20)}px`)
      .attr("text-anchor", "middle")
      .attr("dy", 4)
      .attr("fill", "black")
      .style("cursor", "pointer")
      .on("click", (_, d) => navigate(`/keywords/${d.id}`));

    (labels as d3.Selection<SVGTextElement, Node, any, any>).call(
      d3
        .drag<SVGTextElement, Node>()
        .on("start", (event, d) => {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        })
        .on("drag", (event, d) => {
          d.fx = event.x;
          d.fy = event.y;
        })
        .on("end", (event, d) => {
          if (!event.active) simulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        })
    );

    // ✅ tick 함수에서 간선 길이 보정
    simulation.on("tick", () => {
      link
        .attr("x1", (d) => {
          const src = d.source as Node;
          const tgt = d.target as Node;
          return adjustLinePosition(src, tgt).x1;
        })
        .attr("y1", (d) => {
          const src = d.source as Node;
          const tgt = d.target as Node;
          return adjustLinePosition(src, tgt).y1;
        })
        .attr("x2", (d) => {
          const src = d.source as Node;
          const tgt = d.target as Node;
          return adjustLinePosition(src, tgt).x2;
        })
        .attr("y2", (d) => {
          const src = d.source as Node;
          const tgt = d.target as Node;
          return adjustLinePosition(src, tgt).y2;
        });

      labels.attr("x", (d) => d.x!).attr("y", (d) => d.y!);
    });

    return () => { simulation.stop(); };

    // ✅ 라인 끝 좌표를 조정하여 텍스트 외곽에서 연결되도록 함
    function adjustLinePosition(src: Node, tgt: Node) {
      const dx = tgt.x! - src.x!;
      const dy = tgt.y! - src.y!;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist === 0) return { x1: src.x!, y1: src.y!, x2: tgt.x!, y2: tgt.y! };

      // 출발점과 도착점에서 각각 padding 만큼 밀기
      const offsetSrc = getNodeRadius(src);
      const offsetTgt = getNodeRadius(tgt);

      const ratioSrc = offsetSrc / dist;
      const ratioTgt = offsetTgt / dist;

      return {
        x1: src.x! + dx * ratioSrc,
        y1: src.y! + dy * ratioSrc,
        x2: tgt.x! - dx * ratioTgt,
        y2: tgt.y! - dy * ratioTgt,
      };
    }

    function getNodeRadius(d: Node) {
      const fontSize = 10 + Math.min(d.count, 20);
      return fontSize + d.name.length * 5;
    }
  }, [nodes, edges, navigate]);

  return (
    <svg
      ref={svgRef}
      viewBox="0 0 900 400"
      preserveAspectRatio="xMidYMid meet"
      className="w-full h-auto mx-auto my-4"
    />
  );
}
