import { useEffect, useState } from 'react'
import { useAuth } from '../auth/AuthContext'
import api from '../api/client'
import { KpiCard } from '../components/KpiCard'
import { DonutChart } from '../components/DonutChart'
import { Layout } from '../components/Layout'

interface KPI {
  code_efp: string | null
  nb_groupes: number
  effectif_total: number
  nb_formateurs_fp: number
  nb_formateurs_fv: number
  nb_salles: number
  nb_stagiaires_actifs: number
  mh_prevue: number
  mh_affectee: number
  mh_realisee: number
  taux_realisation: number
  taux_absence_moyen: number
  nb_modules_efm_fait: number
  nb_modules_total: number
}

export function Dashboard() {
  const { user } = useAuth()
  const [kpi, setKpi] = useState<KPI | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchKPI = async () => {
      try {
        const { data } = await api.get('/dashboard/kpi')
        setKpi(data)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    fetchKPI()
  }, [])

  if (loading) return <Layout><div>Chargement...</div></Layout>

  if (!kpi) return <Layout><div>Erreur de chargement</div></Layout>

  const mhData = [
    { name: 'MH Prévue', value: Math.round(kpi.mh_prevue) },
    { name: 'MH Affectée', value: Math.round(kpi.mh_affectee) },
    { name: 'MH Réalisée', value: Math.round(kpi.mh_realisee) },
  ]

  const efmData = [
    { name: 'EFM Validé', value: kpi.nb_modules_efm_fait },
    { name: 'EFM Restant', value: kpi.nb_modules_total - kpi.nb_modules_efm_fait },
  ]

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Tableau de bord</h1>
          <p className="text-gray-600 mt-1">Bienvenue, {user?.nom_complet}</p>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <KpiCard title="Groupes" value={kpi.nb_groupes} subtitle="Effectif total: " color="blue" />
          <KpiCard title="Formateurs" value={`${kpi.nb_formateurs_fp}/${kpi.nb_formateurs_fv}`} subtitle="FP/FV" color="green" />
          <KpiCard title="Salles" value={kpi.nb_salles} color="purple" />
          <KpiCard title="Stagiaires Actifs" value={kpi.nb_stagiaires_actifs} color="orange" />
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <DonutChart data={mhData} title="Masses Horaires (MH)" />
          <DonutChart data={efmData} title="Validation EFM" />
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <p className="text-sm text-gray-600">Taux de Réalisation</p>
            <p className="text-3xl font-bold text-blue-600 mt-2">{kpi.taux_realisation.toFixed(1)}%</p>
          </div>
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <p className="text-sm text-gray-600">Absence Moyenne</p>
            <p className="text-3xl font-bold text-orange-600 mt-2">{kpi.taux_absence_moyen.toFixed(1)}</p>
          </div>
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <p className="text-sm text-gray-600">Modules en Formation</p>
            <p className="text-3xl font-bold text-purple-600 mt-2">{kpi.nb_modules_total}</p>
          </div>
        </div>
      </div>
    </Layout>
  )
}
