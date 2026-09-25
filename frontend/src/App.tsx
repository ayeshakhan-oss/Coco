import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AppLayout } from './components/AppLayout'
import { ApplicationDetailPage } from './pages/ApplicationDetailPage'
import { AttendancePage } from './pages/AttendancePage'
import { CaseStudyPage } from './pages/CaseStudyPage'
import { CaseStudyTrackingPage } from './pages/CaseStudyTrackingPage'
import { CVScreeningPage } from './pages/CVScreeningPage'
import { ComingSoonPage } from './pages/ComingSoonPage'
import { DecisionBriefPage } from './pages/DecisionBriefPage'
import { DraftEditorPage } from './pages/DraftEditorPage'
import { EvaluationPage } from './pages/EvaluationPage'
import { TechScreeningPage } from './pages/TechScreeningPage'
import { HiringBriefPage } from './pages/HiringBriefPage'
import { HistoryPage } from './pages/HistoryPage'
import { KCDEvaluationPage } from './pages/KCDEvaluationPage'
import { HomePage } from './pages/HomePage'
import { InvitesPage } from './pages/InvitesPage'
import { LoginPage } from './pages/LoginPage'
import { QueuePage } from './pages/QueuePage'
import { ReviewInboxPage } from './pages/ReviewInboxPage'
import { SourcingPage } from './pages/SourcingPage'
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
          <Route path="/tech-screening" element={<TechScreeningPage />} />
          <Route path="/evaluations" element={<EvaluationPage />} />
          <Route path="/cv-screening" element={<CVScreeningPage />} />
          <Route path="/case-study-tracking" element={<CaseStudyTrackingPage />} />
          <Route path="/kcd-evaluations" element={<KCDEvaluationPage />} />
          <Route path="/attendance" element={<AttendancePage />} />
          <Route path="/decision-brief" element={<DecisionBriefPage />} />
          <Route path="/hiring-brief" element={<HiringBriefPage />} />
          <Route path="/sourcing" element={<SourcingPage />} />
          <Route path="/invites" element={<InvitesPage />} />
          <Route path="/applications/:id" element={<ApplicationDetailPage />} />
          <Route path="/drafts/:commId" element={<DraftEditorPage />} />
          <Route path="/review" element={<ReviewInboxPage />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="/users" element={<UsersPage />} />
          <Route path="/values-scorecards" element={<ValuesScorecardPage />} />
          <Route path="/case-studies" element={<CaseStudyPage />} />
          <Route path="/modules/:slug" element={<ComingSoonPage />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
