// 📄 src/components/TodayKeywordGraph.tsx

import React, { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import * as d3 from "d3";

type Cluster = {
  cluster_id: number;
  keywords: string[];
  num_articles: number; // 각 클러스터의 기사 수
};

type Props = {
  clusters: Cluster[];
};

type Node = {
  id: string;
  name: string;
  weight: number; // 키워드별 누적 기사 수
  x?: number;
  y?: number;
  vx?: number;
  vy?: number;
  fx?: number | null;
  fy?: number | null;
};

// offsetIndex: 같은 source-target 그룹 내에서 몇 번째 엣지인지 (0부터 시작)
// totalCount: 소속 그룹의 전체 엣지 개수
type Edge = {
  source: string | Node;
  target: string | Node;
  color: string;
  cluster_id: number;
  offsetIndex?: number;
  totalCount?: number;
};

export const TodayKeywordGraph: React.FC<Props> = ({ clusters }) => {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!svgRef.current) return;

    const width = 700;
    const height = 500;

    // 1) 키워드별 누적 weight 계산 (cluster.num_articles 합산)
    const weightMap = new Map<string, number>();
    clusters.forEach((cluster) => {
      cluster.keywords.forEach((kw) => {
        const prev = weightMap.get(kw) || 0;
        weightMap.set(kw, prev + cluster.num_articles);
      });
    });

    // 2) 고유 키워드 노드 생성 (weight 포함)
    const nodeMap = new Map<string, Node>();
    weightMap.forEach((weight, kw) => {
      nodeMap.set(kw, { id: kw, name: kw, weight });
    });
    const nodes: Node[] = Array.from(nodeMap.values());

    // 3) 같은 클러스터 내 키워드 쌍을 Edge로 연결 (색상 및 cluster_id 포함)
    let edges: Edge[] = [];
    clusters.forEach((cluster, idx) => {
      const color = d3.schemeCategory10[idx % 10];
      const kws = cluster.keywords;
      for (let i = 0; i < kws.length; i++) {
        for (let j = i + 1; j < kws.length; j++) {
          edges.push({
            source: kws[i],
            target: kws[j],
            color,
            cluster_id: cluster.cluster_id,
          });
        }
      }
    });

    // 4) “source-target” 키 기준으로 같은 쌍 그룹화하여 offsetIndex, totalCount 계산
    const pairMap = new Map<string, Edge[]>();
    edges.forEach((e) => {
      // source와 target 모두 Node 객체는 아니므로, 문자열 ID만 얻어야 함
      const srcId = typeof e.source === "string" ? e.source : e.source.id;
      const tgtId = typeof e.target === "string" ? e.target : e.target.id;
      // 키를 항상 “사전식 순서”로 만들어서 두 방향이 동일한 키가 되게 함
      const key =
        srcId < tgtId ? `${srcId}__${tgtId}` : `${tgtId}__${srcId}`;

      if (!pairMap.has(key)) {
        pairMap.set(key, []);
      }
      pairMap.get(key)!.push(e);
    });

    // 이제 각 그룹 내에서 index를 매기고 totalCount를 부여
    pairMap.forEach((groupEdges) => {
      const total = groupEdges.length;
      groupEdges.forEach((edgeObj, idx) => {
        edgeObj.offsetIndex = idx;
        edgeObj.totalCount = total;
      });
    });

    // 5) SVG 초기화
    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    // 6) D3 Force Simulation 설정
    const simulation = d3
      .forceSimulation<Node>(nodes)
      .force(
        "link",
        d3.forceLink<Node, Edge>(edges)
          .id((d) => d.id)
          .distance(100)
      )
      .force("charge", d3.forceManyBody().strength(-150))
      .force("x", d3.forceX(width / 2).strength(0.07))
      .force("y", d3.forceY(height / 2).strength(0.07));

    // 7) Edge를 <path>로 그리기 (곡선 형태)
    const link = svg
      .append("g")
      .attr("fill", "none")
      .selectAll<SVGPathElement, Edge>("path")
      .data(edges)
      .join("path")
      .attr("stroke", (d) => d.color)
      .attr("stroke-width", 2)
      .attr("opacity", 0.8)
      .style("cursor", "pointer")
      .on("click", (event, d) => {
        navigate(`/clusters/${d.cluster_id}`);
      });

    // 8) Node(circle) 그리기 — 내부 흰색, 테두리 회색
    const node = svg
      .append("g")
      .selectAll<SVGCircleElement, Node>("circle")
      .data(nodes)
      .join("circle")
      .attr("r", (d) => 5 + Math.sqrt(d.weight)*1.2) // weight가 클수록 반지름 증가
      .attr("fill", "#ffffff") // 내부는 흰색
     .style("cursor", "grab")
     .call(
       d3
         .drag<SVGCircleElement, Node>()
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
    
    // 9) Node 위에 레이블(text) 추가 — font-size 조정하여 weight 반영
    const labels = svg
      .append("g")
      .selectAll<SVGTextElement, Node>("text")
      .data(nodes)
      .join("text")
      .text((d) => d.name)
      .attr("font-size", (d) => `${5 + Math.sqrt(d.weight) * 1.5}px`)
      .attr("fill", "#333333")
      .attr("text-anchor", "middle")
      .attr("dy", (d) => {
        const size = 5 + Math.sqrt(d.weight) * 1.2;
        return `${size / 3}px`;
      })
      .attr("pointer-events", "none");

    // 10) 시뮬레이션 Tick 이벤트: path(d)와 node/label 위치 업데이트
    simulation.on("tick", () => {
      // 각 엣지마다 곡선 형태로 path 데이터(d) 계산
      link.attr("d", (d) => {
        const sourceNode = d.source as Node;
        const targetNode = d.target as Node;
        if (!sourceNode.x || !sourceNode.y || !targetNode.x || !targetNode.y) {
          return "";
        }

        // 노드 간의 벡터 (dx, dy)
        const dx = targetNode.x - sourceNode.x;
        const dy = targetNode.y - sourceNode.y;
        // 두 노드 중간 지점
        const mx = sourceNode.x + dx / 2;
        const my = sourceNode.y + dy / 2;

        // 그룹 내에서 몇 번째 엣지인지, 전체는 몇 개인지
        const { offsetIndex = 0, totalCount = 1 } = d;

        // “곡선의 굽힘 정도”를 결정할 기본 거리 (실험적으로 20 정도가 적당)
        const curveBase = 25;
        // 그룹 중심(가운데)에서 얼마나 멀리 이동해야 하는지 계산
        // 예: 총 3개 엣지면, offsetIndex 0 → -1, 1 → 0, 2 → +1 형태로 배치
        const offsetSign = offsetIndex! - (totalCount! - 1) / 2;
        const offsetAmount = offsetSign * (curveBase / Math.max(totalCount!, 1));

        // 노드 간 벡터의 수직 단위 벡터 구하기
        const length = Math.sqrt(dx * dx + dy * dy) || 1;
        const ux = -(dy / length);
        const uy = dx / length;

        // 중간 지점을 수직 방향으로 이동
        const cx = mx + ux * offsetAmount;
        const cy = my + uy * offsetAmount;

        // Quadratic Bézier 곡선: M → Q → L
        return `M${sourceNode.x},${sourceNode.y} Q${cx},${cy} ${targetNode.x},${targetNode.y}`;
      });

      node.attr("cx", (d) => d.x!).attr("cy", (d) => d.y!);
      labels.attr("x", (d) => d.x!).attr("y", (d) => d.y!);
    });

    // 11) 언마운트 혹은 clusters 변경 시 시뮬레이션 정리
    return () => {
      simulation.stop();
    };
  }, [clusters, navigate]);

  return (
    <svg
      ref={svgRef}
      width={700}
      height={500}
      className="border rounded-lg mx-auto my-4"
    />
  );
};
