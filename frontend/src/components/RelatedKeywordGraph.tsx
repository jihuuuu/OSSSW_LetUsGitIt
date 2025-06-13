// 📄 src/components/RelatedKeywordGraph.tsx
import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import * as d3 from "d3";
import type { PCluster } from "@/types/cluster";
import type { D3DragEvent } from "d3";

type Node = {
  id: number;
  name: string;
  clusterId: number;
  count?: number; // ✅ count 추가
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
};

type Props = {
  clusters: PCluster[];
};

export function RelatedKeywordGraph({ clusters }: Props) {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!svgRef.current) return;

    const width = 600;
    const height = 400;

    const nodes: Node[] = clusters.flatMap((cluster) =>
      cluster.keywords.map((k) => ({
        id: k.id,
        name: k.name,
        clusterId: cluster.id,
        count: k.count || 1, // ✅ count가 없으면 기본값 1
      }))
    );

    const centralNode = nodes.find((n) => n.id === -999);

    const edges: Edge[] = clusters.flatMap((cluster) => {
      const keywords = cluster.keywords;
    
      if (cluster.id === -1) return []; // 중심 클러스터는 건너뛰기
    
      const links: Edge[] = [];
    
      // 중심 노드와 연결
      if (centralNode) {
        for (const k of keywords) {
          links.push({ source: centralNode.id, target: k.id });
        }
      }
    
      // 클러스터 내부 키워드 간 연결 (원한다면 유지)
      for (let i = 0; i < keywords.length; i++) {
        for (let j = i + 1; j < keywords.length; j++) {
          links.push({ source: keywords[i].id, target: keywords[j].id });
        }
      }
    
      return links;
    });    

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    const simulation = d3
      .forceSimulation<Node>(nodes)
      .force("link", d3.forceLink<Node, Edge>(edges).id((d) => d.id).distance(80))
      .force("charge", d3.forceManyBody().strength(-200))
      .force("center", d3.forceCenter(width / 2, height / 2));

    const link = svg
      .append("g")
      .attr("stroke", "#aaa")
      .selectAll("line")
      .data(edges)
      .join("line")
      .attr("stroke-width", 1.5);

    const node = svg
      .append("g")
      .selectAll<SVGCircleElement, Node>("circle")
      .data(nodes)
      .join("circle")
      .attr("r", (d) => d.id === -999 ? 20 : 10 + Math.min(d.count || 1, 20))
      .attr("fill", (d) => {
        if (d.id === -999) return "#FDD835"; // 중심 노드 고정 색
        const base = d3.hsl(d3.schemeCategory10[d.clusterId % 10]);
        base.l = 0.6;
        return base.toString();
      })      
      .style("cursor", "pointer")
      .on("click", (event, d) => {
        navigate(`/keywords/${d.id}`);
      })
      .call(
        d3
          .drag<SVGCircleElement, Node>()
          .on("start", (event: D3DragEvent<SVGCircleElement, Node, Node>, d) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on("drag", (event: D3DragEvent<SVGCircleElement, Node, Node>, d) => {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on("end", (event: D3DragEvent<SVGCircleElement, Node, Node>, d) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          })
      );

    const labels = svg
      .append("g")
      .selectAll("text")
      .data(nodes)
      .join("text")
      .text((d) => d.name)
      .attr("font-size", (d) => d.id === -999 ? 16 : 12)
      .attr("text-anchor", "middle")
      .attr("dy", 4);

    simulation.on("tick", () => {
      link
        .attr("x1", (d) => (d.source as Node).x!)
        .attr("y1", (d) => (d.source as Node).y!)
        .attr("x2", (d) => (d.target as Node).x!)
        .attr("y2", (d) => (d.target as Node).y!);

      node.attr("cx", (d) => d.x!).attr("cy", (d) => d.y!);
      labels.attr("x", (d) => d.x!).attr("y", (d) => d.y!);
    });

    return () => {
      simulation.stop();
    };
  }, [clusters, navigate]);

  return (
  <svg
    ref={svgRef}
    viewBox="0 0 600 400"
    preserveAspectRatio="xMidYMid meet"
    className="w-full h-auto mx-auto my-4"
  />
);
}