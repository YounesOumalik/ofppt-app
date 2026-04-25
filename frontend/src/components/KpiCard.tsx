interface KpiCardProps {
  title: string
  value: string | number
  subtitle?: string
  color?: 'blue' | 'green' | 'purple' | 'orange'
}

const colors = {
  blue: 'bg-blue-50 border-blue-200',
  green: 'bg-green-50 border-green-200',
  purple: 'bg-purple-50 border-purple-200',
  orange: 'bg-orange-50 border-orange-200',
}

const textColors = {
  blue: 'text-blue-700',
  green: 'text-green-700',
  purple: 'text-purple-700',
  orange: 'text-orange-700',
}

export function KpiCard({ title, value, subtitle, color = 'blue' }: KpiCardProps) {
  return (
    <div className={`${colors[color]} border-2 rounded-lg p-6`}>
      <p className="text-sm font-medium text-gray-600">{title}</p>
      <p className={`text-3xl font-bold mt-2 ${textColors[color]}`}>{value}</p>
      {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
    </div>
  )
}
