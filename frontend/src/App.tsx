import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AppLayout } from './components/AppLayout'
import { ApplicationDetailPage } from './pages/ApplicationDetailPage'
import { LoginPage } from './pages/LoginPage'
import { Placeholder } from './pages/Placeholder'
import { QueuePage } from './pages/QueuePage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<AppLayout />}>
          <Route index element={<QueuePage />} />
          <Route path="/applications/:id" element={<ApplicationDetailPage />} />
          <Route
            path="/review"
            element={<Placeholder title="Review" note="Approval inbox arrives with the drafting + approval phase." />}
          />
          <Route
            path="/history"
            element={<Placeholder title="History" note="Sent-communication audit log arrives with the send phase." />}
          />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
