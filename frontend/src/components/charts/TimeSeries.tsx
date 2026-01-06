import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, AreaChart, Area, BarChart, Bar } from 'recharts'
import { format } from 'date-fns'

type Serie = { name: string; dataKey: string; color: string; type?: 'line' | 'area' | 'bar' }

export function LineSeriesChart({ data, series, yUnit }: { data: any[]; series: Serie[]; yUnit?: string }) {
  return (
    <div style={{ width: '100%', height: 280 }}>
      <ResponsiveContainer>
        <LineChart data={data} margin={{ top: 10, right: 20, bottom: 0, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
          <XAxis dataKey="timestamp" tickFormatter={(t) => format(new Date(t), 'HH:mm')} stroke="#94a3b8" />
          <YAxis stroke="#94a3b8" tickFormatter={(v) => `${v}${yUnit ?? ''}`} />
          <Tooltip labelFormatter={(l) => format(new Date(l as string), 'PP HH:mm')} />
          <Legend />
          {series.map(s => (
            <Line key={s.name} type="monotone" dataKey={s.dataKey} name={s.name} stroke={s.color} dot={false} />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export function AreaSeriesChart({ data, series, yUnit }: { data: any[]; series: Serie[]; yUnit?: string }) {
  return (
    <div style={{ width: '100%', height: 280 }}>
      <ResponsiveContainer>
        <AreaChart data={data} margin={{ top: 10, right: 20, bottom: 0, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
          <XAxis dataKey="timestamp" tickFormatter={(t) => format(new Date(t), 'HH:mm')} stroke="#94a3b8" />
          <YAxis stroke="#94a3b8" tickFormatter={(v) => `${v}${yUnit ?? ''}`} />
          <Tooltip labelFormatter={(l) => format(new Date(l as string), 'PP HH:mm')} />
          <Legend />
          {series.map(s => (
            <Area key={s.name} type="monotone" dataKey={s.dataKey} name={s.name} stroke={s.color} fill={s.color} fillOpacity={0.2} />
          ))}
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}

export function BarSeriesChart({ data, series, yUnit }: { data: any[]; series: Serie[]; yUnit?: string }) {
  return (
    <div style={{ width: '100%', height: 280 }}>
      <ResponsiveContainer>
        <BarChart data={data} margin={{ top: 10, right: 20, bottom: 0, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
          <XAxis dataKey="timestamp" tickFormatter={(t) => format(new Date(t), 'HH:mm')} stroke="#94a3b8" />
          <YAxis stroke="#94a3b8" tickFormatter={(v) => `${v}${yUnit ?? ''}`} />
          <Tooltip labelFormatter={(l) => format(new Date(l as string), 'PP HH:mm')} />
          <Legend />
          {series.map(s => (
            <Bar key={s.name} dataKey={s.dataKey} name={s.name} fill={s.color} />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
