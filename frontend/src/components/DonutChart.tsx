import { PieChart, Pie, Cell, Legend, ResponsiveContainer } from 'recharts'

interface DonutChartProps {
  data: { name: string; value: number }[]
  title?: string
  colors?: string[]
}

export function DonutChart({
  data,
  title,
  colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'],
}: DonutChartProps) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      {title && <h3 className="font-semibold text-gray-900 mb-4">{title}</h3>}
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={100}
            dataKey="value"
            label
          >
            {data.map((_, index) => (
              <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
            ))}
          </Pie>
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}
