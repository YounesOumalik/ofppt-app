import { useState } from 'react'
import { Layout } from '../components/Layout'
import { Eye } from 'lucide-react'

export function Data() {
  const [activeTab, setActiveTab] = useState<'stagiaires' | 'groupes' | 'formateurs' | 'modules' | 'avancement'>('stagiaires')

  const tabs = [
    { id: 'stagiaires' as const, label: 'Stagiaires', icon: '🎓' },
    { id: 'groupes' as const, label: 'Groupes', icon: '👥' },
    { id: 'formateurs' as const, label: 'Formateurs', icon: '👨‍🏫' },
    { id: 'modules' as const, label: 'Modules', icon: '📚' },
    { id: 'avancement' as const, label: 'Avancement', icon: '📊' },
  ]

  return (
    <Layout>
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Consultation Données</h1>

        <div className="flex space-x-2 mb-6 border-b border-gray-200 overflow-x-auto">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-3 font-medium transition whitespace-nowrap ${
                activeTab === tab.id
                  ? 'text-blue-600 border-b-2 border-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </div>

        <div className="bg-white border border-gray-200 rounded-lg p-8">
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <Eye className="mx-auto text-gray-400 mb-4" size={48} />
              <p className="text-gray-600">
                Tables de consultation à implémenter<br />
                <span className="text-sm">Recherche, tri, pagination par onglet</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  )
}
