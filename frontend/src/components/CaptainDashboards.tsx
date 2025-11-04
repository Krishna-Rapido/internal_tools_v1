import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { DaprBucketAnalysis } from './DaprBucketAnalysis';
import { Fe2NetAnalysis } from './Fe2NetAnalysis';

type Section = 'quality' | 'retention' | null;
type QualityTab = 'dapr' | null;
type RetentionTab = 'fe2net' | null;

export function CaptainDashboards() {
    const [activeSection, setActiveSection] = useState<Section>(null);
    const [activeQualityTab, setActiveQualityTab] = useState<QualityTab>(null);
    const [activeRetentionTab, setActiveRetentionTab] = useState<RetentionTab>(null);

    const sections = [
        { id: 'quality', label: 'Quality', icon: '⭐', description: 'Quality metrics and analysis' },
        { id: 'retention', label: 'Retention', icon: '🔄', description: 'Retention and funnel analysis' },
        // Future sections can be added here
        // { id: 'performance', label: 'Performance', icon: '🚀', description: 'Performance analytics' },
    ];

    const qualityTabs = [
        { id: 'dapr', label: 'Dapr Bucket Distribution : Mode City Time level', icon: '📊' },
        // Future tabs:
        // { id: 'ratings', label: 'Ratings Analysis', icon: '⭐' },
        // { id: 'cancellations', label: 'Cancellation Patterns', icon: '❌' },
    ];

    const retentionTabs = [
        { id: 'fe2net', label: 'FE2Net Funnel', icon: '📈' },
        // Future tabs:
        // { id: 'cohort', label: 'Cohort Retention', icon: '👥' },
        // { id: 'churn', label: 'Churn Analysis', icon: '📉' },
    ];

    return (
        <div className="glass-card slide-in">
            <div className="card-header">
                <span className="card-icon">👨‍✈️</span>
                <div>
                    <h2 className="card-title">Captain Dashboards</h2>
                    <p className="card-subtitle">Specialized analytics and insights for captain management</p>
                </div>
            </div>

            <div className="mt-6">
                {/* Section Selection */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    {sections.map((section) => (
                        <motion.button
                            key={section.id}
                            onClick={() => {
                                setActiveSection(section.id as Section);
                                if (section.id === 'quality') {
                                    setActiveQualityTab('dapr');
                                    setActiveRetentionTab(null);
                                } else if (section.id === 'retention') {
                                    setActiveRetentionTab('fe2net');
                                    setActiveQualityTab(null);
                                }
                            }}
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                            className={`p-6 rounded-xl border-2 transition-all text-left ${activeSection === section.id
                                ? 'border-purple-500 bg-purple-50 shadow-lg'
                                : 'border-slate-200 bg-white hover:border-purple-300 hover:shadow-md'
                                }`}
                        >
                            <div className="flex items-center gap-3 mb-2">
                                <span className="text-3xl">{section.icon}</span>
                                <h3 className="text-lg font-bold text-slate-800">{section.label}</h3>
                            </div>
                            <p className="text-sm text-slate-600">{section.description}</p>
                        </motion.button>
                    ))}
                </div>

                {/* Section Content */}
                <AnimatePresence mode="wait">
                    {activeSection === 'quality' && (
                        <motion.div
                            key="quality"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            transition={{ duration: 0.3 }}
                            className="space-y-6"
                        >
                            {/* Quality Tabs */}
                            <div className="flex gap-2 border-b border-slate-200 pb-2">
                                {qualityTabs.map((tab) => (
                                    <button
                                        key={tab.id}
                                        onClick={() => setActiveQualityTab(tab.id as QualityTab)}
                                        className={`px-4 py-2 rounded-t-lg font-medium transition-all ${activeQualityTab === tab.id
                                            ? 'bg-purple-100 text-purple-700 border-b-2 border-purple-500'
                                            : 'text-slate-600 hover:bg-slate-50'
                                            }`}
                                    >
                                        <span className="mr-2">{tab.icon}</span>
                                        <span>{tab.label}</span>
                                    </button>
                                ))}
                            </div>

                            {/* Tab Content */}
                            <AnimatePresence mode="wait">
                                {activeQualityTab === 'dapr' && (
                                    <motion.div
                                        key="dapr"
                                        initial={{ opacity: 0, x: 20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        exit={{ opacity: 0, x: -20 }}
                                        transition={{ duration: 0.2 }}
                                    >
                                        <DaprBucketAnalysis />
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </motion.div>
                    )}

                    {/* Retention Section */}
                    {activeSection === 'retention' && (
                        <motion.div
                            key="retention"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            transition={{ duration: 0.3 }}
                            className="space-y-6"
                        >
                            {/* Retention Tabs */}
                            <div className="flex gap-2 border-b border-slate-200 pb-2">
                                {retentionTabs.map((tab) => (
                                    <button
                                        key={tab.id}
                                        onClick={() => setActiveRetentionTab(tab.id as RetentionTab)}
                                        className={`px-4 py-2 rounded-t-lg font-medium transition-all ${activeRetentionTab === tab.id
                                            ? 'bg-purple-100 text-purple-700 border-b-2 border-purple-500'
                                            : 'text-slate-600 hover:bg-slate-50'
                                            }`}
                                    >
                                        <span className="mr-2">{tab.icon}</span>
                                        <span>{tab.label}</span>
                                    </button>
                                ))}
                            </div>

                            {/* Tab Content */}
                            <AnimatePresence mode="wait">
                                {activeRetentionTab === 'fe2net' && (
                                    <motion.div
                                        key="fe2net"
                                        initial={{ opacity: 0, x: 20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        exit={{ opacity: 0, x: -20 }}
                                        transition={{ duration: 0.2 }}
                                    >
                                        <Fe2NetAnalysis />
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </motion.div>
                    )}

                    {/* Empty State */}
                    {!activeSection && (
                        <motion.div
                            key="empty"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="text-center py-16 text-slate-500"
                        >
                            <p className="text-5xl mb-4">👨‍✈️</p>
                            <p className="text-lg font-medium text-slate-700">Select a Dashboard</p>
                            <p className="text-sm mt-2">
                                Choose a section above to access specialized captain analytics
                            </p>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}

