// src/components/LineChart.tsx
import { LineChart as RechartLineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';

export default function LineChart({ data }: { data: any[] }) {
  const keywordKeys = data.length > 0 ? Object.keys(data[0]).filter(k => k !== 'date') : [];

  return (
    <div className="bg-white rounded shadow p-4 h-full">
      <h2 className="text-lg font-bold mb-2">기사 수</h2>
      <ResponsiveContainer width="100%" height={300}>
        <RechartLineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          {keywordKeys.map(keyword => (
            <Line
              key={keyword}
              type="monotone"
              dataKey={keyword}
              stroke="#8884d8"
              strokeWidth={2}
            />
          ))}
        </RechartLineChart>
      </ResponsiveContainer>
    </div>
  );
}
