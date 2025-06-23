import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const BootstrapStatsApp = () => {
  const [selectedExercise, setSelectedExercise] = useState('');
  const [data1, setData1] = useState('');
  const [data2, setData2] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const exercises = [
    { id: '1', name: 'Estimación de la Media', desc: 'Intervalo de confianza para la media poblacional', icon: '📊' },
    { id: '2', name: 'Comparación de Dos Medias', desc: 'Diferencia significativa entre dos sistemas', icon: '⚖️' },
    { id: '3', name: 'Estimación de Proporciones', desc: 'Proporción de éxito en tratamiento médico', icon: '📈' },
    { id: '4', name: 'Correlación Bootstrap', desc: 'Coeficiente de correlación entre variables', icon: '🔗' },
    { id: '5', name: 'Mediana y Percentiles', desc: 'Estadísticas robustas con bootstrap', icon: '📏' },
    { id: '6', name: 'Razón de Varianzas', desc: 'Comparación de variabilidad entre procesos', icon: '📐' },
    { id: '7', name: 'Bootstrap en Regresión', desc: 'Coeficientes de regresión lineal', icon: '📉' },
    { id: '8', name: 'Diferencia de Proporciones', desc: 'Comparación de efectividad de tratamientos', icon: '🧪' },
    { id: '9', name: 'Bootstrap Paramétrico', desc: 'Estimación con distribución exponencial', icon: '⚡' },
    { id: '10', name: 'Bootstrap con Datos Dependientes', desc: 'Bootstrap por bloques para series temporales', icon: '🔄' }
  ];

  // Funciones estadísticas optimizadas
  const stats = {
    mean: arr => arr.reduce((a, b) => a + b, 0) / arr.length,
    variance: arr => {
      const m = stats.mean(arr);
      return arr.reduce((a, b) => a + (b - m) ** 2, 0) / (arr.length - 1);
    },
    std: arr => Math.sqrt(stats.variance(arr)),
    median: arr => {
      const s = [...arr].sort((a, b) => a - b);
      const mid = Math.floor(s.length / 2);
      return s.length % 2 ? s[mid] : (s[mid - 1] + s[mid]) / 2;
    },
    percentile: (arr, p) => {
      const s = [...arr].sort((a, b) => a - b);
      const idx = (p / 100) * (s.length - 1);
      const lower = Math.floor(idx);
      const upper = Math.ceil(idx);
      return s[lower] + (idx - lower) * (s[upper] - s[lower]);
    },
    correlation: (x, y) => {
      const n = x.length;
      const [sumX, sumY, sumXY, sumX2, sumY2] = [
        x.reduce((a, b) => a + b, 0),
        y.reduce((a, b) => a + b, 0),
        x.reduce((a, b, i) => a + b * y[i], 0),
        x.reduce((a, b) => a + b * b, 0),
        y.reduce((a, b) => a + b * b, 0)
      ];
      return (n * sumXY - sumX * sumY) / Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY));
    },
    linearRegression: (x, y) => {
      const n = x.length;
      const [sumX, sumY, sumXY, sumX2] = [
        x.reduce((a, b) => a + b, 0),
        y.reduce((a, b) => a + b, 0),
        x.reduce((a, b, i) => a + b * y[i], 0),
        x.reduce((a, b) => a + b * b, 0)
      ];
      const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
      return { slope, intercept: (sumY - slope * sumX) / n };
    }
  };

  const randomSample = (arr, size = arr.length) => 
    Array.from({length: size}, () => arr[Math.floor(Math.random() * arr.length)]);

  const blockBootstrap = (data, blockSize = 3) => {
    const blocks = [];
    for (let i = 0; i <= data.length - blockSize; i++) {
      blocks.push(data.slice(i, i + blockSize));
    }
    const numBlocks = Math.ceil(data.length / blockSize);
    const sample = [];
    for (let i = 0; i < numBlocks; i++) {
      sample.push(...blocks[Math.floor(Math.random() * blocks.length)]);
    }
    return sample.slice(0, data.length);
  };

  const runBootstrap = () => {
    setLoading(true);
    setTimeout(() => {
      try {
        const arr1 = data1.split(',').map(x => parseFloat(x.trim())).filter(x => !isNaN(x));
        const arr2 = data2 ? data2.split(',').map(x => parseFloat(x.trim())).filter(x => !isNaN(x)) : [];
        
        if (arr1.length === 0) {
          alert('Por favor ingresa datos válidos');
          setLoading(false);
          return;
        }

        const nBootstrap = 1000;
        let bootstrapStats = [];
        let result = {};

        // Ejecutar bootstrap según el ejercicio seleccionado
        const bootstrapFunctions = {
          '1': () => {
            for (let i = 0; i < nBootstrap; i++) {
              bootstrapStats.push(stats.mean(randomSample(arr1)));
            }
            bootstrapStats.sort((a, b) => a - b);
            return {
              originalMean: stats.mean(arr1).toFixed(4),
              bootstrapMean: stats.mean(bootstrapStats).toFixed(4),
              ci95: [stats.percentile(bootstrapStats, 2.5).toFixed(4), stats.percentile(bootstrapStats, 97.5).toFixed(4)]
            };
          },
          '2': () => {
            if (arr2.length === 0) throw new Error('Necesitas datos para ambos sistemas');
            for (let i = 0; i < nBootstrap; i++) {
              bootstrapStats.push(stats.mean(randomSample(arr1)) - stats.mean(randomSample(arr2)));
            }
            bootstrapStats.sort((a, b) => a - b);
            const originalDiff = stats.mean(arr1) - stats.mean(arr2);
            return {
              originalDiff: originalDiff.toFixed(4),
              bootstrapDiff: stats.mean(bootstrapStats).toFixed(4),
              ci95: [stats.percentile(bootstrapStats, 2.5).toFixed(4), stats.percentile(bootstrapStats, 97.5).toFixed(4)],
              significant: stats.percentile(bootstrapStats, 2.5) > 0 || stats.percentile(bootstrapStats, 97.5) < 0
            };
          },
          '3': () => {
            const originalProp = arr1.filter(x => x === 1).length / arr1.length;
            for (let i = 0; i < nBootstrap; i++) {
              const sample = randomSample(arr1);
              bootstrapStats.push(sample.filter(x => x === 1).length / sample.length);
            }
            bootstrapStats.sort((a, b) => a - b);
            return {
              originalProp: originalProp.toFixed(4),
              bootstrapProp: stats.mean(bootstrapStats).toFixed(4),
              ci90: [stats.percentile(bootstrapStats, 5).toFixed(4), stats.percentile(bootstrapStats, 95).toFixed(4)]
            };
          },
          '4': () => {
            if (arr2.length === 0 || arr1.length !== arr2.length) throw new Error('Necesitas dos variables con el mismo número de observaciones');
            const originalCorr = stats.correlation(arr1, arr2);
            for (let i = 0; i < nBootstrap; i++) {
              const indices = randomSample(Array.from({length: arr1.length}, (_, i) => i));
              bootstrapStats.push(stats.correlation(indices.map(i => arr1[i]), indices.map(i => arr2[i])));
            }
            bootstrapStats.sort((a, b) => a - b);
            return {
              originalCorr: originalCorr.toFixed(4),
              bootstrapCorr: stats.mean(bootstrapStats).toFixed(4),
              ci95: [stats.percentile(bootstrapStats, 2.5).toFixed(4), stats.percentile(bootstrapStats, 97.5).toFixed(4)]
            };
          },
          '10': () => {
            const originalVolatility = stats.std(arr1);
            for (let i = 0; i < nBootstrap; i++) {
              bootstrapStats.push(stats.std(blockBootstrap(arr1, 3)));
            }
            bootstrapStats.sort((a, b) => a - b);
            return {
              originalVolatility: originalVolatility.toFixed(4),
              bootstrapVolatility: stats.mean(bootstrapStats).toFixed(4),
              ci95: [stats.percentile(bootstrapStats, 2.5).toFixed(4), stats.percentile(bootstrapStats, 97.5).toFixed(4)]
            };
          }
        };

        result = bootstrapFunctions[selectedExercise] ? bootstrapFunctions[selectedExercise]() : {};
        result.histogram = bootstrapStats.slice(0, 50).map((val, i) => ({ x: i, y: val }));
        
        setResults(result);
        setLoading(false);
      } catch (error) {
        alert('Error: ' + error.message);
        setLoading(false);
      }
    }, 100);
  };

  const getDataLabels = () => {
    const labels = {
      '2': { label1: 'Sistema A:', label2: 'Sistema B:' },
      '4': { label1: 'Horas de estudio:', label2: 'Calificaciones:' },
      '6': { label1: 'Proceso 1:', label2: 'Proceso 2:' },
      '7': { label1: 'Publicidad (x):', label2: 'Ventas (y):' },
      '8': { label1: 'Tratamiento A:', label2: 'Tratamiento B:' }
    };
    return labels[selectedExercise] || { label1: 'Datos:', label2: null };
  };

  const labels = getDataLabels();
  const selectedEx = exercises.find(ex => ex.id === selectedExercise);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="max-w-6xl mx-auto p-6">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
            Bootstrap Analytics
          </h1>
          <p className="text-xl text-gray-600">Análisis estadístico avanzado con técnicas de remuestreo</p>
        </div>

        {/* Exercise Selection */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Selecciona tu Análisis</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {exercises.map(ex => (
              <div
                key={ex.id}
                onClick={() => setSelectedExercise(ex.id)}
                className={`p-4 rounded-xl cursor-pointer transition-all duration-300 hover:scale-105 ${
                  selectedExercise === ex.id 
                    ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg' 
                    : 'bg-gray-50 hover:bg-gray-100 text-gray-700'
                }`}
              >
                <div className="text-2xl mb-2">{ex.icon}</div>
                <h3 className="font-semibold text-sm mb-1">{ex.name}</h3>
                <p className="text-xs opacity-80">{ex.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Data Input */}
        {selectedExercise && (
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
            <div className="flex items-center mb-6">
              <span className="text-3xl mr-4">{selectedEx?.icon}</span>
              <div>
                <h2 className="text-2xl font-bold text-gray-800">{selectedEx?.name}</h2>
                <p className="text-gray-600">{selectedEx?.desc}</p>
              </div>
            </div>
            
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-3">{labels.label1}</label>
                <input
                  type="text"
                  value={data1}
                  onChange={(e) => setData1(e.target.value)}
                  placeholder="1.2, 3.4, 5.6, 7.8, 9.0..."
                  className="w-full p-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all duration-200"
                />
              </div>

              {labels.label2 && (
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-3">{labels.label2}</label>
                  <input
                    type="text"
                    value={data2}
                    onChange={(e) => setData2(e.target.value)}
                    placeholder="2.1, 4.3, 6.5, 8.7, 10.9..."
                    className="w-full p-4 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all duration-200"
                  />
                </div>
              )}

              <button
                onClick={runBootstrap}
                disabled={loading}
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 px-8 rounded-xl font-bold text-lg hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg"
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-3"></div>
                    Calculando Bootstrap...
                  </div>
                ) : (
                  'Ejecutar Análisis Bootstrap 🚀'
                )}
              </button>
            </div>
          </div>
        )}

        {/* Results */}
        {results && (
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h3 className="text-2xl font-bold text-gray-800 mb-6">📊 Resultados del Análisis</h3>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="space-y-4">
                <h4 className="text-lg font-semibold text-gray-700 mb-4">Estadísticas Principales</h4>
                <div className="space-y-3">
                  {Object.entries(results).map(([key, value]) => {
                    if (key === 'histogram') return null;
                    return (
                      <div key={key} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                        <span className="font-medium text-gray-600 capitalize">
                          {key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}:
                        </span>
                        <span className="font-bold text-gray-800">
                          {Array.isArray(value) ? `[${value.join(', ')}]` : value}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>
              
              <div>
                <h4 className="text-lg font-semibold text-gray-700 mb-4">Distribución Bootstrap</h4>
                <div className="h-64 bg-gray-50 rounded-lg p-4">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={results.histogram}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                      <XAxis dataKey="x" tick={{fontSize: 12}} />
                      <YAxis tick={{fontSize: 12}} />
                      <Tooltip 
                        contentStyle={{
                          backgroundColor: 'white',
                          border: 'none',
                          borderRadius: '8px',
                          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                        }}
                      />
                      <Bar dataKey="y" fill="url(#colorGradient)" radius={[2, 2, 0, 0]} />
                      <defs>
                        <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.8}/>
                          <stop offset="95%" stopColor="#8B5CF6" stopOpacity={0.8}/>
                        </linearGradient>
                      </defs>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Instructions */}
        <div className="mt-8 bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-6">
          <h3 className="font-bold text-gray-800 mb-3">💡 Instrucciones Rápidas</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-700">
            <div>• Selecciona el tipo de análisis que necesitas</div>
            <div>• Ingresa tus datos separados por comas</div>
            <div>• Para comparaciones, llena ambos campos</div>
            <div>• Se generan 1000 muestras bootstrap automáticamente</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BootstrapStatsApp;
