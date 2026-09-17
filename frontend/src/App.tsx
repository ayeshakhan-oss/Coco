import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AppLayout } from './components/AppLayout'
import { ApplicationDetailPage } from './pages/ApplicationDetailPage'
import { ComingSoonPage } from './pages/ComingSoonPage'
import { DraftEditorPage } from './pages/DraftEditorPage'
import { EvaluationPage } from './pages/EvaluationPage'
import { HistoryPage } from './pages/HistoryPage'
import { HomePage } from './pages/HomePage'
import { LoginPage } from './pages/LoginPage'
import { QueuePage } from './pages/QueuePage'
import { ReviewInboxPage } from './pages/ReviewInboxPage'
import { UsersPage } from './pages/UsersPage'
import { ValuesScorecardPage } from './pages/ValuesScorecardPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<AppLayout />}>
          <Route index element={<HomePage />} />
          <Route path="/queue" element={<QueuePage />} />
          <Route path="/evaluations" element={<EvaluationPage />} />
          <Route path="/applications/:id" element={<ApplicationDetailPage />} />
          <Route path="/drafts/:commId" element={<DraftEditorPage />} />
          <Route path="/review" element={<ReviewInboxPage />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="/users" element={<UsersPage />} />
          <Route path="/values-scorecards" element={<ValuesScorecardPage />} />
          <Route path="/modules/:slug" element={<ComingSoonPage />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
