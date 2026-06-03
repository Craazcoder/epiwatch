import { useState, useEffect } from "react"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"
import axios from "axios"

export default function App() {
  const [stats, setStats] = useState(null)
  const [outbreaks, setOutbreaks] = useState([])
  const [stateId, setStateId] = useState(1)
  const [weekNum, setWeekNum] = useState(24)
  const [prediction, setPrediction] = useState(null)

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/stats").then(res => setStats(res.data))
    axios.get("http://127.0.0.1:8000/outbreaks").then(res => setOutbreaks(res.data))
  }, [])

  const handlePredict = () => {
    axios.get(`http://127.0.0.1:8000/predict/${stateId}/${weekNum}`)
      .then(res => setPrediction(res.data))
  }

  return (
    <div style={{ fontFamily: "Arial", padding: "20px", background: "#f0f2f5", minHeight: "100vh" }}>

      {/* Header */}
      <h1 style={{ color: "#1a237e", textAlign: "center" }}>🦠 EpiWatch Dashboard</h1>
      <p style={{ textAlign: "center", color: "#666" }}>Real-time Epidemic Detection Engine</p>

      {/* Stats Cards */}
      {stats && (
        <div style={{ display: "flex", gap: "20px", justifyContent: "center", margin: "20px 0" }}>
          <div style={{ background: "white", padding: "20px", borderRadius: "10px", textAlign: "center", minWidth: "200px", boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }}>
            <h2 style={{ color: "#e53935" }}>{stats.total_patients.toLocaleString()}</h2>
            <p>Total Patients</p>
          </div>
          <div style={{ background: "white", padding: "20px", borderRadius: "10px", textAlign: "center", minWidth: "200px", boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }}>
            <h2 style={{ color: "#1565c0" }}>{stats.total_diagnoses.toLocaleString()}</h2>
            <p>Total Diagnoses</p>
          </div>
        </div>
      )}

      {/* Prediction Box */}
      <div style={{ background: "white", padding: "20px", borderRadius: "10px", margin: "20px 0", boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }}>
        <h3 style={{ color: "#1a237e" }}>🔮 Outbreak Predictor</h3>
        <div style={{ display: "flex", gap: "10px", alignItems: "center", flexWrap: "wrap" }}>
          <div>
            <label>Region ID (1-6): </label>
            <input type="number" min="1" max="6" value={stateId}
              onChange={e => setStateId(e.target.value)}
              style={{ padding: "8px", borderRadius: "5px", border: "1px solid #ccc", width: "80px" }} />
          </div>
          <div>
            <label>Week Number (1-52): </label>
            <input type="number" min="1" max="52" value={weekNum}
              onChange={e => setWeekNum(e.target.value)}
              style={{ padding: "8px", borderRadius: "5px", border: "1px solid #ccc", width: "80px" }} />
          </div>
          <button onClick={handlePredict}
            style={{ padding: "8px 20px", background: "#1a237e", color: "white", border: "none", borderRadius: "5px", cursor: "pointer" }}>
            Predict
          </button>
        </div>

        {prediction && (
          <div style={{ marginTop: "15px", padding: "15px", borderRadius: "8px",
            background: prediction.outbreak_predicted ? "#ffebee" : "#e8f5e9" }}>
            <h4 style={{ color: prediction.outbreak_predicted ? "#e53935" : "#2e7d32" }}>
              {prediction.outbreak_predicted ? "⚠️ Outbreak Likely!" : "✅ No Outbreak Predicted"}
            </h4>
            <p>Probability: <strong>{prediction.probability}%</strong></p>
            <p>Region ID: {prediction.state_id} | Week: {prediction.week_num}</p>
          </div>
        )}
      </div>

      {/* Chart */}
      <div style={{ background: "white", padding: "20px", borderRadius: "10px", margin: "20px 0", boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }}>
        <h3 style={{ color: "#1a237e" }}>Cases by Region</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={outbreaks}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="state_name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="case_count" fill="#1565c0" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Table */}
      <div style={{ background: "white", padding: "20px", borderRadius: "10px", boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }}>
        <h3 style={{ color: "#1a237e" }}>Outbreak Table</h3>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ background: "#1a237e", color: "white" }}>
              <th style={{ padding: "10px", textAlign: "left" }}>Region</th>
              <th style={{ padding: "10px", textAlign: "left" }}>Cases</th>
            </tr>
          </thead>
          <tbody>
            {outbreaks.map((row, i) => (
              <tr key={i} style={{ background: i % 2 === 0 ? "#f5f5f5" : "white" }}>
                <td style={{ padding: "10px" }}>{row.state_name}</td>
                <td style={{ padding: "10px" }}>{row.case_count.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

    </div>
  )
}